const formSubmitButton = document.getElementById('form_submit');
function cargarPreguntas() {
    fetch('/api/modelFields/')
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo cargar la lista de preguntas.');
            }
            return response.json();
        })
        .then(data => {
            const textareasContainer = document.getElementById('textareas-container');

            data.forEach(pregunta => {
                const preguntaDiv = document.createElement('div');
                preguntaDiv.className = 'pregunta';

                const tituloPregunta = document.createElement('h3');
                tituloPregunta.textContent = pregunta.nameFields;

                const textareaElement = document.createElement('textarea');
                textareaElement.style.width = '100%';
                textareaElement.style.height = '200px';

                textareaElement.setAttribute('data-question-id', pregunta.id);
                preguntaDiv.appendChild(tituloPregunta);
                preguntaDiv.appendChild(textareaElement);

                textareasContainer.appendChild(preguntaDiv);
            });
        })
        .catch(error => console.error('Error al cargar las preguntas:', error));
}


function enviarDatosALaAPIRespuestas() {
    const textareas = document.querySelectorAll('#textareas-container textarea');

    textareas.forEach((textarea) => {
        const preguntaID = +textarea.getAttribute('data-question-id');
        const respuesta = textarea.value;

        const respuestaActual = {
            "fieldsRes": preguntaID,
            "responseF": respuesta
        };

        // Enviar la respuesta actual a la API
        fetch('/api/response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(respuestaActual)
        })
        .then(response => {
            if (response.ok) {
                console.log('Datos enviados con éxito a la API de respuestas');
            } else {
                throw new Error('Error al enviar los datos a la API de respuestas.');
            }
        })
        .catch(error => console.error(error.message));
    });
}

formSubmitButton.addEventListener('click', function (event) {
    event.preventDefault();
    enviarDatosALaAPIRespuestas();
});

window.addEventListener('load', cargarPreguntas);
