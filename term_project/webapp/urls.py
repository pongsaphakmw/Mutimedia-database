from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('home/', HomePage, name='home-page'),
    path('schedule/', schedule_view, name='schedule'),
    re_path(r'^event/(?P<event_id>[0-9]+)/$', event_detail_view, name='event-detail'),
    path('results/', results_view, name='results'),
    path('import_csv/', import_csv, name='import-csv'),
    path('athletes/', AthleteListView, name='athlete-list'),
]