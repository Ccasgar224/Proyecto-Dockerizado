document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('form').addEventListener('submit', function (e) {
        e.preventDefault();
        let formData = new FormData(this);
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.text().then(text => {
                try {
                    return JSON.parse(text);
                } catch (err) {
                    return text;
                }
            });
        })
        .then(data => {
            if (typeof data === 'string') { // Si es HTML
                document.body.innerHTML = data; 
            } else if (data.access_token) { // Si es JSON y tiene el token
                localStorage.setItem('access_token', data.access_token);
                // Redirige al index y añade el token en el header
                fetch('/index', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${data.access_token}`
                    }
                })
                .then(response => {
                    if (response.ok) {
                        return response.text(); 
                    } else {
                        throw new Error(response.statusText);
                    }
                })
                .then(data => {
                    // Inserta el HTML devuelto en el cuerpo de la página
                    document.body.innerHTML = data;
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Redireccionar a login si no está autorizado
                    window.location.href = '/login';
                });
            } else {
                throw new Error('No token received');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

