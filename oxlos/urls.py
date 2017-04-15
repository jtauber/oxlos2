from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin

from .views import (
    home,
    dashboard,
    item,
    item_random,
    project,
    task,
    join_project
)

urlpatterns = [
    url(r"^$", home, name="home"),
    url(r"^dashboard/$", dashboard, name="dashboard"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^teams/", include("pinax.teams.urls")),
    url(r"^projects/(?P<pk>\d+)/$", project, name="project"),
    url(r"^projects/(?P<pk>\d+)/join/$", join_project, name="join_project"),
    url(r"^tasks/(?P<pk>\d+)/$", task, name="task"),
    url(r"^tasks/(?P<pk>\d+)/random-item/$", item_random, name="item_random"),
    url(r"^items/(?P<pk>\d+)/$", item, name="item"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
