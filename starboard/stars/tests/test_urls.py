import pytest
from django.test import Client
from django.urls import reverse

from starboard.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_root_guest():
    c = Client()
    root_url = reverse("home")
    response = c.get(root_url)
    assert response.status_code == 301
    assert response.url == "top/"


def test_top_stars_guest():
    c = Client()
    response = c.get(reverse("top"))
    assert response.status_code == 200


def test_user_stars_guest():
    c = Client()
    user_stars_url = reverse("me")
    response = c.get(user_stars_url)
    assert response.status_code == 302
    assert response.url == f"/signup/?next={user_stars_url}"


def test_top_stars_authenticated():
    user = UserFactory()
    c = Client()
    c.force_login(user)
    user_stars_url = reverse("top")
    response = c.get(user_stars_url)
    assert response.status_code == 200


def test_user_stars_authenticated():
    user = UserFactory()
    c = Client()
    c.force_login(user)
    user_stars_url = reverse("me")
    response = c.get(user_stars_url)
    assert response.status_code == 200
