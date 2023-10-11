# serializers.py

from rest_framework import serializers
from .models import ModelTemplate


class ModelTemplateSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source='_meta.app_label', read_only=True)
    app_name = serializers.CharField(source='_meta.app_name', read_only=True)

    class Meta:
        model = ModelTemplate
        fields = '__all__'







