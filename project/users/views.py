from django.views.generic import TemplateView 
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from users.models import User ###########
from .models import Admin, Donor, Association ###########
#from paypal.standard.forms import PayPalPaymentsForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
import codecs
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponseForbidden
#
class HomeView(TemplateView):
    template_name = 'users/home.html'

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'users/profile.html'
    # LoginRequiredMixin : pour restreindre l'accès à une vue en utilise 



#register en tant que Donor
def DonorSignup(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        telephone = request.POST.get('telephone', None)
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Entrez un email valide !'})

        if password != repassword:
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})
        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_donor = True
        utilisateur.is_association = False
        utilisateur.is_admin=False
        utilisateur.save()

        # Create a donor associated with the user
        donor = Donor.objects.create(
            user=utilisateur,
            phone_number=telephone,  
        )
        donor.save()
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboard_donor')

    return render(request, 'users/registerdonor.html', {'error': False, 'message': ''})

#login en tant que Donor
def DonorSignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_donor:
                return redirect('dashboard_donor')
            elif user.is_association:
                return redirect('dashboard_association')
            else:
                return redirect('dashboardAdmin')
    return render(request, 'users/Logindonor.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})
        

@login_required(login_url="")
def dashboard_donor(request):
    user = request.user
    donor = Donor.objects.filter(user=user).first()
    return render(request, 'users/dashboard_donor.html', {'donor': donor})


def donors(request):
    user = request.user
    admin = Admin.objects.filter(user=user).first()
    donors=Donor.objects.all()
    associations=Association.objects.all()
    context ={
        'admin': admin,
        'donors': donors,
        'associations':associations,
        
    }
    return render (request,'users/donors.html',context)
 


#####################/ Donor /#############################

##################### Association #########################
#register en tant que Association
def AssociationSignup(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        telephone = request.POST.get('telephone', None)
        stat_juridique=request.POST.get('stat_juridique',None)
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Entrez un email valide !'})

        if password != repassword:
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})
        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=name, email=email, password=password, first_name=name)
        utilisateur.is_association = True
        utilisateur.is_donor=False
        utilisateur.is_admin=False
        utilisateur.save()

        # Create a association associated with the user
        association = Association.objects.create(
            user=utilisateur,
            phone_number=telephone,
            stat_juridique=stat_juridique,  
        )
        association.save()
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboard_association')

    return render(request, 'users/registerassociation.html', {'error': False, 'message': ''})

#login en tant que Association
def AssociationSignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_donor:
                return redirect('dashboard_donor')
            elif user.is_association:
                return redirect('dashboard_association')
            else:
                return redirect('dashboardAdmin')
    return render(request, 'users/Loginassociation.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})
        

@login_required(login_url="")
def dashboard_association(request):
    user = request.user
    association = Association.objects.filter(user=user).first()
    return render(request, 'users/dashboard_association.html', {'association': association})


def associations(request):
    user = request.user
    admin = Admin.objects.filter(user=user).first()
    donors=Donor.objects.all()
    associations=Association.objects.all()
    context ={
        'admin': admin,
        'donors': donors,
        'associations':associations,
        
    }
    return render (request,'users/associations.html',context)
 
#####################/ Association /#############################

###################  admin  ####################
def signupadmin(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        photo = request.FILES.get('image', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
       

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Entrez un email valide !!!!!'})

        if password != repassword:
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})

        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_donor = False
        utilisateur.is_association = False
        utilisateur.is_admin=True
        utilisateur.save()


         # Create a admin associated with the user
        admin = Admin.objects.create(
            user=utilisateur,
            
        )
        admin.image=photo
        admin.save()
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboardAdmin')

    return render(request, 'users/adminregister.html', {'error': False, 'message': ''})


@login_required(login_url="")
def dashboardAdmin(request):
    user = request.user
    admin = Admin.objects.filter(user=user).first()
    donors=Donor.objects.all()
    associations=Association.objects.all()

    context = {
        'admin': admin,
        'donors': donors,
        'associations': associations,
    }
    return render(request, 'users/dashboardAdmin.html', context)
###################### / admin  / ##################












###################### Ancien   #############################
#class MyLoginView(LoginView):
#    template_name='users/registration/login.html'
#    redirect_authenticated_user= False #login in next time directly

#    def get_success_url(self):
#        messages.info(self.request, 'Welcome in your profile')
#        return reverse_lazy('profile')
#    
#    def form_invalid(self, form):
#        messages.error(self.request, 'error username or password') # keep the error abstract don't specifie
#        return self.render_to_response(self.get_context_data(form=form))
        

#########  se déconnecter ##############
def custom_logout(request):
    print('Logging out {}'.format(request.user))
    logout(request)
    print(request.user)
    return HttpResponseRedirect('/')  #direction  home