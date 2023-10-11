from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djgentelella.urls import urlpatterns as djgentelellaurls

from api_model import views
from api_model.views import apimodel
from api_model.viewset import ModelTemplateViewSet, GetModelInfoView

router = DefaultRouter()
router.register(r'models', ModelTemplateViewSet),



urlpatterns =  [
    path('', apimodel, name='home'),
    path('api/', include(router.urls)),
    path('template/', views.template_view, name='template_view'),
    path('rendered_template/', views.render_template, name='rendered_template'),
    path('api/models/get_model_info/<int:model_id>/', GetModelInfoView.as_view(), name='get-model-info'),
    path('api/render_template/', views.render_template, name='render_template'),

]
