from django.http import JsonResponse
from django.shortcuts import  redirect
from rest_framework import generics
from rest_framework.response import Response

from api_model.models import FormWithQuestions, ModelTemplate
from django.shortcuts import render

from api_model.serializers import ModelTemplateSerializer


def apimodel(request):

    return render(request,'home.html')


def template_view(request):
    return render(request, 'template.html')


def render_template(request):
    template_content = """
    <html>
    <body>
        <h1>{{name}}</h1>
        <p>{{nameFields}}</p>
    </body>
    </html>
    """

    data = {
        'title': 'Título Real',
        'content': 'Contenido Real',
    }

    rendered_template = template_content
    for key, value in data.items():
        placeholder = f'{{{{{key}}}}}'
        rendered_template = rendered_template.replace(placeholder, value)

    return render(request, 'rendered_template.html', {'rendered_template': rendered_template})

class ModelFieldsList(generics.ListAPIView):
    serializer_class = ModelTemplateSerializer

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        queryset = ModelTemplate.objects.filter(name=model_name)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        name_fields_list = [obj.nameFields for obj in queryset]
        return Response({'nameFields': name_fields_list})

def render_template(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')

        rendered_template = render(request, 'template.html', {'content': content})

        rendered_content = rendered_template.content.decode('utf-8')

        return JsonResponse({'rendered_template': rendered_content})

    return JsonResponse({'error': 'Método no permitido'}, status=405)