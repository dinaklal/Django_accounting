from django.urls import path

from . import views


urlpatterns = [
    path('add_company',views.add_company,name='add_company'),
    path('add_de_note',views.add_de_note,name='add_de_note'),
   
    ]
