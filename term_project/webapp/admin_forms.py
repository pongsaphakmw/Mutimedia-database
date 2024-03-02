from django.contrib import admin
from .models import Result

class ResultInline(admin.TabularInline):  # For inline editing
    model = Result

class ResultAdminForm(admin.ModelAdmin):
    list_display = ('athlete', 'event', 'rank', 'result', 'medal')
    search_fields = ('event__event_name', 'athlete__athlete_name', 'rank', 'result', 'medal')
    list_filter = ('event', 'medal')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_time', 'stage',)
    search_fields = ('event_name', 'event_time', 'stage')
    list_filter = ('stage', 'start_datetime')

    inlines = [ResultInline]

class SessionAdminView(admin.ModelAdmin):
    search_fields = ('id','gender', 'day', 'time', 'event')
    list_filter = ('id','gender', 'day', 'time')
    list_display = ('day', 'display_events', 'time', 'gender')

    def display_events(self, obj):
        return ", ".join([event.event_name for event in obj.event.all()])

    display_events.short_description = 'Events' 

class AthleteAdminView(admin.ModelAdmin):
    list_display = ('athlete_name', 'bib_number', 'country', 'gender')
    search_fields = ('athlete_name', 'bib_number', 'country', 'gender')
    list_filter = ('country', 'gender')
    
class CountryAdminView(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')