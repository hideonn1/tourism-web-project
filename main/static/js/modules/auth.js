/**
 * Authentication Module
 */
import { updateNav, showSection, showNotification, sectionTitles, updateTitle } from './ui.js';

export async function login(e, state) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (data.success) {
            state.user = data.usuario;
            // Clear login fields
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';

            updateNav(state);
            return true; // Signal success to caller (main.js)
        } else {
            const errorElement = document.getElementById('login-error');
            errorElement.innerText = data.message;
            setTimeout(() => {
                errorElement.innerText = '';
            }, 5000);
            return false;
        }
    } catch (error) {
        console.error('Error logging in:', error);
        return false;
    }
}

export async function logout(state) {
    await fetch('/api/logout', { method: 'POST' });
    state.user = null;
    updateNav(state);
    showSection('home', state);
}

export async function register(e) {
    e.preventDefault();
    const errorMsg = document.getElementById('register-error');
    errorMsg.innerText = '';

    const password = document.getElementById('reg-password').value;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[#$%&/!"?¿'@]).{8,}$/;

    if (!passwordRegex.test(password)) {
        errorMsg.innerText = 'La contraseña debe tener al menos 8 caracteres, letras, 1 número y 1 especial.';
        return;
    }

    const toTitleCase = (str) => str.replace(/\b\w/g, l => l.toUpperCase());

    const data = {
        nombres: toTitleCase(document.getElementById('reg-nombres').value),
        apellido_paterno: toTitleCase(document.getElementById('reg-paterno').value),
        apellido_materno: toTitleCase(document.getElementById('reg-materno').value),
        rut: document.getElementById('reg-rut').value,
        email: document.getElementById('reg-email').value,
        telefono: document.getElementById('reg-phone').value,
        password: document.getElementById('reg-password').value
    };

    try {
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (result.success) {
            const container = document.querySelector('#register .auth-container');
            container.innerHTML = `
                <div style="text-align: center; animation: fadeIn 0.5s;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 1rem;">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <h2 style="margin-bottom: 0.5rem;">¡Registro exitoso!</h2>
                    <p style="color: var(--secondary-text); margin-bottom: 2rem;">Tu cuenta ha sido creada correctamente.</p>
                    <button onclick="location.reload()" class="btn-primary" style="width: 100%;">Volver al inicio</button>
                </div>
            `;
        } else {
            errorMsg.innerText = result.message;
        }
    } catch (err) {
        errorMsg.innerText = 'Error de conexión';
    }
}

export async function checkSession(state) {
    try {
        const res = await fetch('/api/me');
        const data = await res.json();

        const urlParams = new URLSearchParams(window.location.search);
        const sectionParam = urlParams.get('section');
        let targetSection = 'home';

        // Simple XSS check for section param
        if (sectionParam && sectionTitles[sectionParam]) {
            targetSection = sectionParam;
        }

        if (data.success) {
            state.user = data.usuario;
            updateNav(state);

            if (targetSection === 'login') {
                // Return 'dashboard' to indicate main should load dashboard
                return 'dashboard';
            } else {
                return targetSection;
            }
        } else {
            return targetSection;
        }
    } catch (e) {
        return 'home';
    }
}

export function togglePasswordVisibility(btn, targetId = 'password') {
    const passwordInput = document.getElementById(targetId);
    const isPassword = passwordInput.getAttribute('type') === 'password';

    passwordInput.setAttribute('type', isPassword ? 'text' : 'password');

    if (isPassword) {
        btn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
        `;
        btn.style.color = 'var(--accent)';
    } else {
        btn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
            </svg>
        `;
        btn.style.color = '';
    }
}

export async function updateProfile(e) {
    e.preventDefault();
    const msg = document.getElementById('profile-msg');
    msg.innerText = 'Actualizando...';
    msg.style.color = '#fff';

    const email = document.getElementById('prof-email').value;
    const telefono = document.getElementById('prof-phone').value;

    try {
        const res = await fetch('/api/me', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, telefono })
        });

        const data = await res.json();

        if (data.success) {
            msg.innerText = 'Datos actualizados correctamente';
            msg.style.color = '#4ade80';
        } else {
            msg.innerText = 'Error: ' + data.message;
            msg.style.color = 'var(--error)';
        }
    } catch (e) {
        msg.innerText = 'Error al actualizar';
        msg.style.color = 'var(--error)';
    }
}
