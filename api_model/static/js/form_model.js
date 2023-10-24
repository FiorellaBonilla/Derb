const formSubmitButton = document.getElementById('form_submit');
function loadQuestions() {
    fetch('/api/modelFields/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load the list of questions.');
            }
            return response.json();
        })
        .then(data => {
            const textareasContainer = document.getElementById('textareas-container');

            data.forEach(question => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question';

                const questionTitle = document.createElement('h3');
                questionTitle.textContent = question.nameFields;

                const textareaElement = document.createElement('textarea');
                textareaElement.style.width = '30%';
                textareaElement.style.height = '30px';

                textareaElement.setAttribute('data-question-id', question.id);
                questionDiv.appendChild(questionTitle);
                questionDiv.appendChild(textareaElement);

                textareasContainer.appendChild(questionDiv);
            });
        })
        .catch(error => console.error('Error loading questions:', error));
}


function sendDataToAPIResponses() {
    const textareas = document.querySelectorAll('#textareas-container textarea');

    textareas.forEach((textarea) => {
        const questionID = +textarea.getAttribute('data-question-id');
        const response = textarea.value;

        const currentResponse = {
            "fieldsRes": questionID,
            "responseF": response
        };

        // Send the current response to the API
        fetch('/api/response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentResponse)
        })
        .then(response => {
            if (response.ok) {
                console.log('Data sent successfully to the responses API');
            } else {
                throw new Error('Error sending data to the responses API.');
            }
        })
        .catch(error => console.error(error.message));
    });
}

formSubmitButton.addEventListener('click', function (event) {
    event.preventDefault();
    sendDataToAPIResponses();
});

window.addEventListener('load', loadQuestions);
