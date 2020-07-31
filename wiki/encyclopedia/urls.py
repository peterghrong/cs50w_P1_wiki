from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.add, name="create"),
    path("<str:title>", views.title, name="title"),
    #path("create/add", views.create, name="add")
]
