class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.modelFields = document.getElementById('model-fields');
        this.rightPanel = document.getElementById('right-panel');
        this.tinyEditors = new Map();
        this.init();

        this.sendButton = document.getElementById('send-button');
        this.sendButton.addEventListener('click', () => {
            const activeModelId = this.getActiveModelId();
            if (activeModelId) {
                const editor = this.tinyEditors.get(activeModelId);
                const content = editor.getContent();

                fetch('llenar_campos_modelo/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ contenido: content }),
                })
                    .then((response) => {
                        if (response.ok) {
                            // Realizar acciones adicionales si es necesario
                            console.log('Contenido enviado con éxito');
                        } else {
                            console.error('Error al enviar el contenido');
                        }
                    })
                    .catch((error) => {
                        console.error('Error en la solicitud:', error);
                    });
            }
        });
    }

    async init() {
        await this.loadModels();
        this.setupListeners();
    }

    async loadModels() {
        try {
            const response = await fetch('/api/models');
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

        fetch(`/api/models/get_model_info/${modelId}/`)
            .then(response => response.json())
            .then(data => {
                const fieldName = data.nameFields;
                const modelName = data.name;

                console.log(`Nombre del modelo: ${modelName}`);
                console.log(`Campo nameFields: ${fieldName}`);

                const modelFieldsList = document.getElementById('model-fields-list');

                if (modelFieldsList) {
                    const fieldListItem = document.createElement('li');
                    modelFieldsList.appendChild(fieldListItem);
                    fieldListItem.textContent = fieldName;

                    $('#model-details').collapse('show');
                }
            })
            .catch(error => {
                console.error('Error al obtener los campos del modelo:', error);
            });
    }

    showTinyMCEEditor(model) {
        if (this.tinyEditors.has(model.id)) {

            return;
        }

        const formField = document.createElement('div');
        formField.className = 'form-field';
        formField.textContent = model.name;
        this.formPreview.appendChild(formField);

        const editor = tinymce.init({
            target: formField,
            plugins: 'autolink lists media',
            toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
            setup: (editor) => {
                editor.on('init', () => {
                    editor.setContent('');
                });

                editor.on('change', () => {
                    const content = editor.getContent();
                    console.log('Contenido de TinyMCE:', content);
                });
            }
        });

        this.tinyEditors.set(model.id, editor);
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

document.addEventListener('DOMContentLoaded', () => {
    new FormBuilder();
});
