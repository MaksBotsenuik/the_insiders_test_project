from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm

# Create your views here.

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
