from django.urls import path

from . import views


urlpatterns = [
   path('report',views.report,name='report'),
   path('add_money',views.add_money,name='add_money'),
   path('summary',views.summary,name='summary'),
   path('add_start',views.add_start,name='add_start'),
   path('print_account',views.print_account,name='print_account'),
    
]
