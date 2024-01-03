from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.views.decorators.csrf import csrf_protect


def Index(request):
    return render(request, 'index.html')

# User Registration                                  

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2: # check pws1 and pws2 both are same or not
            if User.objects.filter(username=username).exists(): # username is already exists or not
                messages.info(request, 'User Name is Taken..!!')
                return redirect('Register')
            else:
                user_form = User.objects.create_user(username=username, password=password1, email=email)
                user_form.save()
                user_id = User.objects.get(
                    username=username).pk  # get registerd user id
                profile_form = UserProfile(user_id=user_id)
                profile_form.save()
                messages.info(
                    request, 'User Registration Successfuly Now You Can Login..!!')
                return redirect('Login')
        else:
            messages.info(request, 'Password Not Matching..!!')
            return redirect('Register')
    else:
        return render(request, 'registration.html')

# User Login

def Login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        user = auth.authenticate(username=username_or_email, password=password)
        
        # If authentication fails using the username, try with the email
        if user is None:
            try:
                user = User.objects.get(email=username_or_email)
                user = auth.authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                pass


        if user is not None:
            auth.login(request, user)
            args = {'user': request.user}
            messages.info(request, 'User Login Successfuly..!!')
            return render(request, 'UserLogin.html', args)
        else:
            messages.info(request, 'Invelid Credentials..!!')
            return redirect('Login')
    else:
        return render(request, 'login.html')

# user Logout
@csrf_protect
@login_required
def LogoutForm(request):
    auth.logout(request)
    messages.info(request, 'User Logout Successfuly..!!')
    return render(request, 'index.html')

# user Edit Profile

@login_required
def EditProfile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Upadet Profile Successfuly..!!')
            return render(request, 'UserLogin.html')
    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'EditProfile.html', args)

# User Change Password

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'Change Password Successfuly..!!')
            return render(request, 'UserLogin.html')
        else:
            messages.info(request, 'Please Enter Given Formate Password..!!')
            return redirect('ChangePassword')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'changepassword.html', args)
