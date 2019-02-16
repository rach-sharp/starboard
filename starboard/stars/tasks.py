import itertools

import pytz
from allauth.socialaccount.models import SocialToken
from celery import shared_task
from django.contrib.auth import get_user_model
from github import Github

from starboard.stars.api_extensions import get_starred_with_dates
from starboard.stars.models import Repo, Star


@shared_task(bind=True, max_retries=5)
def get_repos_for_user(self, user_pk, count=None):
    try:
        user = get_user_model().objects.get(pk=user_pk)
        social_token = SocialToken.objects.get(account__user=user)
        github = Github(social_token.token)
        user_profile = github.get_user()
        starred = get_starred_with_dates(user_profile)
        repos = itertools.islice(starred, count) if count is not None else starred
        for starred_response in repos:
            if not starred_response.repository.private:
                repo, created = Repo.upsert_from_api_obj(starred_response.repository)
                if created:
                    get_image_url.delay(repo.pk)
                Star.objects.update_or_create(
                    user=user, repo=repo,
                    defaults={"starred_at": starred_response.starred_at.replace(tzinfo=pytz.utc)}
                )
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task
def get_top_repos(user_pk, count=600):
    user = get_user_model().objects.get(pk=user_pk)
    social_token = SocialToken.objects.get(account__user=user)
    github = Github(social_token.token)
    top_repos = github.search_repositories("stars:>1")
    repos = itertools.islice(top_repos, count) if count is not None else top_repos
    for repo_response in repos:
        repo, created = Repo.upsert_from_api_obj(repo_response)
        if created:
            get_image_url.delay(repo.pk)


@shared_task
def update_images_for_repos():
    for repo in Repo.objects.all():
        get_image_url.delay(repo.pk)


@shared_task
def get_image_url(repo_pk):
    repo = Repo.objects.get(pk=repo_pk)
    repo.first_img_in_readme()
