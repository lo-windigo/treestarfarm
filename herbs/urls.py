from __future__ import unicode_literals
from django.conf.urls import patterns, url
from herbs import views


urlpatterns = patterns("",
	url(r"^(?P<findSlug>.+)/$", views.herb, name="herb"),
	url(r"^latin/(?P<slug>.+)/$", views.herb, name="latin"),
)
