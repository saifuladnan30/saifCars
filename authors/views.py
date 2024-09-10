from django.shortcuts import render,redirect
from .forms import Register, ChangeUserData
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from cars.models import PostCar,Purchase
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
# Create your views here.


@login_required
def profile(request):
    data = PostCar.objects.filter(author = request.user)
    user_purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'profile.html', {'data':data, 'user_purchases': user_purchases})
    
@login_required
def update_profile(request):
        if request.method == 'POST':
            form = ChangeUserData(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account Updated Successfully')
                return redirect('profile')
        else:
            form = ChangeUserData(instance=request.user)
        return render(request, 'update_profile.html', {'form':form})


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = Register(request.POST)
            if form.is_valid():
                messages.success(request, 'Account created Successfully')
                form.save()
                return redirect('signin')
        else:
            form = Register()
        return render(request, 'signup.html', {'form':form})
    else:
        return redirect('profile')

class SignIn(LoginView):
    template_name = 'signin.html'
    
    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Loggedin Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context



class SignOut(LogoutView):
    def get_success_url(self):
        return reverse_lazy('cars')

@login_required
def change_pass(request):
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password Updated Successfully')
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'pass_change.html', {'form':form})

@login_required
def new_pass(request):
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password added Successfully')
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request, 'pass_change.html', {'form':form})
