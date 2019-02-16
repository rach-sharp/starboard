from urllib.parse import urljoin

import emoji
import markdown
import pytz
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.db import models
from github import Repository

from starboard.stars.utilities import ignore_sources


class Repo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True)
    url = models.CharField(max_length=255)
    homepage = models.CharField(max_length=1000, null=True)
    default_branch = models.CharField(max_length=500)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    language = models.CharField(max_length=255, null=True)

    image_url = models.URLField(null=True)

    open_issues = models.IntegerField()
    stargazers_count = models.IntegerField()
    forks = models.IntegerField()

    stargazers = models.ManyToManyField(get_user_model(), through='Star')

    @staticmethod
    def upsert_from_api_obj(repo: Repository):
        return Repo.objects.update_or_create(
            id=repo.id,
            defaults={
                "name": repo.name,
                "description": emoji.emojize(repo.description, use_aliases=True) if repo.description else None,
                "url": repo.html_url,
                "full_name": repo.full_name,
                "created_at": repo.created_at.replace(tzinfo=pytz.utc),
                "forks": repo.forks,
                "homepage": repo.homepage,
                "language": repo.language,
                "open_issues": repo.open_issues,
                "stargazers_count": repo.stargazers_count,
                "updated_at": repo.updated_at.replace(tzinfo=pytz.utc),
                "default_branch": repo.default_branch
            }
        )

    def raw_base(self):
        return f"https://raw.githubusercontent.com/{self.full_name}/{self.default_branch}"

    def first_img_in_readme(self):
        possible_readme_url = f"{self.raw_base()}/README.md"
        readme_response = requests.get(possible_readme_url)
        if readme_response.status_code == 200:
            html_markdown = markdown.markdown(readme_response.text)
            soup = BeautifulSoup(html_markdown)
            for img in soup.find_all('img'):
                if not ignore_sources(img):
                    img_src = img.attrs["src"]
                    if img_src.startswith('/'):
                        img_src = img_src[1:]
                    self.image_url = urljoin(possible_readme_url, img_src).replace("/blob/", "/raw/")
                    break
            else:
                self.image_url = None
        else:
            self.image_url = None
        self.save()

    def __str__(self):
        return self.name


class Star(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    starred_at = models.DateTimeField()
