from django.contrib import admin

from .models import *

admin.site.register(RepresentativeModel)
admin.site.register(ComplaintModel)
admin.site.register(DataControllerModel)
admin.site.register(RemedialMeasuresModel)
admin.site.register(DataBreachModel)
