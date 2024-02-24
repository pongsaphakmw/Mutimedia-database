from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('home/', HomePage, name='home-page'),
]