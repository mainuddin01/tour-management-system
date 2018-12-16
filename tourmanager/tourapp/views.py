from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Tour, TourExpense
from .forms import TourForm, TourExpenseForm, TourExpenseFormSet

# Create your views here.
class AboutPage(TemplateView):
    template_name = 'about-us.html'

class HomePage(View):

    def get(self, request, *args, **kwargs):
        try:
            tour_pk = Tour.objects.filter(user=request.user, start=True, end=False).first()
            expense_list = TourExpense.objects.filter(tour=tour_pk).all()
            # user = request.user
            recent_tour = Tour.objects.filter(user=request.user).first()
        except:
            expense_list = None
            recent_tour = None
        tour_form = TourForm()
        expense_form = TourExpenseForm()
        expense_form_set = TourExpenseFormSet(queryset=expense_list)
        try:
            current_users_tour = Tour.objects.filter(user=request.user)
            users_current_tour = current_users_tour.filter(start=True, end=False).first()
        except:
            users_current_tour = None
        context = {
            'tour_form': tour_form,
            'expense_form': expense_form,
            'expense_form_set': expense_form_set,
            'recent_tour': recent_tour,
            'users_current_tour': users_current_tour
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        tour_form = TourForm(request.POST)
        expense_form = TourExpenseForm(request.POST)
        expense_form_set = TourExpenseFormSet(request.POST, request.FILES)
        try:
            recent_tour = Tour.objects.filter(user=request.user).first()
            current_users_tour = Tour.objects.filter(user=request.user)
            users_current_tour = current_users_tour.filter(start=True, end=False).first()
        except:
            recent_tour = None
            users_current_tour = None
        if tour_form.is_valid():
            new_tour = tour_form.save(commit=False)
            new_tour.user = request.user
            new_tour.save()
            return HttpResponseRedirect(reverse('home'))

        if expense_form.is_valid():
            new_expense = expense_form.save(commit=False)
            try:
                current_users_tour = Tour.objects.filter(user=request.user)
                users_current_tour = current_users_tour.filter(start=True, end=False).first()
            except:
                raise Http404
            new_expense.tour = users_current_tour
            new_expense.save()

        if expense_form_set.is_valid():
            expense_form_set.save(commit=False)
            for expense_item in expense_form_set:
                new_item = expense_item.save(commit=False)
                if new_item.spent_on:
                    tour = Tour.objects.filter(user=request.user, start=True, end=False).first()
                    new_item.tour = tour
                    new_item.save()

        context = {
            'tour_form': tour_form,
            'expense_form': expense_form,
            'expense_form_set': expense_form_set,
            'recent_tour': recent_tour,
            'users_current_tour': users_current_tour
        }

        return render(request, 'index.html', context)


class TourListView(LoginRequiredMixin,ListView):
    model = Tour

    def get_queryset(self, *args, **kwargs):
        return Tour.objects.filter(user=self.request.user)


class TourDetailView(LoginRequiredMixin, DetailView):
    model = Tour

    def get_object(self, *args, **kwargs):
        obj_instance = super(TourDetailView, self).get_object(*args, **kwargs)
        if obj_instance.user != self.request.user:
            raise Http404
        else:
            return obj_instance


class TourUpdateView(LoginRequiredMixin, UpdateView):
    model = Tour
    form_class = TourForm

    def get_object(self, *args, **kwargs):
        obj_instance = super(TourUpdateView, self).get_object(*args, **kwargs)
        if obj_instance.user != self.request.user:
            raise Http404
        else:
            return obj_instance



class ExpenseListView(LoginRequiredMixin, ListView):
    model = TourExpense

    def get_queryset(self, *args, **kwargs):
        queryset = super(ExpenseListView, self).get_queryset(*args, **kwargs)
        tour = self.kwargs.get("pk")
        tour_expense_list = queryset.filter(tour=tour)
        return tour_expense_list


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = TourExpense

    def get_object(self, *args, **kwargs):
        tour_pk = self.kwargs.get("pk")
        expense_id = self.kwargs.get("id")
        # expense_object = self.model.objects.get(id=expense_id, tour=tour_pk)
        expense_object = get_object_or_404(self.model, id=expense_id, tour=tour_pk)
        return expense_object

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = TourExpense
    form_class = TourExpenseForm
    template_name = 'index.html'

    def get_object(self, *args, **kwargs):
        tour_pk = self.kwargs.get("pk")
        expense_id = self.kwargs.get("id")
        expense_object = get_object_or_404(self.model, id=expense_id, tour=tour_pk)
        return expense_object

# class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
#     model = TourExpense
#     success_url = reverse_lazy('home')

    # def get_object(self, *args, **kwargs):
    #     tour_pk = self.kwargs.get("pk")
    #     expense_id = self.kwargs.get("id")
    #     expense_object = get_object_or_404(TourExpense, id=expense_id, tour=tour_pk)
    #     return expense_object

def tour_start_view(request, *args, **kwargs):
    tour_pk = kwargs.get('pk')
    tour_instance = get_object_or_404(Tour, id=tour_pk)
    tour_instance.start_tour()
    return HttpResponseRedirect(reverse('home'))

def tour_end_view(request, *args, **kwargs):
    tour_pk = kwargs.get('pk')
    tour_instance = get_object_or_404(Tour, id=tour_pk)
    tour_instance.end_tour()
    return HttpResponseRedirect(reverse('home'))


def expense_delete_view(request, *args, **kwargs):
    tour_pk = kwargs.get("pk")
    expense_id = kwargs.get("id")
    expense_object = get_object_or_404(TourExpense, id=expense_id, tour=tour_pk)
    expense_object.delete()
    return HttpResponseRedirect(reverse('home'))
