from django.contrib.auth.mixins import LoginRequiredMixin
from el_pagination.views import AjaxListView

from starboard.stars.forms import StarOutputForm
from starboard.stars.models import Repo


class StarView(AjaxListView):

    model = Repo
    template_name = "pages/starboard.html"
    page_template = "pages/starboard_page.html"

    def get_context_data(self, **kwargs):
        # leaving in form logic for use if desired, but isn't being rendered in the frontend atm
        form = StarOutputForm(self.request.GET)
        context = super(StarView, self).get_context_data(**kwargs)
        context["form"] = form
        return context


class UserStarView(LoginRequiredMixin, StarView):

    def get_queryset(self):
        form = StarOutputForm(self.request.GET)
        qs = super(UserStarView, self).get_queryset().filter(star__user=self.request.user).order_by("-star__starred_at")
        if form.is_valid():
            if "language" in form.data:
                qs = qs.filter(language__iexact=form.data["language"])
        return qs


user_starboard_view = UserStarView.as_view()


class TopStarView(StarView):

    def get_queryset(self):
        form = StarOutputForm(self.request.GET)
        qs = super(TopStarView, self).get_queryset()
        if form.is_valid():
            if "language" in form.data:
                qs = qs.filter(language__iexact=form.data["language"])
        return qs.order_by("-stargazers_count")


top_starboard_view = TopStarView.as_view()
