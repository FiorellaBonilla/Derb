from django.db import models

class ModelTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ModelFields(models.Model):
    nameFields = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)
    model_inicial = models.ManyToManyField(ModelTemplate)


    def __str__(self):
        return self.nameFields




class tinyModel(models.Model):
    text = models.TextField(blank=True, null=True)

    def __str__(self):

        return self.text
class FormModel(models.Model):
    title = models.CharField(max_length=200)
    description_model = models.TextField(blank=True, null=True)
    model_pre = models.ManyToManyField(tinyModel)

    def __str__(self):

        return self.title

class ResponseForm(models.Model):
    responseF = models.TextField(blank=True, null=True)
    fieldsRes = models.OneToOneField(ModelFields, on_delete= models.CASCADE)

    def __str__(self):

        return self.responseF

class UserResponse(models.Model):
    response_text = models.TextField(blank=True, null=True)
    field = models.ForeignKey(ModelFields, on_delete=models.CASCADE)
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE)

#ejemplo
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ID Number: {self.id_number}'

class Room(models.Model):
    physical_address = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    occupants_count = models.IntegerField()

    def __str__(self):
        return f'Address: {self.physical_address} - Color: {self.color} - Occupants: {self.occupants_count}'

class Pet(models.Model):
    PET_TYPES = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Fish', 'Fish'),
    )

    pet_type = models.CharField(max_length=50, choices=PET_TYPES)
    color = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return f'Type: {self.get_pet_type_display()} - Color: {self.color} - Age: {self.age} years'


class Descriptor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    persons = models.ManyToManyField('Person')
    rooms = models.ManyToManyField('Room')
    pets = models.ManyToManyField('Pet')

    def __str__(self):
        return self.name