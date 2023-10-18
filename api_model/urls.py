from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djgentelella.urls import urlpatterns as djgentelellaurls

from api_model import views
from api_model.views import apimodel, form
from api_model.viewset import ModelTemplateViewSet, GetModelInfoView, tinyViewset

router = DefaultRouter()
router.register(r'models', ModelTemplateViewSet),
router.register(r'tiny', tinyViewset),


urlpatterns =  [
    path('', apimodel, name='home'),
    path('api/', include(router.urls)),
    path('api/models/get_model_info/<int:model_id>/', GetModelInfoView.as_view(), name='get-model-info'),
    path('create/', form, name='create'),


]
