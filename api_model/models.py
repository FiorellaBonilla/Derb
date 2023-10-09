from django.apps import apps
from django.db import models

class ModelTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    nameFields = models.CharField(max_length=100, null=True)
    field_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Forms(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    model_template = models.ForeignKey(ModelTemplate, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text
