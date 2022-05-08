from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.randompage, name="rand"),
    path("<str:title>", views.entry, name="title"),
    path("new/", views.new, name='new'),
    path("edit/<str:naziv>", views.edit, name='edit')
]
