from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from accounts.forms import CustomRegistrationForm
from donations.models import Donation


class SignUp(generic.CreateView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class UserProfileView(LoginRequiredMixin, View):
    def get(self,request):
        donations = Donation.objects.filter(user=request.user).order_by('is_taken', 'pick_up_date',
                                                                        'pick_up_time', 'quantity')
        return render(request, 'user_site.html', {'donations': donations})

