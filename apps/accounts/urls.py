from django.urls import path, re_path
from . import views as acc_views
from django.contrib.auth import views as auth_views
from django.contrib import admin

from .views import UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', acc_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^activate/(?P<unameb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            acc_views.ActivationView.as_view(),
            name='activate'),
    path('register/', acc_views.SignUp.as_view(), name='register'),
    path('password_reset/', acc_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/sent/', acc_views.CustomPasswordResetSentView.as_view(), name='password_reset_sent'),
    path('password_reset/<uidb64>/<token>/',
         acc_views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/done', acc_views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user_edit/', acc_views.ProfileChangeView.as_view(), name='user_edit'),
    path('profile/', UserProfileView.as_view(), name='profile'),

]
