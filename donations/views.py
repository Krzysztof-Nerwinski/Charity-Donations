from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from donations.models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        backed_institutions = Donation.objects.distinct('institution').count()
        foundations = Institution.objects.filter(type=1)
        nongov_institutions = Institution.objects.filter(type=2)
        local_pickups = Institution.objects.filter(type=3)
        return render(request, 'index.html', {'quantity': bags_quantity,
                                              'backed_institutions': backed_institutions,
                                              'foundations': foundations,
                                              'nongov_institutions': nongov_institutions,
                                              'local_pickups': local_pickups})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')
