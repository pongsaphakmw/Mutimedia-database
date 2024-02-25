from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('home/', HomePage, name='home-page'),
    path('schedule/', schedule_view, name='schedule'),
    re_path(r'^session/(?P<session_id>[0-9]+)/$', session_detail_view, name='session-detail'),
]