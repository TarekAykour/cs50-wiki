from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("wiki/<str:title>/", views.entry,name="title"),
    path("create",views.create, name="create"),
    path("edit/<str:title>/",views.edit, name="edit"),
    path("random", views.random, name="random")
]
