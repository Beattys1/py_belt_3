from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^add_quote/(?P<id>[0-9]+)', views.add_quote),
    url(r'^favorite_quote/(?P<id>[0-9]+)', views.favorite_quote),
    url(r'^remove_quote/(?P<id>[0-9]+)', views.remove_quote),
    url(r'^user/(?P<id>[0-9]+)', views.user),
]
