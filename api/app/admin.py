from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from . import models

TokenAdmin.raw_id_fields = ['user']

# Register your models here.
admin.site.register(models.Holiday)
