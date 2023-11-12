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
    try {
      const response = await fetch(`/api/form/${formId}/`);
      if (!response.ok) {
        throw new Error('The form model could not be loaded.');
      }
      const formModel = await response.json();
      this.displayFormModel(formModel);
    } catch (error) {
      console.error('Error loading form model:', error);
    }
  }

  displayFormModel(formModel) {
    console.log(formModel.title);
    console.log(formModel.description_model);
    console.log(formModel.model_pre);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const formModelLoader = new FormModelLoader();
  const formModelId = window.location.pathname.split('/').filter(Boolean).pop();

  if (formModelId) {
    formModelLoader.loadFormModel(formModelId);
  } else {
    console.error('Form model ID not provided in URL.');
  }
});
