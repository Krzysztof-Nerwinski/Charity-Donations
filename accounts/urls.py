from django.urls import path, include
from . import views as acc_views
from .forms import CustomAuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib import admin

from .views import UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', acc_views.SignUp.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm,
                                                redirect_authenticated_user=True), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
