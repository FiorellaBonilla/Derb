from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djgentelella.urls import urlpatterns as djgentelellaurls

from api_model import views
from api_model.views import form, home, api_model_view, render_view_model
from api_model.viewset import ModelTemplateViewSet, tinyViewset, FormModelViewset, ModelFieldsViewset, \
    ResponseFormViewset, UserResponseViewset

router = DefaultRouter()
router.register(r'models', ModelTemplateViewSet),
router.register(r'tiny', tinyViewset),
router.register(r'form', FormModelViewset),
router.register(r'modelFields', ModelFieldsViewset),
router.register(r'response', ResponseFormViewset),
router.register(r'userresponses', UserResponseViewset)



urlpatterns =  [
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('create/', form, name='create'),
    path('api_model_view/<int:form_id>/', api_model_view, name='api_model_view'),
    path('api/combined_models/', views.CombinedModelList.as_view(), name='combined-model-list'),
    path('api/combined_data/', views.CombinedDataList.as_view(), name='combined-data-list'),
    path('render_principal/<int:form_id>/<int:tiny_id>/', views.render_principal, name='render_principal'),
    path('render_view_model/<int:pk>/', views.DescriptorDetailView.as_view(), name='descriptor-detail'),
    path('CombinedDataAPI/', views.CombinedDataAPI.as_view(), name='CombinedDataAPI'),

]
