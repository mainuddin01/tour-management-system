from django.contrib import admin

from .models import Tour, TourExpense

# Register your models here.
admin.site.register(Tour)

admin.site.register(TourExpense)
