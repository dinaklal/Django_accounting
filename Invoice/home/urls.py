from django.urls import path

from . import views


urlpatterns = [
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('add_site',views.add_site,name='add_site'),
    path('view_site',views.view_site,name='view_site'),
    path('process',views.process,name='process'),
    path('GeneratePdf',views.GeneratePdf,name='GeneratePdf'),
    path('get_invoice',views.get_invoice,name='get_invoice'),
    path('edit_inv',views.edit_inv,name='edit_inv'),
    path('save_inv',views.save_inv,name='save_inv'),
    path('edit_inv_date',views.edit_inv_date,name='edit_inv_date'),
    
]
