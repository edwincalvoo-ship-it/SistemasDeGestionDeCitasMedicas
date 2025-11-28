// Configuración de la API
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINTS = {
    // Auth
    login: '/api/auth/login',
    
    // Pacientes
    pacientes: '/api/pacientes',
    registrarPaciente: '/api/pacientes/registrar',
    
    // Doctores
    doctores: '/api/doctores',
    especialidades: '/api/doctores/especialidades/listar',
    
    // Horarios
    horarios: '/api/horarios',
    horariosDoctor: (id) => `/api/horarios/doctor/${id}`,
    
    // Citas
    citas: '/api/citas',
    actualizarEstadoCita: '/api/citas/actualizar_estado',
    
    // Historias
    historias: '/api/historias',
    
    // Facturas
    facturas: '/api/facturas',
    metodosPago: '/api/metodos-pago'
};

// Helpers para peticiones HTTP
async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers
    });
    
    return response.json();
}