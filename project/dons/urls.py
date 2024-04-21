from django.urls import path
from . import views

urlpatterns = [
    path('don',views.don,name='don'),
    path('',views.dons,name='dons'),
]
