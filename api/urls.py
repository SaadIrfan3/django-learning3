from django.urls import path
from .views import signup_user, login_user,get_profile

urlpatterns = [
    path('signup/', signup_user),
    path('login/', login_user),
    path('profile/',get_profile)
]
