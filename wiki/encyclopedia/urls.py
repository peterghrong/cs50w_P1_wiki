from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("<str:title>", views.title, name="title"),
    path("create/add", views.add, name="add"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("<str:title>/change", views.change, name="change"),
    path("random/", views.rand, name="random")
]
