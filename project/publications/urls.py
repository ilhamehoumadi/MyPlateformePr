from django.urls import path
from . import views

urlpatterns = [
    # Ajoutez vos patterns d'URL ici
    path('publication/',views.publication,name='publication'),
    path('publications/',views.publications,name='publications'),
]