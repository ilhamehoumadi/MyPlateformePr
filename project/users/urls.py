from django.urls import path
from .views import HomeView,ProfileView 
from .views import custom_logout 
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    # Ajoutez vos patterns d'URL ici
    path('home/', HomeView.as_view() , name="home"),
    path('profile/', ProfileView.as_view() , name="profile"),
    #path('login/', MyLoginView.as_view() , name="login"),
    #path('register/', RegisterView.as_view() , name="register"),
    path('logout/', custom_logout, name='logout'),


    path('registerdonor/', views.DonorSignup, name='registerdonor'),
    path('Logindonor/', views.DonorSignIn, name='Logindonor'),
    path('dashboard_donor/', views.dashboard_donor, name='dashboard_donor'),

    path('registerassociation/', views.AssociationSignup, name='registerassociation'),
    path('Loginassociation/', views.AssociationSignIn, name='Loginassociation'),
    path('dashboard_association/', views.dashboard_association, name='dashboard_association'),

    path('signupadmin/', views.signupadmin, name='signupadmin'),
    path('dashboardAdmin/',views.dashboardAdmin,name='dashboardAdmin'),

    path('donors/',views.donors,name='donors'),
    path('associations/',views.associations,name='associations'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)