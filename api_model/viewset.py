
from rest_framework import viewsets, status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

from api_model.models import ModelTemplate, FormWithQuestions
from api_model.serializers import FormWithQuestionsSerializer, ModelTemplateFullSerializer, \
    ModelTemplateBasicSerializer, ModelTemplateSerializer, ResponseSerializer, ObjectModelSerializer
from rest_framework.permissions import IsAuthenticated

class ModelTemplateViewSet(viewsets.ModelViewSet):
    queryset = ModelTemplate.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class =  ObjectModelSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ModelTemplateFullSerializer
        elif self.action == 'basic_info':
            return ModelTemplateBasicSerializer
        return ModelTemplateFullSerializer

    @action(detail=False)
    def basic_info(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class FormWithQuestionsViewSet(viewsets.ModelViewSet):
    queryset = FormWithQuestions.objects.all()
    serializer_class = FormWithQuestionsSerializer

class GetModelInfoView(generics.RetrieveAPIView):
    queryset = ModelTemplate.objects.all()
    serializer_class = ModelTemplateSerializer

    def retrieve(self, request, model_id, *args, **kwargs):
        try:
            model = ModelTemplate.objects.get(id=model_id)
            model_data = {
                'name': model.name,
                'nameFields': model.nameFields,
            }
            return Response(model_data)
        except ModelTemplate.DoesNotExist:
            return Response({'error': 'Modelo no encontrado'}, status=404)



