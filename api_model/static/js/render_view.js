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
