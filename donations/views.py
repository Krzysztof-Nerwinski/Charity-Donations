from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.views import View, generic
from donations.forms import DonationForm
from donations.models import Donation, Institution, FOUNDATION, ORGANIZATION, LOCAL_COLLECTION


class LandingPageView(View):
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        backed_institutions = Donation.objects.distinct('institution').count()
        foundations = Institution.objects.filter(type=FOUNDATION)
        nongov_institutions = Institution.objects.filter(type=ORGANIZATION)
        local_pickups = Institution.objects.filter(type=LOCAL_COLLECTION)
        return render(request, 'index.html', {'quantity': bags_quantity,
                                              'backed_institutions': backed_institutions,
                                              'foundations': foundations,
                                              'nongov_institutions': nongov_institutions,
                                              'local_pickups': local_pickups})


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
    def get(self,request,donation_id):
        raise Http404('Archiwizacja możliwa tyko poprzez przyciski w profilu i w szczegółowym widoku darowizny')

    def post(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = False if donation.is_taken else True
        donation.save()
        return redirect('profile')


class SingleDonationView(LoginRequiredMixin, generic.DetailView):
    model = Donation
    context_object_name = 'donation'
