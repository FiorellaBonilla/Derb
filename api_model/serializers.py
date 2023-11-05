# serializers.py

from rest_framework import serializers
from api_model.models import ModelTemplate, tinyModel, FormModel, ModelFields, ResponseForm, UserResponse, Person, Room, Pet


class ModelTemplateSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source='_meta.app_label', read_only=True)
    app_name = serializers.CharField(source='_meta.app_name', read_only=True)

    class Meta:
        model = ModelTemplate
        fields = '__all__'



class tinySerializer(serializers.ModelSerializer):

    class Meta:
        model = tinyModel
        fields = '__all__'

class formModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormModel
        fields = '__all__'

class ModelFieldsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelFields
        fields = '__all__'

class ResponseFormSerializer(serializers.ModelSerializer):
    fieldsRes = serializers.PrimaryKeyRelatedField(queryset=ModelFields.objects.all(),
                                                 required=True)
    class Meta:
        model = ResponseForm
        fields = '__all__'


class UserResponseSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.nameFields', read_only=True)
    form_name = serializers.CharField(source='form.title', read_only=True)

    class Meta:
        model = UserResponse
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['field'] = instance.field.nameFields  # Reemplaza 'field' con el nombre del campo
        data['form'] = instance.form.title  # Agrega el nombre del formulario
        return data


#example models combinados
class CombinedModelSerializer(serializers.Serializer):
    models = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

#see info to models
class CombinedDataSerializer(serializers.Serializer):
    persons = PersonSerializer(many=True)
    rooms = RoomSerializer(many=True)
    pets = PetSerializer(many=True)
