from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def Index(request):
    return render(request, 'index.html')

def HomePage(request):
    return render(request, 'home-page.html')


def schedule_view(request):
    sessions = Session.objects.all().order_by('day', 'time')  # Fetch and order sessions
    context = {'sessions': sessions}
    return render(request, 'schedule.html', context) 


def event_detail_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    results = Result.objects.filter(event=event).order_by('rank')
    context = {'event': event, 'results': results}
    return render(request, 'session_detail.html', context) 

def results_view(request):
    results = Session.objects.all().order_by('day', 'time')  # Fetch and order sessions
    context = {'results': results}
    return render(request, 'results.html', context)