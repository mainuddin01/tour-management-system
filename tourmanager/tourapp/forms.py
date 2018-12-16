from django import forms
from django.forms.models import modelformset_factory
from django.conf import settings

from .models import Tour, TourExpense

class TourForm(forms.ModelForm):
    tour_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    total_budget = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))

    class Meta():
        fields = ('tour_location', 'total_budget', 'start_date', 'end_date')
        model = Tour


# class TourExpenseForm(forms.ModelForm):
#     spent_on = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
#     amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
#
#     class Meta():
#         fields = ('spent_on', 'description', 'amount')
#         model = TourExpense

class TourExpenseForm(forms.ModelForm):
    spent_on = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta():
        fields = ('spent_on', 'description', 'amount')
        model = TourExpense

TourExpenseFormSet = modelformset_factory(TourExpense, form=TourExpenseForm, extra=1)

