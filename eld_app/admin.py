from django.contrib import admin

from eld_app.models import Driver, Vehicle, ELD

# Register your models here.
admin.site.register(Driver)
admin.site.register(ELD)
admin.site.register(Vehicle)
