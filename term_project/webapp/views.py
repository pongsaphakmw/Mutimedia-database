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


def session_detail_view(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    results = Result.objects.filter(session=session).order_by('rank')
    context = {'session': session, 'results': results}
    return render(request, 'session_detail.html', context) 