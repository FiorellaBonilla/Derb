from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api_model.models import ModelTemplate
from api_model.serializers import ModelTemplateSerializer


# Create your tests here.
#model template
class ModelTemplateTestCase(TestCase):
    def test_model_creation(self):
        model = ModelTemplate(name="Test Model", description="Description", nameFields="Field Name", field_type="Field Type")
        model.save()
        self.assertEqual(model.name, "Test Model")
        self.assertEqual(model.description, "Description")
        self.assertEqual(model.nameFields, "Field Name")
        self.assertEqual(model.field_type, "Field Type")


#serializer
class ModelTemplateSerializationTestCase(TestCase):
    def test_model_serialization(self):
        model = ModelTemplate(name="Test Model", description="Description", nameFields="Field Name", field_type="Field Type")
        model.save()
        serialized_data = ModelTemplateSerializer(model).data
        self.assertEqual(serialized_data['name'], "Test Model")
        self.assertEqual(serialized_data['description'], "Description")
        self.assertEqual(serialized_data['nameFields'], "Field Name")
        self.assertEqual(serialized_data['field_type'], "Field Type")


class ModelTemplateValidationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_model_template_with_invalid_data(self):
        data = {'name': 'Test Model', 'description': '', 'nameFields': 'Field Name', 'field_type': 'Field Type'}
        response = self.client.post('/api/modeltemplates/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ModelTemplate.objects.count(), 0)

    def test_create_model_template_with_valid_data(self):
        data = {'name': 'Test Model', 'description': 'Description', 'nameFields': 'Field Name', 'field_type': 'Field Type'}
        response = self.client.post('/api/modeltemplates/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ModelTemplate.objects.count(), 1)


