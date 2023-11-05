document.addEventListener('DOMContentLoaded', () => {
    const responseContent = document.getElementById('response_content');
    const modelId = responseContent.getAttribute('data-model-id');

    fetch(`/api/tiny/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Request Error: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            let content = data.text;

            responseContent.innerHTML = content;
        })
        .catch(error => console.error('Request Error:', error));
});
