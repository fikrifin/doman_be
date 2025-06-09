"""
URL configuration for doman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from transaksi.urls import urlpatterns as transaksi_urls
from users.urls import urlpatterns as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doman/', include(transaksi_urls)),
    path('api/user/', include('users.urls')),  # Enable users URLs
    path('api/auth/', include('dj_rest_auth.urls')),
    # Remove default registration URL
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
