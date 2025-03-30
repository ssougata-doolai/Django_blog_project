from django.shortcuts import render, redirect, get_object_or_404
from . forms import (
    UserCreationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    EmailVerificationForm,
    PasswordResetForm,
    OtpVerificationForm)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse,  HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from . models import Profile
from django.urls import reverse
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'users/registration.html',{'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('user-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)


def user_profile(request,username):
    user = get_object_or_404(User,username=(username))
    prof = user.profile
    return render(request,'users/user_profile1.html',{'prof':prof})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


def send_verification_mail(request):
    if request.method == 'POST':
        context = {}
        form = EmailVerificationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            receiver_mail = form.cleaned_data.get('email')

            print("mail == ",receiver_mail)
            send_mail(
                'hii',
                'this is message',
                settings.EMAIL_HOST_USER,
                [receiver_mail],
                fail_silently = False,
            )
            messages.success(request,f'A conformation mail has been sent to your registered email id')
    else:
        form = EmailVerificationForm(request.POST)
        context = {
            'form':form
        }
    return render(request,'users/email_verification_form.html',context)

def send_password_reset_mail(request):
    if request.method == 'POST':
        context = {}
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username__iexact=username).exists():
                obj = get_object_or_404(User,username__iexact=username)
                otp = randint(111111,999999)
                receiver_mail = obj.email
                obj.profile.otp = otp
                obj.save()
                print("Otp = ",obj.profile.otp)
                message = 'your one time password is '+str(otp)
                send_mail(
                    'hii',
                    message,
                    settings.EMAIL_HOST_USER,
                    [receiver_mail],
                    fail_silently = False,
                )
                form = OtpVerificationForm()
                context = {'form':form,'username':username}
                messages.success(request,f'A conformation mail has been sent to your registered email id')
                return render(request,'users/verify_otp.html',context);
            else:
                context = {'form':form}
                messages.success(request,f'Invalid username')
                return render(request,'users/password_reset_form.html',context)
    else:
        form = PasswordResetForm()
        context = {'form':form}
        return render(request,'users/password_reset_form.html',context)

def verify_otp(request):
    if request.method == 'POST':
        context = {}
        form = OtpVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            otp = int(otp)
            username = request.POST.get('username')
            print("Username = ",username)
            obj = get_object_or_404(User,username__iexact=username)
            p_otp = obj.profile.otp
            print("otp = ",otp,"p_otp = ",p_otp)
            if p_otp == otp:
                return HttpResponseRedirect(reverse('blogs:blogs-index'))
            else:
                form = OtpVerificationForm()
                context = {'form':form,'username':username}
                return render(request,'users/verify_otp.html',context);


def user_account(request):
    return render(request,'users/user_account.html',{})
