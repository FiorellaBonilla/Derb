import re
from re import findall
from django.shortcuts import render
from .models import Descriptor
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_model.models import ModelTemplate, FormModel, tinyModel, ModelFields, ResponseForm, Person, Room, Pet, \
    UserResponse, Descriptor
from api_model.serializers import ModelTemplateSerializer, ResponseFormSerializer, CombinedModelSerializer, \
    CombinedDataSerializer, PersonSerializer, RoomSerializer, PetSerializer


@login_required
def home(request):
    return render(request, 'home.html')
@login_required
def api_model_view(request, form_id):
    form = FormModel.objects.get(id=form_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        new_questionsModels = tinyModel(
            text= text,

        )
        new_questionsModels.save()
        form.model_pre.add(new_questionsModels)
        create_questionsModels = [new_questionsModels]

    else:
        create_questionsModels = form.model_pre.all()

    return render(request, 'api_model_view.html', {'form': form, 'create_questionsModels': create_questionsModels})


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
def fetch_form_api(create_questionsModels):
    api_url = "/api/form/"
    payload = {
        "create_questionsModels": create_questionsModels
    }

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Error al hacer la solicitud a la API de form")

    fetch_form_api(create_questionsModels)
@login_required
def form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description_model = request.POST.get('description_model')

        new_formModels = FormModel(
            title=title,
            description_model=description_model
        )
        new_formModels.save()

        return redirect('api_model_view', form_id=new_formModels.id)
    new_formModels = FormModel()

    return render(request, 'create_form_model.html',{'new_formModels': new_formModels})




#combinados
class CombinedModelList(APIView):
    def get(self, request):
        models = [
            {'name': 'Person'},
            {'name': 'Room'},
            {'name': 'Pet'},
        ]

        return Response(models)


#see reponse to models
class CombinedDataList(APIView):
    def get(self, request):
        response_data = {
            "models": {
                "person": {
                    "fields": {
                        "first_name": "string",
                        "last_name": "string",
                        "id_number": "string"
                    }
                },
                "room": {
                    "fields": {
                        "physical_address": "string",
                        "color": "string",
                        "occupants_count": "integer"
                    }
                },
                "pet": {
                    "fields": {
                        "pet_type": "string",
                        "color": "string",
                        "age": "integer"
                    }
                }
            }
        }

        return Response(response_data)



def render_view_model(request, descriptor_id):
    try:
        descriptor = Descriptor.objects.get(id=descriptor_id)
    except Descriptor.DoesNotExist:
        return render(request, 'error_template.html', {'error_message': 'El Descriptor no existe'})

    persons = descriptor.persons.all()
    rooms = descriptor.rooms.all()
    pets = descriptor.pets.all()

    return render(request, 'render_view_model.html', {'descriptor': descriptor, 'persons': persons, 'rooms': rooms, 'pets': pets})

class DescriptorDetailView(DetailView):
    model = Descriptor
    template_name = 'render_view_model.html'
    context_object_name = 'descriptor'


def render_principal(request, form_id, tiny_id):
    content_from_tiny = tinyModel.objects.filter(formmodel=form_id, id=tiny_id)

    # Replace the tags {{model.field}}
    for item in content_from_tiny:
        item.text = replace_content_placeholders(item.text)

    context = {
        'content_from_tiny': content_from_tiny,
        'form_id': form_id,
        'tiny_id': tiny_id,
    }

    return render(request, 'render_principal.html', context)



def replace_content_placeholders(content):
    # Find all matches of {{model.field}}
    matches = findall(r'\{\{(.+?)\}\}', content)

    # Perform the replacement
    for match in matches:
        model_field = match.split('.')
        if len(model_field) == 2:
            model_name, field_name = model_field
            try:
                model_instances = get_model_instances(model_name)
                if model_instances:
                    field_values = ', '.join([str(getattr(instance, field_name)) for instance in model_instances])
                    content = content.replace(f'{{{{{match}}}}}', field_values)
            except (KeyError, AttributeError):
                pass

    return content

def get_model_instances(model_name):
    try:
        model_name = model_name.title()
        return globals()[model_name].objects.all()
    except (KeyError, AttributeError):
        return None

class CombinedDataAPI(APIView):
    def get(self, request):
        combined_data = {}

        combined_data['persons'] = list(Person.objects.values())
        combined_data['room'] = list(Room.objects.values())
        combined_data['pet'] = list(Pet.objects.values())

        return Response(combined_data)



