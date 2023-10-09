from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

from api_model.models import ModelTemplate, Forms, Question
from api_model.serializers import ModelTemplateSerializer, FormSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated

class ModelTemplateViewSet(viewsets.ModelViewSet):
    queryset = ModelTemplate.objects.all()
    serializer_class = ModelTemplateSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

class FormViewSet(viewsets.ModelViewSet):
    queryset = Forms.objects.all()
    serializer_class = FormSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer











