# serializers.py

from rest_framework import serializers
from .models import ModelTemplate, FormWithQuestions, Response


class ModelTemplateSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source='_meta.app_label', read_only=True)
    app_name = serializers.CharField(source='_meta.app_name', read_only=True)

    class Meta:
        model = ModelTemplate
        fields = '__all__'

class FormWithQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormWithQuestions
        fields = '__all__'


class ModelTemplateFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTemplate
        fields = '__all__'

class ModelTemplateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTemplate
        fields = ['name', 'nameFields']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

from rest_framework import serializers

class NameFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.CharField()

class ObjectModelSerializer(serializers.Serializer):
    description = serializers.CharField()
    nameFields = NameFieldSerializer(many=True)



