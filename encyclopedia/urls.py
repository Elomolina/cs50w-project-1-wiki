from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.encyclopedia, name = "encyclopedia"),
    path("search", views.search, name="search"),
    path("similar", views.similar, name="similar"),
    path("random_page", views.random_page, name = "random_page"),
    path("create", views.create, name="create")
]
