from django.db import models
from django.contrib.auth.models import User

class ModelTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    nameFields = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ResponseM(models.Model):
    model_template = models.ForeignKey(ModelTemplate, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    response_data = models.TextField()
