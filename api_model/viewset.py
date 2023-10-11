
from rest_framework import viewsets, status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

from api_model.models import ModelTemplate
from api_model.serializers import ModelTemplateSerializer
from rest_framework.permissions import IsAuthenticated

class ModelTemplateViewSet(viewsets.ModelViewSet):
    queryset = ModelTemplate.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class =  ModelTemplateSerializer

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



