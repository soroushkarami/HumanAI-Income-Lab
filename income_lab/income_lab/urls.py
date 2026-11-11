
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),    # admin page
    path('', include('income_predictor.urls')),     # game + register URLs ---> the app urls.py handles them
    path('accounts/', include('django.contrib.auth.urls'))      # login/logout/password reset ---> auth.urls handles them
    # This automatically creates:
    # /accounts/login/
    # /accounts/logout/
    # /accounts/password_change/
    # /accounts/password_reset/
]
