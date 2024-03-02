from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Result, Athlete

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

    actions = ['import_from_csv']

    def import_from_csv(self, request, queryset):
        if 'csv_file' in request.FILES:
            # Temporary file handling (adjust as needed)
            temp_file = request.FILES['csv_file'].temporary_file_path()
            Athlete.import_athletes_from_csv(temp_file)
            self.message_user(request, "Import completed")
        else:
            self.message_user(request, "Please select a CSV file to upload")
    
class CountryAdminView(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')