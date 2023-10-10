from django.db import models


class ModelTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    nameFields = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FormWithQuestions(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=255)
    question_text = models.CharField(max_length=255)
    associated_model = models.ForeignKey(ModelTemplate, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Response(models.Model):
    response = models.TextField(blank=True, null=True)
    questions = models.OneToOneField(FormWithQuestions, on_delete=models.CASCADE)

    def __str__(self):
        return self.response

