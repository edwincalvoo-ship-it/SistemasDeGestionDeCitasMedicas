// Funciones principales del dashboard
function showSection(section) {
    // Redirigir a las páginas específicas
    const pages = {
        'pacientes': 'pacientes.html',
        'doctores': 'doctores.html',
        'citas': 'citas.html',
        'facturas': 'facturas.html'
    };
    
    if (pages[section]) {
        window.location.href = pages[section];
    }
}

// Proteger páginas que requieren autenticación
function requireAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}