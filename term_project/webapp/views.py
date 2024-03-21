from django.shortcuts import render, get_object_or_404, redirect
from .models import *

# Create your views here.
def Index(request):
    return render(request, 'index.html')

def HomePage(request):
    return render(request, 'home-page.html')


def schedule_view(request):
    sessions = Session.objects.all().order_by('day', 'time')  # Fetch and order sessions
    results = Result.objects.all().order_by('rank') # Fetch and order results
    context = {'sessions': sessions,
               'results': results}
    results = Result.objects.all()
    context = {'sessions': sessions, 'results': results}
    return render(request, 'schedule.html', context) 


def event_detail_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    results = Result.objects.filter(event=event).order_by('rank')
    context = {'event': event, 'results': results}
    return render(request, 'session_detail.html', context) 

def results_view(request):
    sessions = Session.objects.all().order_by('day', 'time')
    results = Result.objects.all().order_by('rank')  # Fetch and order sessions
    context = {'sessions': sessions,
               'results': results}
    return render(request, 'results.html', context)

def import_csv(request):
    if request.method == 'POST':
        # ... handle file upload, call import_athletes_from_csv ...
        return redirect('admin:app_label_athlete_changelist')  # Redirect back to Athlete list
    return render(request, 'admin/import_csv.html')  # Render a simple form template

def AthleteListView(request):
    athletes = Athlete.objects.all().order_by('classification')
    context = {'athletes': athletes}
    return render(request, 'athlete_list.html', context)
