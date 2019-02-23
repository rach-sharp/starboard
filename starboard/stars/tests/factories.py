import datetime

import factory
import pytz
from factory.django import DjangoModelFactory

from starboard.stars.models import Repo, Star


class RepoFactory(DjangoModelFactory):
    class Meta:
        model = Repo

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"repo{n}")
    full_name = factory.Sequence(lambda n: f"Repo {n}")
    url = factory.Sequence(lambda n: f"https://test/repo{n}")
    default_branch = "master"

    created_at = datetime.datetime(year=2019, month=1, day=1, tzinfo=pytz.utc)
    updated_at = datetime.datetime(year=2019, month=1, day=1, tzinfo=pytz.utc)

    open_issues = 0
    stargazers_count = 0
    forks = 0
