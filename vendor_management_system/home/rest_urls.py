import home.rest_views as rest_views
from django.urls import path

urlpatterns = [
    path('user-login/', rest_views.UserLoginView.as_view(), name='login'),
    path('user-registration/', rest_views.UserRegistrationView.as_view(), name='registration'), 
]