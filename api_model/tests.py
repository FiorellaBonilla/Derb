from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from api_model.models import ModelTemplate, ModelFields, tinyModel, FormModel, ResponseForm, Person, Room, Pet, \
    Descriptor
from api_model.serializers import ModelTemplateSerializer, ModelFieldsSerializer, tinySerializer, formModelSerializer, \
    ResponseFormSerializer, CombinedModelSerializer
from api_model.viewset import ModelFieldsViewset


# Create your tests here.
#model template test

#verify that creating a ModelTemplate instance works correctly
# and that the name and description
# fields have the expected values saving the object to the database.

#Response: OK
class ModelTemplateTestCase(TestCase):
    def test_model_creation(self):
        model = ModelTemplate(name="Test Model", description="Description")
        model.save()
        self.assertEqual(model.name, "Test Model")
        self.assertEqual(model.description, "Description")



#serializer
#verify that serializing a ModelTemplate
# instance with the ModelTemplateSerializer
# serializer works correctly and that
# the serialized data matches the expected values.
#Response: OK
class ModelTemplateSerializationTestCase(TestCase):
    def test_model_serialization(self):
        model = ModelTemplate(name="Test Model", description="Description")
        model.save()
        serialized_data = ModelTemplateSerializer(model).data
        self.assertEqual(serialized_data['name'], "Test Model")
        self.assertEqual(serialized_data['description'], "Description")



#test creating a model using invalid
# data via a POST request to an API

#Response: OK
class ModelTemplateValidationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Crea un usuario para autenticación en las pruebas
        self.user = User.objects.create_user(username='test', password='1234')
        # Autentica al usuario en el cliente de prueba
        self.client.force_authenticate(user=self.user)

    def test_create_model_template_with_invalid_data(self):
        data = {'name': 'Test Model', 'description': ''}
        response = self.client.post('/api/models/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ModelTemplate.objects.count(), 0)

    def test_create_model_template_with_valid_data(self):
        data = {'name': 'Test Model', 'description': 'Description'}
        response = self.client.post('/api/models/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ModelTemplate.objects.count(), 1)


#ModelFields TEST

#test_model_fields_creation:
#This test ensures that ModelFields instantiation works correctly
# and that relationships are established properly.

#test_model_fields_str_method:
#This test validates that the custom __str__
# method on the model returns a readable representation of the model
# , in this case the name of the fields.

#test_model_fields_association_with_model_template:
#This test validates that the relationship between ModelFields
# and ModelTemplate works correctly and that
# appropriate associations can be established

#Response test_model_fields_creation: OK
#Response test_model_fields_str_method: OK
#Response test_model_fields_association_with_model_template: OK
class ModelFieldsTestCase(TestCase):
    def setUp(self):
        self.model_template = ModelTemplate.objects.create(name="Test Model", description="Description")

    def test_model_fields_creation(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        model_fields.model_inicial.add(self.model_template)
        self.assertEqual(model_fields.nameFields, "Field Name")
        self.assertEqual(model_fields.field_type, "Field Type")

        self.assertEqual(model_fields.model_inicial.count(), 1)
        self.assertEqual(model_fields.model_inicial.first(), self.model_template)

    def test_model_fields_str_method(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        self.assertEqual(str(model_fields), "Field Name")

    def test_model_fields_association_with_model_template(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        model_fields.model_inicial.add(self.model_template)

        self.assertEqual(model_fields.model_inicial.count(), 1)
        self.assertEqual(model_fields.model_inicial.first(), self.model_template)


#serializer:
#test_serialization: An instance of ModelFields is created,
# serialized using the ModelFieldsSerializer serializer,
# and then verified to ensure that the serialized
# data matches the values in the instance.

#test_deserialization: A data dictionary is created that will be used
# for deserialization. A ModelFieldsSerializer object is created with this data,
# verified that the data is valid, and that validation passes without errors.
# A new ModelFields instance is then created from the deserialized data

#Response test_serialization: OK
#Response test_deserialization: Failed AssertionError: False is not true

class ModelFieldsSerializerTestCase(TestCase):
    def test_serialization(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()

        serializer = ModelFieldsSerializer(model_fields)

        self.assertEqual(serializer.data['nameFields'], "Field Name")
        self.assertEqual(serializer.data['field_type'], "Field Type")

    def test_deserialization(self):
        data = {'nameFields': "New Field Name", 'field_type': "New Field Type"}

        serializer = ModelFieldsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        model_fields = serializer.save()
        self.assertEqual(model_fields.nameFields, "New Field Name")
        self.assertEqual(model_fields.field_type, "New Field Type")

#Tiny model test

#test_model_creation: Verifies that a tinyModel
# instance can be created and that
# the fields are saved correctly in the database.

#test_model_blank_and_null_fields: Tests whether a
# tinyModel can be instantiated with a blank
# field and is successfully saved to the database.

#test_model_null_fields: Tests whether a tinyModel
# instance can be created with a null
# field (None) and is successfully saved to the database.

#Response test_model_creation: OK
#Response test_model_str_method: OK
#Response test_model_blank_and_null_fields: OK
#Response test_model_null_fields: OK


class TinyModelTestCase(TestCase):
    def test_model_creation(self):
        tiny_instance = tinyModel(text="This is a test text.")
        tiny_instance.save()
        self.assertEqual(tiny_instance.text, "This is a test text.")

    def test_model_str_method(self):
        tiny_instance = tinyModel(text="Sample Text")
        self.assertEqual(str(tiny_instance), "Sample Text")

    def test_model_blank_and_null_fields(self):
        tiny_instance = tinyModel(text="")
        self.assertEqual(tiny_instance.text, "")

    def test_model_null_fields(self):
        tiny_instance = tinyModel(text=None)

        self.assertIsNone(tiny_instance.text)


#SERIALIZER
#test_serialization: An instance of tinyModel is created,
# saved to the database, and then serialized
# using the tinySerializer serializer.
# The serialized data is then verified to match the model values.

#test_deserialization: A data dictionary is created that will be used
# for deserialization. A tinySerializer object is
# created with this data, verified that the data is valid,
# and that validation passes without errors. Next, a new
# tinyModel instance is created from the deserialized data
# and it is verified that the instance was created correctly.

#Response test_serialization: OK
#Response test_deserialization: OK

class TinySerializerTestCase(TestCase):
    def test_serialization(self):
        tiny_instance = tinyModel(text="This is a test text.")
        tiny_instance.save()

        serializer = tinySerializer(tiny_instance)

        self.assertEqual(serializer.data['text'], "This is a test text.")

    def test_deserialization(self):
        data = {'text': "New Text"}
        serializer = tinySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tiny_instance = serializer.save()
        self.assertEqual(tiny_instance.text, "New Text")


# FORMODEL TEST
#test_model_creation: Verifies that a FormModel
# instance can be created and
# that the fields are saved correctly in the database.

#test_model_pre_association: Creates a FormModel
# instance and a ModelTemplate instance.
# Then, associate the ModelTemplate instance
# with the FormModel through the model_pre relationship

#Response test_model_creation: OK
#Response test_model_str_method: OK
#Response test_model_pre_association:ValueError: "<FormModel: Test Form>"
# needs to have a value for field "id" before this many-to-many relationship can be used.



class FormModelTestCase(TestCase):
    def test_model_creation(self):
        form_model = FormModel(title="Test Form", description_model="Description")
        form_model.save()
        self.assertEqual(form_model.title, "Test Form")
        self.assertEqual(form_model.description_model, "Description")

    def test_model_str_method(self):
        form_model = FormModel(title="Sample Form")
        self.assertEqual(str(form_model), "Sample Form")

    def test_model_pre_association(self):
        form_model = FormModel(title="Test Form")
        model_template = ModelTemplate(name="Test Model", description="Description")
        model_template.save()
        form_model.model_pre.add(model_template)

        self.assertEqual(form_model.model_pre.count(), 1)
        self.assertEqual(form_model.model_pre.first(), model_template)

#Serializer:

#test_serialization: An instance of FormModel is created,
# saved to the database, and then serialized using the
# formModelSerializer serializer. The serialized data
# is then verified to match the model values.

#test_deserialization: A data dictionary is created that will
# be used for deserialization. A formModelSerializer object
# is created with this data, verified that the data is valid,
# and that validation passes without errors. Next, a new FormModel
# instance is created from the deserialized data and it is verified
# that the instance was created correctly.

#Response test_serialization: OK
#Response test_deserialization:AssertionError: False is not true

class FormModelSerializerTestCase(TestCase):
    def test_serialization(self):
        form_model = FormModel(title="Test Form", description_model="Description")
        form_model.save()

        serializer = formModelSerializer(form_model)

        self.assertEqual(serializer.data['title'], "Test Form")
        self.assertEqual(serializer.data['description_model'], "Description")

    def test_deserialization(self):
        data = {'title': "New Form", 'description_model': "New Description"}
        serializer = formModelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        form_model = serializer.save()
        self.assertEqual(form_model.title, "New Form")
        self.assertEqual(form_model.description_model, "New Description")


#response form test

#test_model_creation: An instance of ModelFields is
# created to use as a one-to-one relationship.
# Then, a ResponseForm instance is created related to that
# ModelFields instance. It verifies that the fields are saved
# correctly in the database and that the relationship between
# ResponseForm and ModelFields is correct.

#test_model_str_method: An instance of ModelFields and
# a ResponseForm instance related to that ModelFields
# instance are created. The ResponseForm model's custom __str__ method
# is then verified to return the form response as expected.

#Response test_model_creation: OK
#Response test_model_str_method: OK

class ResponseFormTestCase(TestCase):
    def test_model_creation(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        response_form = ResponseForm(responseF="Test Response", fieldsRes=model_fields)
        response_form.save()

        self.assertEqual(response_form.responseF, "Test Response")
        self.assertEqual(response_form.fieldsRes, model_fields)

    def test_model_str_method(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        response_form = ResponseForm(responseF="Sample Response", fieldsRes=model_fields)

        self.assertEqual(str(response_form), "Sample Response")


#SERIALIZER
#test_serialization: An instance of ModelFields
# and a ResponseForm instance related to that ModelFields
# instance are created. The ResponseForm instance is then
# serialized using the ResponseFormSerializer serializer.
# The serialized data is verified to match the model values,
# and special attention is paid to the fieldsRes field, which
# is serialized as the primary key (pk) of the ModelFields instance.


#test_deserialization: An instance of ModelFields is created.
# Next, a data dictionary is created to be used for deserialization.
# A ResponseFormSerializer object is created with this data, verified
# that the data is valid, and that validation passes without errors.
# Next, a new ResponseForm instance is created from the deserialized
# data, and it is verified that the instance was created correctly,
# including the relationship to the ModelFields instance.

#Response test_serialization: OK
#Response test_deserialization: OK

class ResponseFormSerializerTestCase(TestCase):
    def test_serialization(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        response_form = ResponseForm(responseF="Test Response", fieldsRes=model_fields)
        response_form.save()
        serializer = ResponseFormSerializer(response_form)
        self.assertEqual(serializer.data['responseF'], "Test Response")
        self.assertEqual(serializer.data['fieldsRes'], model_fields.pk)

    def test_deserialization(self):
        model_fields = ModelFields(nameFields="Field Name", field_type="Field Type")
        model_fields.save()
        data = {'responseF': "New Response", 'fieldsRes': model_fields.pk}
        serializer = ResponseFormSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response_form = serializer.save()
        self.assertEqual(response_form.responseF, "New Response")
        self.assertEqual(response_form.fieldsRes, model_fields)


#test of models examples
#test_create_person: This test checks if you
# can create a Person instance with certain attributes
# and then verify that the attributes are stored correctly in the database.
#test_person_str_method: This test checks if the __str__ method of
# the Person class is working correctly. The __str__ method defines
# how a Person instance will be represented as a string.
#Result:
#test_create_person: OK
#test_person_str_method: Ok
#test_person_unicode_method:OK

class PersonModelTest(TestCase):
    def test_create_person(self):
        person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            id_number="1234567890"
        )
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.id_number, "1234567890")

    def test_person_str_method(self):
        person = Person(
            first_name="Jane",
            last_name="Smith",
            id_number="9876543210"
        )
        self.assertEqual(str(person), "Jane Smith - ID Number: 9876543210")

    def test_person_unicode_method(self):
        person = Person(
            first_name="Alice",
            last_name="Johnson",
            id_number="5555555555"
        )
        self.assertEqual(str(person), "Alice Johnson - ID Number: 5555555555")

#room
#The test_create_room test verifies that the Room model
# can be instantiated with specific values for its
# fields (physical address, color, and number of occupants)
# and then verifies that the values are stored correctly in the database.
#Result:
#test_create_room: OK
#test_room_str_method: Ok


class RoomModelTest(TestCase):
    def test_create_room(self):
        room = Room.objects.create(
            physical_address="123 Main St",
            color="Blue",
            occupants_count=3
        )
        self.assertEqual(room.physical_address, "123 Main St")
        self.assertEqual(room.color, "Blue")
        self.assertEqual(room.occupants_count, 3)

    def test_room_str_method(self):
        room = Room(
            physical_address="456 Elm St",
            color="Red",
            occupants_count=2
        )
        expected_str = "Address: 456 Elm St - Color: Red - Occupants: 2"
        self.assertEqual(str(room), expected_str)

#pet
#The test_create_pet test verifies that the
# Pet model can be instantiated with specific
# values for its fields and then verifies that
# the values are stored correctly in the database
#Result:
#test_create_pet: OK
#test_pet_str_method: OK
class PetModelTest(TestCase):
    def test_create_pet(self):
        pet = Pet.objects.create(
            pet_type='Dog',
            color='Brown',
            age=3
        )
        self.assertEqual(pet.pet_type, 'Dog')
        self.assertEqual(pet.color, 'Brown')
        self.assertEqual(pet.age, 3)

    def test_pet_str_method(self):
        pet = Pet(
            pet_type='Cat',
            color='Gray',
            age=2
        )
        expected_str = "Type: Cat - Color: Gray - Age: 2 years"
        self.assertEqual(str(pet), expected_str)


#DESCRIPTOR
#The DescriptorModelTest test
# is used to verify the behavior of the
# Descriptor model and its relationships with other models
#Result:
#setUp: OK
#test_create_descriptor: Ok
#test_descriptor_str_method: OK

class DescriptorModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name="John", last_name="Doe", id_number="1234567890")
        self.room = Room.objects.create(physical_address="123 Main St", color="Blue", occupants_count=2)
        self.pet = Pet.objects.create(pet_type="Dog", color="Brown", age=3)

    def test_create_descriptor(self):
        descriptor = Descriptor.objects.create(
            name="Test Descriptor",
            description="This is a test descriptor"
        )

        descriptor.persons.add(self.person)
        descriptor.rooms.add(self.room)
        descriptor.pets.add(self.pet)

        self.assertEqual(descriptor.name, "Test Descriptor")
        self.assertEqual(descriptor.description, "This is a test descriptor")
        self.assertIn(self.person, descriptor.persons.all())
        self.assertIn(self.room, descriptor.rooms.all())
        self.assertIn(self.pet, descriptor.pets.all())

    def test_descriptor_str_method(self):
        descriptor = Descriptor(name="Sample Descriptor")
        self.assertEqual(str(descriptor), "Sample Descriptor")

#views



