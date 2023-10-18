from django.db import models

class ModelTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    nameFields = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class tinyModel(models.Model):
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text