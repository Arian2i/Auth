from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, OtpLoginForm, CheckOtpForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from random import randint
from .models import Otp, User
from django.utils.crypto import get_random_string
from uuid import uuid4  # creat token in time

# صفحه اصلی
def index(request):
    return render(request, "account/index.html", {})

# لاگین کردن یوزر
class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error("username", "invalid user data")
        else:
            form.add_error("username", "invalid data")

        return render(request, "account/login.html", {'form': form})

# لاگین کردن با کد
class OtpLoginView(View):
    def get(sel, request):
        form = OtpLoginForm()
        return render(request, "account/register.html", {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcod = randint(1000, 9999)
            token = str(uuid4())  # unic token
            Otp.objects.create(phone=cd['phone'], code=randcod, token=token)
            print(randcod)
            return redirect(reverse('account:check_otp') + f'?token={token}')
        else:
            form.add_error("phone", "invalid data")

        return render(request, "account/register.html", {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                # کاربر اگر وجود داشت انرا لاگین کن اگر نه ریجستر
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                otp.delete()    # Delete the otp login number
                
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                
                return redirect('/')

        else:
            form.add_error("phone", "invalid data")

        return render(request, "account/check_otp.html", {'form': form})



def user_logout(request):
    logout(request)
    
    return redirect('/')