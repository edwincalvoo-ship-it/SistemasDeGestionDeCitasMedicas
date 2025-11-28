/* frontend/js/auth.js — versión tolerante a distintos ids */

async function login(event) {
    if (event && typeof event.preventDefault === 'function') event.preventDefault();

    // Intentar varios ids posibles (compatibilidad)
    const emailEl =
        document.getElementById('login-email') ||
        document.getElementById('email') ||
        null;
    const passwordEl =
        document.getElementById('login-password') ||
        document.getElementById('password') ||
        null;
    const errId = 'login-error';

    if (!emailEl || !passwordEl) {
        console.warn('login: elementos de formulario no encontrados', { email: !!emailEl, password: !!passwordEl });
        const err = document.getElementById(errId);
        if (err) {
            err.textContent = 'Formulario de login incompleto en esta página.';
            err.classList.remove('hidden');
            setTimeout(() => err.classList.add('hidden'), 5000);
        }
        return;
    }

    const email = (emailEl.value || '').trim();
    const password = passwordEl.value || '';

    if (!email || !password) {
        showError(errId, 'Por favor ingresa correo y contraseña.');
        return;
    }

    try {
        const result = await apiFetch(API_ENDPOINTS.login, {
            method: 'POST',
            skipAuth: true,
            body: JSON.stringify({ correo: email, contrasena: password })
        });

        console.log('LOGIN RESULT:', result);

        if (result && result.success) {
            localStorage.setItem('token', result.data.access_token);
            localStorage.setItem('user', JSON.stringify(result.data.usuario || {}));
            showDashboard();
        } else {
            const mensaje = result && result.mensaje ? result.mensaje : 'Credenciales inválidas';
            showError(errId, mensaje);
        }
    } catch (error) {
        console.error('Fetch error (network/CORS):', error);
        showError(errId, 'Error de conexión. Verifica que el servidor esté corriendo.');
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    if (window.location.pathname.endsWith('/index.html') || window.location.pathname === '/') {
        location.reload();
    } else {
        window.location.href = 'index.html';
    }
}

function checkAuth() {
    const token = localStorage.getItem('token');
    if (token) {
        try { showDashboard(); } catch (e) { console.warn('checkAuth fallo', e); }
    }
}

function showDashboard() {
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const userInfo = document.getElementById('user-info');
    const userEmail = document.getElementById('user-email');

    if (loginSection && dashboardSection) {
        loginSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
    }

    if (userInfo) userInfo.classList.remove('hidden');

    try {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        if (userEmail && user?.correo) userEmail.textContent = user.correo;
    } catch (e) {
        console.warn('No se pudo parsear usuario en localStorage', e);
    }
}

function showError(elementId, message) {
    const errorDiv = document.getElementById(elementId);
    if (!errorDiv) {
        console.error(`showError: elemento no encontrado (${elementId}):`, message);
        return;
    }
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => errorDiv.classList.add('hidden'), 5000);
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) loginForm.addEventListener('submit', login);
    try { checkAuth(); } catch (e) { console.warn('checkAuth fallo', e); }
});