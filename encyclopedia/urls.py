from django.urls import path, re_path
from django.views.generic.base import RedirectView

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^wiki/?$", views.search_entry, name="search_entry"),
    re_path(r"^wiki/new/?$", views.create_entry, name="create_entry"),
    re_path(r"^wiki/(?P<entry_name>\w+)/?$", views.select_entry, name="select_entry"),
    re_path(r"^wiki/(?P<entry_name>.+)/edit/?$", views.edit_entry, name="edit_entry"),
    re_path(r"^random/?$", views.randomize, name="random"),
    re_path(r'^.+/?$', RedirectView.as_view(pattern_name='encyclopedia:index', permanent=True))
]
