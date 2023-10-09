$(document).ready(function () {
    const sidebar = document.getElementById('sidebar');
    const formPreview = document.getElementById('form-preview');
    const modelFields = document.getElementById('model-fields');
    const fieldList = document.getElementById('field-list');
    let tinyEditor = null;

    // Make a GET request to the API to get the list of models
    $.ajax({
        url: '/api/models',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            const models = data;

            // Create draggable and droppable elements for each model
            models.forEach(function (model) {
                const draggableItem = document.createElement('div');
                draggableItem.className = 'draggable';
                draggableItem.draggable = true;
                draggableItem.textContent = model.name;

                draggableItem.addEventListener('dragstart', function (e) {
                    e.dataTransfer.setData('text/plain', JSON.stringify(model));
                });

                sidebar.appendChild(draggableItem);
            });
        },
        error: function () {
            console.error('Error loading models from the API');
        }
    });

    formPreview.addEventListener('dragover', function (e) {
        e.preventDefault();
    });

    formPreview.addEventListener('dragleave', function () {
        fieldList.innerHTML = '';
        modelFields.style.display = 'none';
    });

    formPreview.addEventListener('drop', async function (e) {
        e.preventDefault();
        const modelData = JSON.parse(e.dataTransfer.getData('text/plain'));

        if (modelData) {
            const formField = document.createElement('div');
            formField.className = 'form-field';
            formField.textContent = modelData.name;
            formPreview.appendChild(formField);

            tinyEditor = tinymce.init({
                target: formField,
                plugins: 'autolink lists media table',
                toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | table | media | link',
                setup: function (editor) {
                    editor.on('init', function () {
                        editor.setContent('');
                    });
                }
            });

            // Make a request to the API to get the fields of the selected model
            try {
                const response = await fetch(`/api/fields/${modelData.id}`);
                if (response.ok) {
                    const fieldsData = await response.json();

                    // Display the fields of the model in the "Selected Model Fields" area
                    fieldList.innerHTML = '';
                    fieldsData.forEach(function (field) {
                        const listItem = document.createElement('li');
                        listItem.textContent = field.name;
                        fieldList.appendChild(listItem);
                    });
                    modelFields.style.display = 'block';
                } else {
                    console.error('Error getting fields of the model from the API');
                }
            } catch (error) {
                console.error('Network error:', error);
            }
        }
    });
});
