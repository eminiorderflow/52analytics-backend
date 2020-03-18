# from django standard library
from django.urls import path

# from project module
from .views import index


urlpatterns = [
    path('', index, name='index'),
]
