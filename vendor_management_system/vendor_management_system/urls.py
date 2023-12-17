from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',  include(('home.rest_urls', 'home'), namespace='auth')),
    path('api/',  include(('vendor.rest_urls', 'vendor'), namespace='vendor')),
]