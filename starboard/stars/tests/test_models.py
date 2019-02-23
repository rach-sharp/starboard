import pytest
import requests

from starboard.stars.tests.factories import RepoFactory

pytestmark = pytest.mark.django_db


@pytest.mark.integration
def test_raw_base_exists():
    repo = RepoFactory(full_name="freeCodeCamp/freeCodeCamp", default_branch="master")
    response = requests.get(repo.raw_base() + "/README.md")
    assert response.status_code == 200
