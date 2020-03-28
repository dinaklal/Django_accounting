from django.urls import path

from . import views


urlpatterns = [
    path('add_company',views.add_company,name='add_company'),
    path('add_de_note',views.add_de_note,name='add_de_note'),
    path('add_rate',views.add_rate,name='add_rate'),
    path('trip_sheet',views.trip_sheet,name='trip_sheet'),
    path('print_tripsheet',views.print_tripsheet,name='print_tripsheet'),
    path('view_company',views.view_company,name='view_company'),
    path('edit_del_note',views.edit_del_note,name='edit_del_note'),
    path('add_de_note2',views.add_de_note2,name='add_de_note2'),
    path('edit_del3',views.edit_del3,name='edit_del3'),
    path('print_tripsheet_inv',views.print_tripsheet_inv,name='print_tripsheet_inv'),
    path('view_money',views.view_money,name='view_money'),
    path('view_money_2',views.view_money_2,name='view_money_2'),
   
    ]
