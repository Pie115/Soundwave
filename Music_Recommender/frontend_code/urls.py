from django.urls import path

# from .views import geeks_view

from .views import *

urlpatterns = [
    path("", geeks_view, name="geeks_view"),
    path("", new_view, name = "new_view"),
]