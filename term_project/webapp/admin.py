from django.contrib import admin
from .models import *
from .admin_forms import *


# Register your models here.
admin.site.register(Country, CountryAdminView)
admin.site.register(Athlete, AthleteAdminView)
admin.site.register(Event, EventAdmin)
admin.site.register(Session, SessionAdminView)
admin.site.register(Result, ResultAdminForm)
admin.site.register(Classification)


# @admin.register(Athlete)
# class AthleteImport(ImportExportModelAdmin):
#     pass