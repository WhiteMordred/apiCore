document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login_form');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const login = loginForm.querySelector('[name="login"]').value; 
        const password = loginForm.querySelector('[name="password"]').value;

        const loginData = {
            login: login,
            password: password
        };

        fetch('/users_api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Connexion réussie") {
                fetchUserInfo(data.user_id);
                window.location.href = '/'; 
                console.error('Erreur lors de la connexion:', data.message);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la soumission du formulaire:', error);
        });
    });
    function fetchUserInfo(userId) {

        fetch(`/users_api/users/${userId}`)
        .then(response => response.json())
        .then(userData => {
            const userSessionData = {
                user_id: userData.user_id,
                name: userData.name,
                role: userData.role,
                email: userData.email,
                avatar: userData.avatar
            };
             sessionStorage.setItem('user', JSON.stringify(userSessionData));
            window.location.href = '/';
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des informations utilisateur:', error);
        });
    }
});

