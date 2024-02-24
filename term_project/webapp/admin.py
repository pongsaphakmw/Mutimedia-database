from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Country)
admin.site.register(Athlete)
admin.site.register(Event)
admin.site.register(Session)
admin.site.register(Result)