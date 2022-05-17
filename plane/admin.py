from django.contrib import admin
from plane import models

# Register your models here.
admin.site.register(models.Plane)
admin.site.register(models.MaintenanceRecord)
admin.site.register(models.MaintenanceRecordItem)