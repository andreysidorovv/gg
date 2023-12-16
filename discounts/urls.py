from django.urls import path

from . import admin
from .views import show_tables

urlpatterns = [
    path('tables/', show_tables, name='show_tables'),
]