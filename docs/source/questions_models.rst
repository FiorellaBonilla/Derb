JavaScript code (script.js)
Form Builder Class
Builder
sidebar: DOM element for the sidebar.
formPreview: DOM element for the form preview.
tinyEditors: Map to store TinyMCE editor instances.
editor: Variable to store the currently active editor.
apiData: Stores data retrieved from the API.
Methods
fetchAPIData(): Makes an asynchronous request to get data from the /api/combined_data/ API.

handleDragStart(event, model): Handles the drag start event, setting the model data and displaying the TinyMCE editor.

SendDataAPI(modelId, content): Send data to the server using fetch to update the model and content in the API.

showTinyMCEEditor(model): Displays a TinyMCE editor for a specific model and performs variable replacements on the content of the editor.

getActiveEditor(): Gets the current active editor.

setupListeners(): Configures DOM listeners, including loading API data and creating draggable elements.

DOMContentLoaded Listener
Configure the FormBuilder and set listeners for the save and help buttons.
Get API request
Makes a request to get data from the /api/tiny/ API and displays the results in the DOM.
Python code (views.py)
FormModelLoader class
Methods
loadFormModel(modelId): Loads a form model via an API request.


DOMContentLoaded Listener
Instances FormModelLoader and loads a form model based on the URL.
HTML Template Code (template.html)
JavaScript Blocks
Main block: script.js

Includes the necessary libraries and scripts.
Defines the behavior of the user interface, such as initial loading, dragging, and manipulating the content of the TinyMCE.
render_view.js block

Defines the behavior of the rendered view.
CSS Blocks
Main block: styleDragAndDrop.css

Styles for the form builder.
render_view.css block

Styles for the rendered view.
HTML blocks
Main block: content

Contains the main structure of the form builder, including sidebars and drop areas.
render_view block

Displays the result of the rendered view with a return button to the main page.
create_form block

Form for creating new forms.
Python code (models.py)
Data models are defined:
tinyModel:
class tinyModel(models.Model):
    text = models.TextField(blank=True, null=True)

    def __str__(self):

        return self.text

FormModel:
class FormModel(models.Model):
    title = models.CharField(max_length=200)
    description_model = models.TextField(blank=True, null=True)
    model_pre = models.ManyToManyField(tinyModel)

    def __str__(self):

        return self.title

Person
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ID Number: {self.id_number}'


Room
class Room(models.Model):
    physical_address = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    occupants_count = models.IntegerField()

    def __str__(self):
        return f'Address: {self.physical_address} - Color: {self.color} - Occupants: {self.occupants_count}'


Pet
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

Python code (urls.py)
The following routes are defined:
urlpatterns =  [
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('create/', form, name='create'),
    path('api_model_view/<int:form_id>/', api_model_view, name='api_model_view'),
    path('api/combined_models/', views.CombinedModelList.as_view(), name='combined-model-list'),
    path('api/combined_data/', views.CombinedDataList.as_view(), name='combined-data-list'),
    path('render_principal/<int:form_id>/<int:tiny_id>/', views.render_principal, name='render_principal'),
    path('render_view_model/<int:pk>/', views.DescriptorDetailView.as_view(), name='descriptor-detail'),
    path('CombinedDataAPI/', views.CombinedDataAPI.as_view(), name='CombinedDataAPI'),

]

Python code (api.py)
TinySerializer:
class tinySerializer(serializers.ModelSerializer):

    class Meta:
        model = tinyModel
        fields = '__all__'

formModelSerializer:
class formModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False);
    class Meta:
        model = FormModel
        fields = '__all__'

PersonSerializer:
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

RoomSerializer:
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

PetSerializer:
class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

CombinedDataSerializer:
class CombinedDataSerializer(serializers.Serializer):
    persons = PersonSerializer(many=True)
    rooms = RoomSerializer(many=True)
    pets = PetSerializer(many=True)

tinyViewset:
class tinyViewset(viewsets.ModelViewSet):
    queryset = tinyModel.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = tinySerializer

FormModelViewset:
class FormModelViewset(viewsets.ModelViewSet):
    queryset = FormModel.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = formModelSerializer



Additional Documentation
The app uses the Django framework for the backend and JavaScript with libraries like TinyMCE and SweetAlert for the frontend.
The application allows drag and drop form building, with rich content provided by TinyMCE.
The rendered view displays stored information and provides a link back to the main page.

How is it used?
Step 1:
First, we are greeted by the home page, with the option that we must first create a form
Step 2:
By clicking on the create form button, it will take us to the view to create the form, where a title and description of the form must be given,
and send to the form.
Step #3: When the send button is clicked, it will take us to the next page, where the available models are located,
and if you want to use them, drag the model and then enter the desired information and click the save button. There is also a help button, which indicates how to fill out the information.
in the tinymce.
Step #4: Once the information is sent, we access the render_principal/1/1 url, which would be the id of the created form and the context.
It would show us the context found in that form.
