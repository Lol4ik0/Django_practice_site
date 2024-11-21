from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.user_login, name='login'),
    path('logout/', LogOutView.user_logout, name='logout'),
    path('profile/', UserProfileView.user_profile, name='profile'),
    path('profile_<int:pk>_edit/', UpdateUserView.as_view(), name='update_user'),
    path('profile_<int:pk>_delete/', DeleteUserView.as_view(), name='delete_user'),
    path('contact/', user_contact, name='contact-me'),
]
