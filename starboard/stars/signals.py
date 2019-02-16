from allauth.account.signals import user_signed_up
from django.db import transaction
from django.dispatch import receiver

from starboard.stars import tasks


@receiver(user_signed_up)
def load_repos_for_new_user(user, **_):
    tasks.get_repos_for_user(user.pk, count=30)
    transaction.on_commit(tasks.get_repos_for_user.s(user.pk).delay)

