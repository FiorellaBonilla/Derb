
from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from api_model.models import ModelTemplate, tinyModel, FormModel, ModelFields, ResponseForm, UserResponse
from api_model.serializers import ModelTemplateSerializer, tinySerializer, formModelSerializer, ModelFieldsSerializer, \
    ResponseFormSerializer, UserResponseSerializer, CombinedModelSerializer
from rest_framework.permissions import IsAuthenticated

class ModelTemplateViewSet(viewsets.ModelViewSet):
     queryset = ModelTemplate.objects.all()
     authentication_classes = [BasicAuthentication]
     permission_classes = [IsAuthenticated]
     serializer_class =  ModelTemplateSerializer




class tinyViewset(viewsets.ModelViewSet):
    queryset = tinyModel.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = tinySerializer

class FormModelViewset(viewsets.ModelViewSet):
    queryset = FormModel.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = formModelSerializer


class ModelFieldsViewset(viewsets.ModelViewSet):
    queryset = ModelFields.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ModelFieldsSerializer

class ResponseFormViewset(viewsets.ModelViewSet):
    queryset = ResponseForm.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResponseFormSerializer

class UserResponseViewset(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer


#viewset combinado
