from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from accounts.forms import CustomRegistrationForm, UserChangeForm, CustomPasswordChangeForm
from donations.models import Donation


class SignUp(generic.CreateView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            donations = Donation.objects.filter(user=request.user).order_by('is_taken', 'pick_up_date',
                                                                            'pick_up_time', 'quantity')
            return render(request, 'user_site.html', {'donations': donations})
        else:
            raise Http404('Użytkownik podany w sesji nie jest zalogowany')


class ProfileChangeView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_form = UserChangeForm(instance=user)
            password_form = CustomPasswordChangeForm(user=request.user)
            return render(request, 'registration/profile_change.html', {'user_form': user_form,
                                                                        'password_form': password_form})
        else:
            raise Http404('Użytkownik podany w sesji nie jest zalogowany')

    def post(self, request):
        if 'profile_change' in request.POST:
            user_form = UserChangeForm(request.POST, instance=request.user)
            if user_form.is_valid():
                username = request.user.username
                password = user_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    user_form.save()
                    messages.success(request, 'Dane użytkownika zostały zmienione')
                    return redirect('profile')
                else:
                    user_form.add_error(None, f'Podane błędne hasło dla użytkownika {username}')

            password_form = CustomPasswordChangeForm(user=request.user)
            return render(request, 'registration/profile_change.html', {'user_form': user_form,
                                                                        'password_form': password_form})

        elif 'password_change' in request.POST:
            password_form = CustomPasswordChangeForm(data=request.POST, user=request.user)
            if password_form.is_valid():
                update_session_auth_hash(request, request.user)
                password_form.save()
                logout(request)
                messages.success(request, 'Hasło zostało zmienione')
                return redirect('login')
            user_form = UserChangeForm(instance=request.user)
            return render(request, 'registration/profile_change.html', {'user_form': user_form,
                                                                        'password_form': password_form})
        else:
            return Http404('Błąd formularza')
