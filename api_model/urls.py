from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djgentelella.urls import urlpatterns as djgentelellaurls
from api_model.views import apimodel
from api_model.viewset import ModelTemplateViewSet, FormViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'models', ModelTemplateViewSet),
router.register(r'forms', FormViewSet),
router.register(r'questions', QuestionViewSet)



urlpatterns = djgentelellaurls + [
    path('', apimodel, name='home'),
    path('api/', include(router.urls)),
    #path('add_question_to_form/<int:form_id>/', AddQuestionToForm.as_view(), name='add-question-to-form'),

]
