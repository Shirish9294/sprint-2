from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect

# Create your views here.
from django.template import context

from user.forms import SignUpForm
from user.models import UserProfile


@login_required(login_url='/login')
def index(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    return render(request=request,
                  template_name="user_profile.html")


def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                userprofile = UserProfile.objects.get(user_id=user.id)
                request.session['userimage'] = userprofile.image.url
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login_form.html",
                  context={"form": form})


def signup_form(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/user.png"
            data.save()

            messages.success(request, 'Your account has been created!')
            return redirect('/signup')
        else:
            messages.warning(request, form.errors)
            return redirect('./')

    form = SignUpForm()
    return render(request, 'signup.html', context={'form': form})


def logout_func(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/login')
