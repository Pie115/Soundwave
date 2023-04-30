from django.urls import path

# from .views import geeks_view

from . import views

urlpatterns = [
    path("", views.selector_page, name="selector_page"),
    path("reset_list/", views.reset_list, name = "reset_list"),
    path("results/", views.results, name = "results"),
]