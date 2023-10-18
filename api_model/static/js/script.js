class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.modelFields = document.getElementById('model-fields');
        this.rightPanel = document.getElementById('right-panel');
        this.tinyEditors = new Map();
        this.sendButton = document.getElementById('send-button');
        this.customFormContainer = document.getElementById('custom-form-container'); // Agrega un contenedor para los campos personalizados
        this.registros = []; // Para almacenar los campos personalizados
        this.textareasContainer = document.getElementById('textareas-container'); // Contenedor de textareas personalizadas
    }

    handleFormSubmit(event) {

        for (const [modelId, editor] of this.tinyEditors) {
            const content = editor.getContent();
            this.enviarDatosALaAPI(modelId, content);
        }
    }

    enviarDatosALaAPI(modelId, content) {
        const formData = {
    modelId: modelId,
    text: content  // Asegúrate de que el nombre del campo coincida con el modelo Django
};
    console.log(formData);
        fetch('/api/tiny/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                console.log('Datos enviados con éxito a la API');
            } else {
                console.error('Error al enviar los datos a la API');
            }
        })
        .catch(error => {
            console.error('Error al enviar los datos a la API:', error);
        });
    }

    async setApiUrls(modelsApiUrl, modelInfoApiUrl) {
        this.modelsApiUrl = modelsApiUrl;
        this.modelInfoApiUrl = modelInfoApiUrl;
        await this.init();
    }

    async init() {
        this.sendButton.addEventListener('click', () => {
            this.handleFormSubmit();
        });
        if (!this.modelsApiUrl || !this.modelInfoApiUrl) {
            throw new Error('API URLs not defined');
        }

        try {
            const response = await fetch(this.modelsApiUrl);
            if (!response.ok) {
                throw new Error('Error loading models from the API');
            }
            const models = await response.json();
            this.createDraggableElements(models);
            this.createDraggableModels(models);
        } catch (error) {
            console.error(error.message);
        }
    }

    createDraggableElements(models) {
        models.forEach((model) => {
            const draggableItem = document.createElement('div');
            draggableItem.className = 'draggable';
            draggableItem.draggable = true;
            draggableItem.textContent = model.name;

            draggableItem.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', JSON.stringify(model));
                this.showTinyMCEEditor(model);
            });

            this.sidebar.appendChild(draggableItem);
        });
    }

    createDraggableModels(models) {
        models.forEach((model) => {
            const draggableItem = document.createElement('div');
            draggableItem.className = 'draggable-model';
            draggableItem.textContent = model.name;

            draggableItem.addEventListener('click', () => {
                this.showModelFields(model);
                this.showTinyMCEEditor(model);
            });

            this.rightPanel.appendChild(draggableItem);
        });
    }

    showModelFields(model) {
        const modelId = model.id;
        const modelInfoUrl = `${this.modelInfoApiUrl}${modelId}/`;
        fetch(modelInfoUrl)
            .then(response => response.json())
            .then(data => {
                const fieldName = data.nameFields;
                const modelName = data.name;
                console.log(`Name of model: ${modelName}`);
                console.log(`NameFields: ${fieldName}`);
                const modelFieldsList = document.getElementById('model-fields-list');
                if (modelFieldsList) {
                    const fieldListItem = document.createElement('li');
                    modelFieldsList.appendChild(fieldListItem);
                    fieldListItem.textContent = fieldName;
                    $('#model-details').collapse('show');
                }
            })
            .catch(error => {
                console.error('Error fetching model info:', error);
            });
    }

   showTinyMCEEditor(model) {
    if (!this.tinyEditors.has(model.id)) {
        const formField = document.createElement('div');
        formField.className = 'form-field';
        formField.textContent = model.name;
        this.formPreview.appendChild(formField);

        tinymce.init({
    target: formField,
    plugins: 'autolink lists media',
    toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
    setup: (editor) => {
        editor.on('init', () => {
            editor.setContent(''); // Inicializa el contenido del editor a un valor por defecto
        });

        editor.on('change', () => {
            // Actualiza el contenido del editor al área de texto
            const content = editor.getContent();
            // Almacena el contenido en la variable adecuada
            // Puedes usar this.registros o cualquier otra estructura de datos
        });

        editor.settings.forced_root_block = ''; // Evita que se agreguen párrafos automáticamente

        this.tinyEditors.set(model.id, editor);
    }
});
    }
}

    fieldAlreadyAdded(fieldName) {
        const fieldListItems = document.querySelectorAll('#model-fields-list li');
        return Array.from(fieldListItems).some(item => item.textContent === fieldName);
    }

    setupListeners() {
        this.formPreview.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        this.formPreview.addEventListener('dragleave', () => {
            if (this.modelFields) {
                this.modelFields.style.display = 'none';
            }
        });
    }
}

const modelsApiUrl = '/api/models';
const modelInfoApiUrl = '/api/models/get_model_info/';

document.addEventListener('DOMContentLoaded', () => {
    const formBuilder = new FormBuilder();
    formBuilder.setApiUrls(modelsApiUrl, modelInfoApiUrl);
});
