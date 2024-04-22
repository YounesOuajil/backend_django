from .views import create_interns_from_json
from django.urls import path

urlpatterns = [
    path('read-and-store-data/', create_interns_from_json, name='create_interns_from_json'),
]
