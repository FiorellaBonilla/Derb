from django.urls import path
from api_model.views import apimodel
from djgentelella.urls import urlpatterns as djgentelellaurls

urlpatterns = djgentelellaurls + [
    path('', apimodel, name='home'),
]
