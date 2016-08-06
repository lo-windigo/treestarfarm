from __future__ import unicode_literals
from django.conf.urls import url
from herbs import views


urlpatterns = [
	url(r"^(?P<findSlug>.+)/$", views.herb, name="herb"),
	url(r"^latin/(?P<slug>.+)/$", views.herb, name="latin"),
]
