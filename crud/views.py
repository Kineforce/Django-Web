from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import RegistrationForm, AccountAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Account
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import time
User = get_user_model()


#from django.http import HttpResponseRedirect
#from django.contrib.auth import login
# Create your views here.

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


def view_404(request, exception=None):
    return redirect('/')

def home(request):
    #queryset = get_current_users()
    #online_users = [item.username for item in queryset]
    #print(online_users)
    #print(queryset.values('username') [0]['username'] )
    return render(request, 'crud/home.html')

def about(request):
    return render(request, 'crud/about.html')

@login_required()
def profile(request):
    queryset = get_current_users()
    online_users = [item.username for item in queryset]

    names = {
        'name': online_users
    }
    return render(request, 'crud/profile.html', names)

def sign_up(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #email = form.cleaned_data.get('email')
            #raw_password = form.cleaned_data.get('password1')
            #account = authenticate(email=email, password=raw_password)
            #login(request, account)
            #result = "Cadastrado com sucesso!"
            #return redirect('/')
            return render(request, 'crud/result.html', {'result': "Cadastrado com sucesso!"})
        else:
            context['registration_form'] = form
            #result = "Email já cadastrado!"
            #return render(request, 'crud/result.html', {'result': result})
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'crud/signup.html', context)

    #return render(request, 'crud/signup.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('/')

def sign_in(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("/profile")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            raw_password = request.POST['password']
            user = authenticate(email=email, password=raw_password)

            if user:
                login(request, user)
                return redirect("/profile")
    else:
        form = AccountAuthenticationForm()

    context['signin_form'] = form
    return render(request, 'crud/signin.html', context)
    

