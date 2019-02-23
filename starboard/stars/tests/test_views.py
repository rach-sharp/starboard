import datetime

import pytest
import pytz
from django.test import Client
from django.urls import reverse

from starboard.stars.models import Star
from starboard.stars.tests.factories import RepoFactory
from starboard.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_stars_view():
    repo = RepoFactory()
    user = UserFactory()

    another_user = UserFactory()
    another_repo = RepoFactory()
    Star(user=another_user, repo=another_repo, starred_at=datetime.datetime.now(pytz.utc)).save()

    c = Client()
    c.force_login(user)

    response = c.get(reverse("me"))
    assert response.context_data["repo_list"].count() == 0
    assert repo.name not in response.rendered_content
    Star(user=user, repo=repo, starred_at=datetime.datetime.now(pytz.utc)).save()
    response = c.get(reverse("me"))
    assert response.context_data["repo_list"].count() == 1
    assert repo.name in response.rendered_content


def test_top_stars_view():
    repos = RepoFactory.create_batch(100)
    c = Client()
    response = c.get(reverse("top"))
    assert response.context_data["repo_list"].count() == 100
