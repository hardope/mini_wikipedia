from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.search_que, name="search_que"),
    path("random", views.search_que, name="search_que"),
    path("<str:name>/edit", views.edit, name="edit"),
]
