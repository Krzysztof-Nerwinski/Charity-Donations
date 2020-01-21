from django.urls import path
from . import views
from .views import archive_donation

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='index'),
    path('add_donation/', views.AddDonationView.as_view(), name='add-donation'),
    path('archive_donation/<int:donation_id>/', archive_donation, name='archive_donation'),
]
