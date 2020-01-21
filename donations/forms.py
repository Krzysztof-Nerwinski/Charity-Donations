from django import forms
from django.forms import ModelForm

from donations.models import Category, Institution, Donation


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'

        widgets = {
            'categories': forms.CheckboxSelectMultiple,
            'address': forms.TextInput(attrs={'placeholder': 'np. Marszałkowska 111/15'}),
            'city': forms.TextInput(attrs={'placeholder': 'np. Warszawa'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'w formacie XX-XXX'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'np. 123-456-789'}),
            'pick_up_date': forms.TextInput(attrs={'type': 'date'}),
            'pick_up_time': forms.TextInput(attrs={'type': 'time'}),
            'pick_up_comment': forms.Textarea(attrs={'rows': '5'}),
        }
