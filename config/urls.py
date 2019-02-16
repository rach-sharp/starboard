from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView

from starboard.stars.views import user_starboard_view, top_starboard_view

urlpatterns = [
    path("", RedirectView.as_view(url='top/', permanent=True), name="home"),
    path("top/", top_starboard_view, name="top"),
    path("me/", user_starboard_view, name="me"),
    path("signup/", TemplateView.as_view(template_name="pages/signup.html"), name="signup"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),

    path("accounts/", include("starboard.contrib.allauth.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
