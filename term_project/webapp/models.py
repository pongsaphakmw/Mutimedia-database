from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    country_flag_image = models.ImageField(upload_to='country_flags')  # Specify upload path

    def __str__(self):
        return self.country_name

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    stage = models.CharField(max_length=50)  

    def __str__(self):
        return self.event_name

class Session(models.Model):
    day = models.DateField()
    time = models.TimeField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'))) 
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event.event_name} - {self.day}'

class Athlete(models.Model):
    athlete_name = models.CharField(max_length=100)
    bib_number = models.IntegerField()
    best_time_score = models.FloatField(null=True, blank=True)  # Allow for initial null values
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    classification = models.CharField(max_length=50, blank=True)  # Optional classification
    image_profile = models.ImageField(upload_to='athlete_images', blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT) 

    def __str__(self):
        return self.athlete_name

class Result(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    rank = models.IntegerField()
    result = models.CharField(max_length=50) 
    score = models.FloatField()
    medal = models.CharField(max_length=10, choices=(('Gold', 'Gold'), ('Silver', 'Silver'), 
                                                   ('Bronze', 'Bronze'), ('None', 'None')))
    
    def __str__(self):
        return f'{self.athlete.athlete_name} - {self.session.day} - {self.rank}'
