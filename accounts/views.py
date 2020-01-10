from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import RegistrationForm


class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
