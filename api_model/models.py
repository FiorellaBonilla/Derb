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
    model_pre = models.ManyToManyField(ModelTemplate)

    def __str__(self):

        return self.title


class ResponseForm(models.Model):
    responseF = models.TextField(blank=True, null=True)
    fieldsRes = models.OneToOneField(ModelFields, on_delete= models.CASCADE)

    def __str__(self):

        return self.responseF

