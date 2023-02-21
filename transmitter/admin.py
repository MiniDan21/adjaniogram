from django.contrib import admin

# Register your models here.
from .models import Order, Service


admin.site.register([Order, Service])
