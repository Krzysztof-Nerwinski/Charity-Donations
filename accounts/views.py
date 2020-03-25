from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from accounts.forms import CustomRegistrationForm, UserChangeForm, CustomPasswordChangeForm, CustomAuthenticationForm, \
    CustomPasswordResetForm
from accounts.models import CustomUser
from accounts.tokens import account_activation_token
from donations.models import Donation


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        signup_form = CustomRegistrationForm()
        return render(request, 'registration/register.html', {'form': signup_form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        signup_form = CustomRegistrationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            current_site = get_current_site(request)
            subject = 'Aktywuj swoje konto na charity.com'
            message = render_to_string('registration/registration_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uname': urlsafe_base64_encode(force_bytes(user.username)),
                'token': account_activation_token.make_token(user)
            })
            try:
                user.email_user(subject=subject, message=message)
            except Exception as exc:
                print('Błąd: ', exc)
                error_msg = 'Błąd przy wysyłaniu wiadomości aktywacyjnej, użytkownik nie został utworzony. ' \
                            'Spróbuj ponownie, jeśli widzisz tę wiadomość kolejny raz skontaktuj się z nami.'
                signup_form.add_error(None, error_msg)
            else:
                user.save()
                user_mail_domain = user.email.split("@")[1]
                message = 'Email aktywacyjny został wysłany. Dziękujemy za rejestrację! '
                link = f"<a href='http://{user_mail_domain}' class='messages-link'>Przejdź do swojej poczty</a>"
                confirmation = message + link
                messages.success(request, confirmation)
                return redirect('login')
        return render(request, 'registration/register.html', {'form': signup_form})


class ActivationView(View):
    def get(self, request, unameb64, token):
        if request.user.is_authenticated:
            messages.error(request, "Obecne konto jest już aktywne, w celu aktywacji innego konta wyloguj się")
            return redirect('profile')
        try:
            username = force_str(urlsafe_base64_decode(unameb64))
            user = CustomUser.objects.get(username=username)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Aktywacja konta zakończona powodzeniem')
            return redirect('login')
        else:
            return render(request, 'registration/account_activation_invalid.html')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


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


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('password_reset_sent')
    form_class = CustomPasswordResetForm


class CustomPasswordResetSentView(PasswordResetDoneView):
    template_name = 'registration/password_reset_sent.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirmation.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_completed.html'
