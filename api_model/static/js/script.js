class FormBuilder {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.formPreview = document.getElementById('form-preview');
        this.tinyEditors = new Map();
        this.editor = null; // Definimos editor como propiedad de la clase
    }

    handleDragStart(event, model) {
        event.dataTransfer.setData('text/plain', JSON.stringify(model));
        this.showTinyMCEEditor(model);
    }

    showTinyMCEEditor(model) {
        if (!this.tinyEditors.has(model.id)) {
            const formField = document.createElement('div');
            formField.className = 'form-field';
            formField.textContent = model.name;
            this.formPreview.appendChild(formField);

            this.editor = tinymce.init({
                target: formField,
                plugins: 'autolink lists media',
                toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
                setup: (editor) => {
                    editor.on('init', () => {
                        editor.setContent('');
                    });
                }
            });

            this.tinyEditors.set(model.id, this.editor);
        }
    }

    async setupListeners() {
        try {
            const response = await fetch('/api/combined_models/');
            if (!response.ok) {
                throw new Error('Error loading combined models from the API');
            }
            const models = await response.json();

            const availableModels = document.getElementById('available-models');

            models.forEach((model) => {
                const draggableItem = document.createElement('div');
                draggableItem.className = 'draggable';
                draggableItem.draggable = true;
                draggableItem.textContent = model.name;

                draggableItem.addEventListener('dragstart', (e) => {
                    this.handleDragStart(e, model);
                });

                availableModels.appendChild(draggableItem);
            });
        } catch (error) {
            console.error(error.message);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const formBuilder = new FormBuilder();
    formBuilder.setupListeners();
});
