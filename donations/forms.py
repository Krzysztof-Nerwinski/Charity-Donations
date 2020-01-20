from django import forms
from django.forms import ModelForm

from donations.models import Category, Institution, Donation


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        exclude = ['user']

