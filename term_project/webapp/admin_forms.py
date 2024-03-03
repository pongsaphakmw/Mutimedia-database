from django.contrib import admin
from django.http import HttpRequest
from .models import Result, Athlete, Event
from django.urls import path
from django.shortcuts import render, redirect
from django import forms

class ResultInline(admin.TabularInline):  # For inline editing
    model = Result

    def clean(self):
        for form in self.cleaned_data:
            event = form.cleaned_data.get('event')  # Access the event from the form
            athlete = form.cleaned_data.get('athlete')  # Access the athlete from the form
            if event and athlete and event.gender != athlete.gender:
                raise forms.ValidationError('Athlete gender must match the selected event gender.')
        return super().clean()

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class ResultAdminForm(admin.ModelAdmin):
    list_display = ('athlete', 'event', 'rank', 'result', 'medal')
    search_fields = ('event__event_name', 'athlete__athlete_name', 'rank', 'result', 'medal')
    list_filter = ('event', 'medal')

    def save_model(self, request, obj, form, change):
        if obj.event and obj.athlete.gender != obj.event.gender:
            raise forms.ValidationError('Athlete gender must match event gender.', code='invalid')
        super().save_model(request, obj, form, change)


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'gender','event_time', 'stage')
    search_fields = ('event_name', 'event_time', 'stage', 'gender')
    list_filter = ('stage', 'start_datetime', 'gender')

    inlines = [ResultInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)  # Save results without saving to database yet

        for obj in formset.deleted_objects:
            obj.delete()

        for instance in instances:
            if instance.event and instance.athlete.gender != instance.event.gender:
               instance.add_error('athlete', forms.ValidationError('Athlete gender must match event gender.'))
            instance.save()  # Save each validated result instance

        formset.save_m2m()

class SessionAdminView(admin.ModelAdmin):
    search_fields = ('id', 'day', 'time', 'event')
    list_filter = ('id', 'day', 'time')
    list_display = ('day', 'display_events', 'time')

    def display_events(self, obj):
        return ", ".join([event.event_name for event in obj.event.all()])

    display_events.short_description = 'Events' 

class AthleteAdminView(admin.ModelAdmin):
    list_display = ('athlete_name', 'bib_number', 'country', 'gender')
    search_fields = ('athlete_name', 'bib_number', 'country', 'gender')
    list_filter = ('country', 'gender')

    actions = ['import_from_csv']

    change_list_template = 'admin/import_csv.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_from_csv),
        ]
        return my_urls + urls
    
    def import_from_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            # reader = csv.reader(csv_file)
            Athlete.import_athletes_from_csv(csv_file)
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    
class CountryAdminView(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')