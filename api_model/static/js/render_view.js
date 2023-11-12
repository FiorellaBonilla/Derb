fetch('/api/tiny/')
  .then(response => {
    if (!response.ok) {
      throw new Error(`Request Error: ${response.status} - ${response.statusText}`);
    }
    return response.json();
  })
  .then(data => {
    const responseContent = document.getElementById('response_content');

    if (data.length > 0) {
      const ul = document.createElement('ul');
      ul.className = 'response-list';

      data.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `Information entered in Tiny: ${item.text}`;
        ul.appendChild(li);
      });
      responseContent.appendChild(ul);
    } else {
      responseContent.innerHTML = 'No related information found.';
    }
  })
  .catch(error => console.error('Request Error:', error));
async function saveContentToApi(content) {
    try {
        const response = await fetch('/api/tiny/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: content }), // send content of server
        });
        if (!response.ok) {
            throw new Error(`Request Error: ${response.status} - ${response.statusText}`);
        }
        console.log('Content saved successfully');
    } catch (error) {
        console.error('Request Error:', error);
    }
}

class FormModelLoader {
  async loadFormModel(modelId) {
  console.log('este es el form',form_id);
    try {
      const response = await fetch(`/api/form/${formId}/`);
      if (!response.ok) {
        throw new Error('No se pudo cargar el modelo de formulario.');
      }
      const formModel = await response.json();
      this.displayFormModel(formModel);
    } catch (error) {
      console.error('Error al cargar el modelo de formulario:', error);
    }
  }

  displayFormModel(formModel) {
    // Lógica para mostrar el modelo de formulario en tu interfaz.
    console.log(formModel.title);
    console.log(formModel.description_model);
    console.log(formModel.model_pre);  // Esto será una lista de IDs de objetos tinyModel.
    // Puedes agregar más lógica según tus necesidades.
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const formModelLoader = new FormModelLoader();
  const formModelId = window.location.pathname.split('/').filter(Boolean).pop();

  if (formModelId) {
    formModelLoader.loadFormModel(formModelId);
  } else {
    console.error('ID del modelo de formulario no proporcionado en la URL.');
  }
});
