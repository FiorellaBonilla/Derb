tinymce.PluginManager.add('custom_placeholder', function(editor) {
    editor.on('BeforeSetContent', function(e) {
        e.content = e.content.replace(/\{\{([^}]+)\}\}/g, function(match, placeholder) {
            return '<span class="custom-placeholder" contenteditable="false">' + placeholder + '</span>';
        });
    });

    editor.on('PostProcess', function(e) {
        if (e.get) {
            e.content = e.content.replace(/<span class="custom-placeholder"[^>]+>([^<]+)<\/span>/g, '{{$1}}');
        }
    });
});

class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.modelFields = document.getElementById('model-fields');
        this.rightPanel = document.getElementById('right-panel');
        this.tinyEditor = null;
        this.init();
    }

    async init() {
        await this.loadModels();
        await this.loadQuestions(); // Cargar las preguntas al iniciar la aplicación
        this.setupListeners();

        const showButton = document.getElementById('showButton');

        if (showButton) {
            showButton.addEventListener('click', () => {
                window.location.href = 'rendered_template/';
            });
        }
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

    async loadQuestions() {
        try {
            const response = await fetch('/api/formwithquestions/');
            if (!response.ok) {
                throw new Error('Error loading questions from the API');
            }
            const questions = await response.json();

            // Agrega las preguntas a la lista de preguntas
            this.createQuestionElements(questions);
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
            });

            this.sidebar.appendChild(draggableItem);
        });
    }

    createDraggableModels(models) {
        models.forEach((model) => {
            const draggableItem = document.createElement('div');
            draggableItem.className = 'draggable-model';
            draggableItem.draggable = true;
            draggableItem.textContent = model.name;

            draggableItem.addEventListener('click', () => {
                this.showModelFields(model);
            });

            this.rightPanel.appendChild(draggableItem);
        });
    }

    createQuestionElements(questions) {
        questions.forEach((question) => {
            const questionItem = document.createElement('div');
            questionItem.className = 'draggable-question';
            questionItem.draggable = true;
            questionItem.textContent = question.question_text;

            questionItem.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', JSON.stringify(question));
            });

            this.sidebar.appendChild(questionItem);
        });
    }

    showModelFields(model) {
    const modelId = model.id;

    fetch(`/api/models/get_model_info/${modelId}/`)
        .then(response => response.json())
        .then(data => {
            const fieldName = data.nameFields;
            const modelName = data.name; // Nombre real del modelo

            console.log(`Nombre del modelo: ${modelName}`);
            console.log(`Campo nameFields: ${fieldName}`);

            const modelFieldsList = document.getElementById('model-fields-list');
            const fieldListItem = document.createElement('li');
            modelFieldsList.appendChild(fieldListItem);
             fieldListItem.textContent = fieldName;

            $('#model-details').collapse('show');
        })
        .catch(error => {
            console.error('Error al obtener los campos del modelo:', error);
        });
}

    setupListeners() {
        this.formPreview.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        this.formPreview.addEventListener('dragleave', () => {
            this.fieldList.innerHTML = '';
            this.modelFields.style.display = 'none';
        });

        this.formPreview.addEventListener('drop', async (e) => {
            e.preventDefault();
            const modelData = JSON.parse(e.dataTransfer.getData('text/plain'));

            if (modelData) {
                const formField = document.createElement('div');
                formField.className = 'form-field';
                formField.textContent = modelData.name;
                this.formPreview.appendChild(formField);

                this.tinyEditor = tinymce.init({
                    target: formField,
                    plugins: 'autolink lists media table custom_placeholder', //
                    toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
                    setup: (editor) => {
                        editor.on('init', () => {
                            editor.setContent('');
                        });

                        editor.on('change', () => {
    const content = editor.getContent();

    // Realiza una solicitud AJAX al servidor para procesar y renderizar la plantilla
    fetch('/api/render_template/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de obtener el valor correcto del token CSRF
        },
        body: `content=${encodeURIComponent(content)}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.rendered_template) {
            // Actualiza la vista previa con la vista renderizada
            const contentDisplay = document.getElementById('contentDisplay');
            if (contentDisplay) {
                contentDisplay.innerHTML = data.rendered_template;
            }
        } else {
            console.error('Error al procesar y renderizar la plantilla en el servidor:', data.error);
        }
    })
    .catch(error => {
        console.error('Error en la solicitud AJAX:', error);
    });
});
                    }
                });
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new FormBuilder();
});

function replace_template_variables(content, context) {
    const regex = /\{\{([^}]+)\}\}/g;
    const processedContent = content.replace(regex, (match, placeholder) => {
        const replacement = context[placeholder] || match;
        return replacement;
    });

    return processedContent;
}
