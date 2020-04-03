from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm, UserChangeForm)
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from apps.accounts.models import CustomUser


class CustomRegistrationForm(UserCreationForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię',
                                                 'autofocus': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.TextInput(attrs={'type': 'email',
                                            'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        password_help_text = self.fields['password1'].help_text
        insert_class = " class='field-help-text'"
        self.fields['password1'].help_text = password_help_text[:3] + insert_class + password_help_text[3:]


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput(render_value=False)}

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists() and email != self.instance.email and email:
            raise ValidationError(_('Użytkownik o podanym adresie email już istnieje, wybierz inny adres'))
        return email

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('first_name') and not cleaned_data.get('last_name') and not cleaned_data.get('email'):
            raise ValidationError(_('Wypełnij co najmniej jedno pole poza hasłem'))
        self.changed_data.remove('password')
        if not self.changed_data:
            raise ValidationError(_('Nie wykryto żadnych zmian!'))

    def save(self, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=self.instance.pk)
        for field in self.changed_data:
            setattr(user, field, self.cleaned_data[field])
        user.save()


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        password_help_text = self.fields['new_password1'].help_text
        insert_class = " class='field-help-text'"
        self.fields['new_password1'].help_text = password_help_text[:3] + insert_class + password_help_text[3:]
        self.fields['old_password'].widget.attrs.pop('autofocus')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password1")
        if old_password == new_password:
            self.add_error('new_password1', _('Nowe hasło musi się róznić od poprzedniego'))


class CustomPasswordResetConfirmForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetConfirmForm, self).__init__(*args, **kwargs)
        password_help_text = self.fields['new_password1'].help_text
        insert_class = " class='field-help-text'"
        self.fields['new_password1'].help_text = password_help_text[:3] + insert_class + password_help_text[3:]


class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_('Podany adres nie jest zarejestrowany na naszej stronie'), code='invalid_email')
        return email
