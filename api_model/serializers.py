# serializers.py

from rest_framework import serializers
from api_model.models import ModelTemplate, ResponseM


class ModelTemplateSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source='_meta.app_label', read_only=True)
    app_name = serializers.CharField(source='_meta.app_name', read_only=True)

    class Meta:
        model = ModelTemplate
        fields = '__all__'
class ModelTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTemplate
        fields = ['id', 'name']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseM
        fields = ['id', 'model_template', 'field_name', 'response_data']








