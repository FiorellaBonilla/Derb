class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.tinyEditors = new Map();
        this.editor = null;
        this.apiData = null;
    }

    async fetchAPIData() {
        try {
            const response = await fetch('/api/combined_data/');
            if (!response.ok) {
                throw new Error('Error loading data from the API');
            }
            this.apiData = await response.json();
        } catch (error) {
            console.error(error.message);
        }
    }

    handleDragStart(event, model) {
        event.dataTransfer.setData('text/plain', JSON.stringify(model));
        this.showTinyMCEEditor(model);
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

    showTinyMCEEditor(model) {
        if (!this.tinyEditors.has(model.id)) {
            const models = document.createElement('div');
            models.className = 'form-field';
            models.textContent = model.name;
            this.formPreview.appendChild(models);
const self = this;
            tinymce.init({
                target: models,
                plugins: 'autolink lists media',
                toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
                setup: (editor) => {
                    editor.on('init', () => {
                        editor.setContent('');
                    });

                    editor.on('input', async (e) => {
                        let content = editor.getContent();

                        // Find all matches of {{...}}
                        const variableMatches = content.match(/\{\{([\w.]+)\}\}/g);

                        if (variableMatches) {
                            variableMatches.forEach((variable) => {
                                const cleanVariable = variable.match(/\{\{([\w.]+)\}\}/)[1];
                                const [modelPartial, fieldPartial] = cleanVariable.split('.');

                                if (this.apiData) {
                                    const matchingModels = Object.keys(this.apiData.models).filter(modelName =>
                                        modelName.startsWith(modelPartial)
                                    );

                                    const currentModel = this.apiData.models[modelPartial];
                                    let matchingFields = [];

                                    if (currentModel) {
                                        matchingFields = Object.keys(currentModel.fields).filter(fieldName =>
                                            fieldName.startsWith(fieldPartial)
                                        );
                                    }

                                    if (matchingModels.length > 0 && matchingFields.length > 0) {
                                        const suggestion = `{{${matchingModels[0]}.${matchingFields[0]}}}`;
                                        content = content.replace(variable, suggestion);
                                    } else if (matchingModels.length > 0) {
                                        const suggestion = `{{${matchingModels[0]}`;
                                        content = content.replace(variable, suggestion);
                                    }
                                }
                            });

                            editor.setContent(content);



                        }
                    });

                    editor.settings.forced_root_block = '';

                    this.tinyEditors.set(model.id, editor);
                }
            });
        }
    }

    getActiveEditor() {
            return this.tinyEditors.size > 0 ? [...this.tinyEditors.values()][0] : null;


    }

    async setupListeners() {
        await this.fetchAPIData();

        const availableModels = document.getElementById('available-models');

        const response_data = this.apiData;
        if (response_data && response_data.models) {
            Object.keys(response_data.models).forEach((modelName) => {
                const model = response_data.models[modelName];
                const draggableItem = document.createElement('div');
                draggableItem.className = 'draggable';
                draggableItem.draggable = true;
                draggableItem.textContent = modelName;

                draggableItem.addEventListener('dragstart', (e) => {
                    this.handleDragStart(e, { id: modelName, name: modelName });
                });

                availableModels.appendChild(draggableItem);
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const formBuilder = new FormBuilder();
    formBuilder.setupListeners();

    const saveButton = document.getElementById('save-button');
    saveButton.addEventListener('click', () => {
        const activeEditor = formBuilder.getActiveEditor();

        if (activeEditor) {
            const content = activeEditor.getContent();
            // Envía el contenido al servidor con la función SendDataAPI
            formBuilder.SendDataAPI(activeEditor.modelId, content);
        } else {
            console.error('No se encontró editor activo o contenido para guardar.');
        }
    });
});
