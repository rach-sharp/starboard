from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Repo(models.Model):

    name = models.CharField()
    description = models.CharField()
    created_at = models.DateTimeField()
    forks = models.IntegerField()
    homepage = models.CharField(blank=True)
    language = models.CharField(blank=True)
    open_issues = models.IntegerField()
    stargazers_count = models.IntegerField()
    updated_at = models.DateTimeField()
    topics = ArrayField(models.CharField())

    @staticmethod
    def from_api_obj(repo):
        return Repo()


class Star(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
