from django.urls import path, include, re_path
from . import views as acc_views
from django.contrib import admin

from .views import UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', acc_views.CustomLoginView.as_view(), name='login'),
    re_path(r'^activate/(?P<unameb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            acc_views.ActivationView.as_view(), name='activate'),
    path('register/', acc_views.SignUp.as_view(), name='register'),
    path('user_edit/', acc_views.ProfileChangeView.as_view(), name='user_edit'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    path('', include('django.contrib.auth.urls')),

]
