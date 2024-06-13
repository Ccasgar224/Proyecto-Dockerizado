document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('access_token');

    if (token) {
        fetch('/index', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.body.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
            window.location.href = '/';
        });
    } else {
        window.location.href = '/';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            cerrarSesion();
        });
    }
});

function cerrarSesion() {
    localStorage.removeItem('access_token');
    window.location.href = '/';

}