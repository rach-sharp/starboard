from django.contrib import admin
from starboard.stars.models import Repo


@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    pass
