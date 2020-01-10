from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='index'),
    path('add_donation/', views.AddDonationView.as_view(), name='add-donation'),
]
