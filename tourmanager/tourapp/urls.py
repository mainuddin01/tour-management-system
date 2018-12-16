from django.conf.urls import url

from .views import ( TourListView, TourDetailView, TourUpdateView, ExpenseListView, ExpenseDetailView, ExpenseUpdateView,
                    expense_delete_view, tour_start_view, tour_end_view )

app_name = 'tourapp'

urlpatterns = [
    url(r'^$', TourListView.as_view(), name='tour_list'),
    url(r'^(?P<pk>\d+)/$', TourDetailView.as_view(), name='tour_detail'),
    url(r'^(?P<pk>\d+)/edit/$', TourUpdateView.as_view(), name='tour_edit'),
    url(r'^(?P<pk>\d+)/start/$', tour_start_view, name='tour_start'),
    url(r'^(?P<pk>\d+)/end/$', tour_end_view, name='tour_end'),
    url(r'^(?P<pk>\d+)/expense/$', ExpenseListView.as_view(), name='expense_list'),
    url(r'^(?P<pk>\d+)/expense/(?P<id>\d+)/$', ExpenseDetailView.as_view(), name='expense_detail'),
    url(r'^(?P<pk>\d+)/expense/(?P<id>\d+)/update/$', ExpenseUpdateView.as_view(), name='expense_update'),
    url(r'^(?P<pk>\d+)/expense/(?P<id>\d+)/delete/$', expense_delete_view, name='expense_delete'),
]
