from django.urls import path

# from .views import geeks_view

from . import views

urlpatterns = [
    path("", views.selector_page, name="selector_page"),
    path("results/", views.reset_list, name = "reset_list"),
]