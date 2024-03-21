import csv
from django.db import models
from datetime import datetime
from django.core.files.base import ContentFile
import io
import base64


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
    gender = models.CharField(max_length=1, choices=(('M', 'Men'), ('W', 'Women'), ('O', 'Other')), default=('O')) 
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        unique_together = ('event_time', 'stage', 'gender') 

    def __str__(self):
        return f'{self.event_name} - {self.gender}'

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField()
    time = models.CharField(max_length=1, choices=(('M', 'Morning'), ('A', 'Afternoon'), ('E', 'Evening')))
    event = models.ManyToManyField(Event)

    class Meta:
        unique_together = ('day', 'time')

    def __str__(self):
        return f'Session - {self.day} - {self.time}' 
    

class Classification(models.Model):
    classification_name = models.CharField(max_length=50, blank=True, null=True)
    classification_code = models.CharField(max_length=10)
    classification_description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.classification_code


class Athlete(models.Model):
    athlete_name = models.CharField(max_length=100)
    bib_number = models.IntegerField()
    best_time_score = models.FloatField(null=True, blank=True)  # Allow for initial null values
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Men'), ('W', 'Women'), ('O', 'Other')))
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    image_profile = models.ImageField(upload_to='athlete_images', blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT) 

    def __str__(self):
        return self.athlete_name
    
    def import_athletes_from_csv(csv_file_path):
        decoded_file = csv_file_path.read().decode('utf-8')  # Decode if necessary
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        for row in reader:

            # Handle potential missing 'Image' field
            # image_profile = row['Image'] if 'Image' in row else None  # Set to None if missing
            if 'Image' in row and row['Image']:
                encoded_string = row['Image']
                img_data = base64.b64decode(encoded_string)
                image_profile = ContentFile(img_data, name=f'{row["Bib No"]}.jpg')
            else:
                image_profile = None

            _classification, _ = Classification.objects.get_or_create(
                classification_code=row['Classification'] if row['Classification'] else 'None'
            )
            athlete, created = Athlete.objects.get_or_create(
                athlete_name=row['Athlete'] + ' ' + row['LastName'],
                bib_number=int(row['Bib No']),
                best_time_score=None,
                birth_date=datetime.strptime(row['DOB'], '%Y-%m-%d').date() if row['DOB'] else None,  # Parse date
                gender=row['Gender'][0],
                classification=_classification,
                country=Country.objects.get(country_code=row['Country']),
                image_profile=image_profile
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
