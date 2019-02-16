import importlib

from allauth.account.views import login, logout
from allauth.socialaccount import providers
from django.conf.urls import include, url

providers_urlpatterns = []

for provider in providers.registry.get_list():
    prov_mod = importlib.import_module(provider.get_package() + ".urls")
    providers_urlpatterns += getattr(prov_mod, "urlpatterns", [])

urlpatterns = [
    url(r"^auth/", include(providers_urlpatterns)),
    url(r"^login/$", login, name="account_login"),
    url(r"^logout/$", logout, name="account_logout"),
]
