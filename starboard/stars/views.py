import itertools

from allauth.socialaccount.models import SocialToken
from django.views.generic import TemplateView
from github import Github


class StarboardView(TemplateView):

    template_name = "pages/starboard.html"

    def get_context_data(self, **kwargs):
        context = super(StarboardView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            social_token = SocialToken.objects.get(account__user=self.request.user)
            github = Github(social_token.token)
            user_profile = github.get_user()
            starred = user_profile.get_starred()
            context["starred"] = itertools.islice(starred, 30)
        return context


starboard_view = StarboardView.as_view()
