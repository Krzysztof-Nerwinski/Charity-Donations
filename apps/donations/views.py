from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views import View, generic

from apps.accounts.models import CustomUser
from apps.donations.forms import DonationForm
from apps.donations.models import Donation, Institution
from charity.local_settings import EMAIL_HOST_USER


class LandingPageView(View):
    def get(self, request):
        donations_counters = {
            'bags_quantity': Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
            'backed_institutions': Donation.objects.distinct('institution').count()
        }
        all_institutions = Institution.objects.all()
        return render(request, 'donations/index.html', {'donations_counters': donations_counters,
                                                        'all_institutions': all_institutions})


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        form = DonationForm(auto_id=False)
        organizations = Institution.objects.all()
        return render(request, 'donations/form.html', {'organizations': organizations,
                                                       'form': form})

    def post(self, request):
        form = DonationForm(request.POST, auto_id=False)
        if form.is_valid():
            form.save()
            return render(request, 'donations/form-confirmation.html')
        organizations = Institution.objects.all()
        selected_categories = form.cleaned_data.get('categories')
        return render(request, 'donations/form.html', {'selected_categories': selected_categories,
                                                       'organizations': organizations,
                                                       'form': form})


class ArchiveDonation(LoginRequiredMixin, View):
    def get(self, request, donation_id):
        raise Http404('Archiwizacja możliwa tyko poprzez przyciski w profilu i w szczegółowym widoku darowizny')

    def post(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = False if donation.is_taken else True
        donation.save()
        return redirect('profile')


class SingleDonationView(LoginRequiredMixin, generic.DetailView):
    model = Donation
    context_object_name = 'donation'


class ContactMailView(View):

    @staticmethod
    def add_error(request, exception=None):
        if exception: print('Błąd: ', exception)
        error_msg = _('Błąd przy wysyłaniu wiadomości. Upewnij się, że wypełnione są wszystkie pola formularza. '
                      'Spróbuj ponownie lub jeśli widzisz tę wiadomość kolejny raz skontaktuj się z nami.')
        messages.error(request, error_msg)

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        message = request.POST.get('message')
        if name and surname and message:
            subject = _(f'Wiadomość od {name} {surname} poprzez stronę Charity')
            message = render_to_string('donations/contact_email.html', {
                'first_name': name,
                'message': message})
            admin_mail_list = [user.email for user in CustomUser.objects.filter(is_staff=True)]
            try:
                send_mail(subject=subject, message=message, recipient_list=admin_mail_list, from_email=EMAIL_HOST_USER)
            except Exception as exc:
                self.add_error(request, exc)
                return redirect('index')
            else:
                return render(request, 'donations/contact_email_sent.html')
        else:
            self.add_error(request)
            return redirect('index')
