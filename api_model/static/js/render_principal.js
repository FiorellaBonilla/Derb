document.addEventListener('DOMContentLoaded', () => {
    const responseContent = document.getElementById('response_content');
    const modelId = responseContent.getAttribute('data-model-id');  // Obtén el ID del modelo desde un atributo en el elemento HTML

    // Realiza una solicitud a la API de Tiny para obtener el contenido de tinyModel
    fetch(`/api/tiny/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Request Error: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // Procesa el contenido para reemplazar los marcadores
            let content = data.text;

            // Reemplaza los marcadores con los valores reales (puedes usar tu lógica de reemplazo aquí)

            // Muestra el contenido procesado en la página
            responseContent.innerHTML = content;
        })
        .catch(error => console.error('Request Error:', error));
});
