from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# Create your views here.

def login_form(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login( request,user)
                return redirect('index')
            
            form.add_error(None, "Неправильное имя или пароль, LOL!")
    else:
        form= LoginForm()

    context = {
        'form': form
    }

    return render(request, 'login.html', context)