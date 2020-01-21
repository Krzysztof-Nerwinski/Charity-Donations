from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import CustomRegistrationForm
from donations.models import Donation


class SignUp(generic.CreateView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


@login_required
def user_profile_view(request):
    if request.method == 'GET':
        donations = Donation.objects.filter(user=request.user).order_by('is_taken', 'pick_up_date')
        return render(request, 'user_site.html', {'donations': donations})

