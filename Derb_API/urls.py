"""Derb_API URL Configuration

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
from django.http import HttpResponse
from django.urls import path, include
from djgentelella.urls import urlpatterns as djgentelellaurls
from api_model.urls import urlpatterns as url

def home(request):
    return HttpResponse('OK')

urlpatterns = djgentelellaurls + [
path('admin/', admin.site.urls),
path('', include('api_model.urls'))

] + url
