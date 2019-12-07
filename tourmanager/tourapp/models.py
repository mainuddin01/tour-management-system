from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from decimal import Decimal

# Create your models here.
class Tour(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    tour_location = models.CharField(max_length=220)
    total_budget = models.DecimalField(max_digits=20, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)

    def start_tour(self):
        if not self.start:
            self.start = True
            self.save()

    def end_tour(self):
        if not self.end & self.start:
            self.end = True
            self.save()

    def get_total_expenses(self):
        total_expense = 0.00
        for expense in self.tourexpense_set.all():
            total_expense = Decimal(total_expense) + expense.amount
        return total_expense

    def get_remaining_balance(self):
        if self.get_total_expenses():
            remaining_balance = self.total_budget - self.get_total_expenses()
            return remaining_balance

    def get_absolute_url(self):
        return reverse('tourapp:tour_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.tour_location


class TourExpense(models.Model):
    tour = models.ForeignKey(Tour)
    spent_on = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    spent_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta():
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse('tour_app:expense_detail', kwargs={'pk': self.tour.pk, 'id': self.pk})

    def __str__(self):
        return self.spent_on
