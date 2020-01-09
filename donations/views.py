from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from donations.models import Donation


class LandingPageView(View):
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        backed_institutions = Donation.objects.distinct('institution').count()
        return render(request, 'index.html', {'quantity': bags_quantity,
                                              'institutions': backed_institutions})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')
