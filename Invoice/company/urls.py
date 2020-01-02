from django.urls import path

from . import views


urlpatterns = [
    path('add_company',views.add_company,name='add_company'),
    path('add_de_note',views.add_de_note,name='add_de_note'),
    path('add_rate',views.add_rate,name='add_rate'),
    path('trip_sheet',views.trip_sheet,name='trip_sheet'),
    path('print_tripsheet',views.print_tripsheet,name='print_tripsheet'),
    path('view_company',views.view_company,name='view_company'),
   
    ]
