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
    athlete_medals = []
    for athlete in athletes:
        athlete_medal = {'athlete': athlete.athlete_name, 
                        'gold_medals': Result.objects.filter(athlete=athlete, medal='Gold').count(),
                        'silver_medals': Result.objects.filter(athlete=athlete, medal='Silver').count(), 
                        'bronze_medals': Result.objects.filter(athlete=athlete, medal='Bronze').count(),
                        'total_medals': Result.objects.filter(athlete=athlete).count(),
                        'athlete_info': athlete}
        athlete_medals.append(athlete_medal)
        # print(f'{athlete} = {athlete_medal["athlete"]}')
    # for i in athlete_medals:
    #     print(i['athlete'], i['gold_medals'], i['silver_medals'], i['bronze_medals'])
    context = {'athletes': athletes, 'athlete_medals': athlete_medals}
    return render(request, 'athlete_list.html', context)

def AthleteDetailView(request, bib_number):
    athlete = get_object_or_404(Athlete, bib_number=bib_number)
    
    athlete_medal = {'athlete': athlete.athlete_name, 
                    'gold_medals': Result.objects.filter(athlete=athlete, medal='Gold').count(),
                    'silver_medals': Result.objects.filter(athlete=athlete, medal='Silver').count(), 
                    'bronze_medals': Result.objects.filter(athlete=athlete, medal='Bronze').count(),
                    'total_medals': Result.objects.filter(athlete=athlete).count(),
                    'athlete_info': athlete}
    results = Result.objects.filter(athlete=athlete).order_by('event')
    context = {'athlete': athlete, 'results': results, 'athlete_medal': athlete_medal}
    return render(request, 'athlete_detail.html', context)

def medalView(request):
    countries = Country.objects.all()
    country_medals = []
    for country in countries:
        athletes = Athlete.objects.filter(country=country)
        country_medal = {
            'country': country.country_name,
            'gold_medals': Result.objects.filter(athlete__in=athletes, medal='Gold').count(),
            'silver_medals': Result.objects.filter(athlete__in=athletes, medal='Silver').count(),
            'bronze_medals': Result.objects.filter(athlete__in=athletes, medal='Bronze').count(),
            'total_medals': Result.objects.filter(athlete__in=athletes).count(),
        }
        country_medals.append(country_medal)
    context = {'country_medals': country_medals}
    return render(request, 'medal.html', context)