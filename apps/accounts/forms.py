from django import forms
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

    def save(self, commit=True):
        user = super(CustomRegistrationForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'email'
        self.fields['username'].widget.attrs['placeholder'] = _('Email')
        self.fields['password'].label = _('Hasło')
        self.fields['password'].widget.attrs['placeholder'] = _('Hasło')


class CustomAdminUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomAdminUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    def save(self, commit=True):
        super(CustomAdminUserChangeForm, self).save(commit=False)
        self.instance.username = self.instance.email
        if commit:
            self.instance.save()
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {'first_name': forms.TextInput(attrs={'autocomplete': 'given-name'}),
                   'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def save(self, *args, **kwargs):
        current_user = self.instance
        user = get_object_or_404(CustomUser, pk=current_user.pk)
        new_email = self.cleaned_data.get('email')
        new_first_name = self.cleaned_data.get('first_name')
        new_last_name = self.cleaned_data.get('last_name')
        if new_email:
            user.email, user.username = new_email, new_email
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name
        user.save()


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        password_help_text = self.fields['new_password1'].help_text
        insert_class = " class='field-help-text'"
        self.fields['new_password1'].help_text = password_help_text[:3] + insert_class + password_help_text[3:]

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
