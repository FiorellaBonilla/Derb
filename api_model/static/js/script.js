function identifyReferences(content) {
    const regex = /{{(.*?)\.(.*?)}}/g;
    const references = [];
    let match;
    while ((match = regex.exec(content)) !== null) {
        const name = match[1]; // Asegúrate de que modelName sea el nombre del modelo en tu API
        const nameFields = match[2]; // Asegúrate de que fieldName sea el nombre del campo en tu API
        references.push({ name, nameFields });
    }
    return references;
}

// Función para obtener valores desde la API de respuesta
function obtenerValoresDesdeAPI(references) {
    const promises = references.map(reference => {
        const { modelName, fieldName } = reference;
        const apiUrl = `/api/response/?fieldsRes=${fieldName}`;
        return fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                return { referencia: reference, valor: data.responseF };
            });
    });

    return Promise.all(promises);
}

class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.modelFields = document.getElementById('model-fields');
        this.rightPanel = document.getElementById('right-panel');
        this.tinyEditors = new Map();
        this.sendButton = document.getElementById('send-button');
        this.customFormContainer = document.getElementById('custom-form-container');
        this.registros = [];
        this.textareasContainer = document.getElementById('textareas-container');
    }

  handleFormSubmit(event) {
    for (const [modelId, editor] of this.tinyEditors) {
        const content = editor.getContent();
        const references = identifyReferences(content);

        obtenerValoresDesdeAPI(references)
            .then(data => {
                // Reemplazar las referencias en el contenido con los valores
                data.forEach(item => {
                    const { referencia, valor } = item;
                    const { modelName, fieldName } = referencia;
                    const referenciaRegex = new RegExp(`{{${modelName}\\.${fieldName}}}`, 'g');
                    content = content.replace(referenciaRegex, valor);
                });

                // Guardar el contenido actualizado
                editor.setContent(content);
            })
            .catch(error => console.error('Error al obtener los valores desde la API:', error));

        // Luego, puedes continuar enviando los datos a la API como lo hacías antes
        this.SendDataAPI(modelId, content);
    }
}

    SendDataAPI(modelId, content) {
        const formData = {
    modelId: modelId,
    text: content
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
            editor.setContent('');
        });

        editor.on('change', () => {
            const content = editor.getContent();

        });

        editor.settings.forced_root_block = '';

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
