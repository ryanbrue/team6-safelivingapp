"""backend_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crimedata/', include('cde_api.urls')),
    path('geocoding/', include('loc_to_addr.urls')),
    path('safelivingscore/', include('safe_living_score.urls')),
    path('amenities/', include('amenities.urls')),
    path('transportation/', include('transportation_score.urls')),
    path('costofliving/', include('cost_of_living.urls')),
    path('boundaries/', include('boundaries.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('user/', include('user.urls')),
    path('dataset_utils/', include('dataset_utils.urls')),
]
