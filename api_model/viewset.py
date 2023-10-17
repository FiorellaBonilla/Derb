
from rest_framework import viewsets, status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from api_model.models import ModelTemplate, ResponseM
from api_model.serializers import ModelTemplateSerializer, ResponseSerializer
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


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseM.objects.all()
    serializer_class = ResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)