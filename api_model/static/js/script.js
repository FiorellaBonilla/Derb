class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.modelFields = document.getElementById('model-fields');
        this.fieldList = document.getElementById('field-list');
        this.tinyEditor = null;
        this.init();
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
                    plugins: 'autolink lists media table',
                    toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
                    setup: (editor) => {
                        editor.on('init', () => {
                            editor.setContent('');
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