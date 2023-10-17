from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from api_model.models import ModelTemplate
from api_model.serializers import ModelTemplateSerializer


def apimodel(request):

    return render(request,'home.html')



class ModelFieldsList(generics.ListAPIView):
    serializer_class = ModelTemplateSerializer

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        queryset = ModelTemplate.objects.filter(name=model_name)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        name_fields_list = [obj.nameFields for obj in queryset]
        return Response({'nameFields': name_fields_list})

