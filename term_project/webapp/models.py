import csv
from django.db import models
from datetime import datetime


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    country_flag_image = models.ImageField(upload_to='country_flags')  # Specify upload path

    def __str__(self):
        return self.country_name

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    event_time = models.TimeField()
    stage = models.CharField(max_length=50) 
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        unique_together = ('event_time', 'stage') 

    def __str__(self):
        return self.event_name

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField()
    time = models.CharField(max_length=1, choices=(('M', 'Morning'), ('A', 'Afternoon'), ('E', 'Evening')))
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'))) 
    event = models.ManyToManyField(Event)

    class Meta:
        unique_together = ('day', 'time', 'gender')

    def __str__(self):
        return f'Session - {self.day} - {self.time}' 
    

class Classification(models.Model):
    classification_name = models.CharField(max_length=50)
    classification_code = models.CharField(max_length=10)
    classification_description = models.TextField(blank=True)
    
    def __str__(self):
        return self.classification_code


class Athlete(models.Model):
    athlete_name = models.CharField(max_length=100)
    bib_number = models.IntegerField()
    best_time_score = models.FloatField(null=True, blank=True)  # Allow for initial null values
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    image_profile = models.ImageField(upload_to='athlete_images', blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT) 

    def __str__(self):
        return self.athlete_name
    
    def import_athletes_from_csv(csv_file_path):
        with open(csv_file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                athlete, created = Athlete.objects.get_or_create(
                    athlete_name=row['Athlete'] + row['LastName'],
                    bib_number=int(row['Bib No']),
                    best_time_score=None,
                    birth_date=row['DOB'],
                    gender=row['Gender'],
                    classification=Classification.objects.get(classification_code=row['Classification']), # Not sure
                    country=Country.objects.get(country_code=row['Country'])
                )
                if not created:  # Handle updates, if desired
                    print(f"Athlete {athlete.athlete_name} might need an update")
    

class Result(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rank = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=50, default='On Going') 
    score = models.FloatField(blank=True, null=True)
    medal = models.CharField(max_length=10, choices=(('Gold', 'Gold'), ('Silver', 'Silver'), 
                                                   ('Bronze', 'Bronze'), ('None', 'None')), default='None')
    
    def __str__(self):
        return f'{self.event.event_name} - {self.athlete.athlete_name} - {self.medal}'
