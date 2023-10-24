import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_model.models import ModelTemplate, FormModel, tinyModel, ModelFields, ResponseForm
from api_model.serializers import ModelTemplateSerializer, ResponseFormSerializer

@login_required
def home(request):
    return render(request, 'home.html')
@login_required
def api_model_view(request, form_id):
    form = FormModel.objects.get(id=form_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        nueva_pregunta = tinyModel(
            text= text,

        )
        nueva_pregunta.save()
        form.model_pre.add(nueva_pregunta)
        preguntas_creadas = [nueva_pregunta]

    else:
        preguntas_creadas = form.model_pre.all()

    return render(request, 'api_model_view.html', {'form': form, 'preguntas_creadas': preguntas_creadas})


@login_required
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


@login_required
def update_form(request, form_id):
    if request.method == 'PUT':
        try:
            form = FormModel.objects.get(id=form_id)
        except FormModel.DoesNotExist:
            return JsonResponse({'error': 'El formulario no existe'}, status=404)
        return JsonResponse({'message': 'Formulario actualizado con éxito'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def fetch_form_api(preguntas_creadas):
    api_url = "/api/form/"
    payload = {
        "preguntas_creadas": preguntas_creadas
    }

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Error al hacer la solicitud a la API de form")

    fetch_form_api(preguntas_creadas)
@login_required
def form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description_model = request.POST.get('description_model')

        nuevo_formulario = FormModel(
            title=title,
            description_model=description_model
        )
        nuevo_formulario.save()

        return redirect('api_model_view', form_id=nuevo_formulario.id)
    nuevo_formulario = FormModel()

    return render(request, 'create_form_model.html',{'nuevo_formulario': nuevo_formulario})


@login_required
def render_name_fields(request):
   # name_fields = ModelFields.objects.all()

    return render(request, 'form_model.html')
@login_required
def render_view_model(request):
    #name_fields = ModelFields.objects.all()

    return render(request, 'render_view_model.html')

@login_required
def render_view_model(request):
    content_from_tiny = tinyModel.objects.first()
    response_content = ResponseForm.objects.filter(responseF=content_from_tiny.text).first()
    context = {
        'response_content': response_content,
    }

    return render(request, 'render_view_model.html', context)



@login_required
class ResponseFormByField(APIView):
    def get(self, request, nameFields):
        try:
            response_form = ResponseForm.objects.get(fieldsRes=nameFields)
            serializer = ResponseFormSerializer(response_form)
            return Response(serializer.data)
        except ResponseForm.DoesNotExist:
            return Response({'error': 'No se encontró ninguna respuesta para el campo especificado'}, status=status.HTTP_404_NOT_FOUND)


