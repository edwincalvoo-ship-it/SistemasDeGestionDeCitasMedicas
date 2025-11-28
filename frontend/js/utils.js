// Utilidades comunes para el frontend

/**
 * Muestra un mensaje toast con animación suave
 */
function showToast(message, type = 'info') {
    const colors = {
        'success': 'bg-green-500',
        'error': 'bg-red-500',
        'warning': 'bg-yellow-500',
        'info': 'bg-blue-500'
    };

    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };

    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300 transform translate-x-full opacity-0`;
    toast.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-${icons[type]}"></i>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(toast);

    // Animar entrada (slide desde la derecha)
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
            toast.classList.add('translate-x-0', 'opacity-100');
        });
    });

    // Remover después de 3 segundos con animación
    setTimeout(() => {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Confirmar acción con modal - transición suave
 */
function confirmAction(message, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-0 flex items-center justify-center z-50 transition-all duration-300';
    modal.innerHTML = `
        <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 transform scale-95 opacity-0 transition-all duration-300">
            <div class="mb-4">
                <i class="fas fa-exclamation-triangle text-yellow-500 text-3xl mb-2"></i>
                <h3 class="text-xl font-bold text-gray-800">Confirmar Acción</h3>
            </div>
            <p class="text-gray-600 mb-6">${message}</p>
            <div class="flex justify-end space-x-2">
                <button class="cancel-btn px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition">
                    Cancelar
                </button>
                <button class="confirm-btn px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition">
                    Confirmar
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Animar entrada con requestAnimationFrame para suavidad
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            modal.classList.remove('bg-opacity-0');
            modal.classList.add('bg-opacity-50');
            const content = modal.querySelector('div > div');
            content.classList.remove('scale-95', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
        });
    });

    // Función para cerrar con animación
    const closeModal = () => {
        modal.classList.add('bg-opacity-0');
        const content = modal.querySelector('div > div');
        content.classList.add('scale-95', 'opacity-0');
        setTimeout(() => modal.remove(), 300);
    };

    // Event listeners
    modal.querySelector('.cancel-btn').onclick = closeModal;
    modal.querySelector('.confirm-btn').onclick = () => {
        closeModal();
        setTimeout(() => onConfirm(), 150);
    };

    // Cerrar al hacer clic fuera del modal
    modal.onclick = (e) => {
        if (e.target === modal) closeModal();
    };
}

/**
 * Formatea fecha a formato local
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Formatea hora
 */
function formatTime(timeString) {
    return timeString.substring(0, 5);
}

/**
 * Formatea moneda
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

/**
 * Valida email
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Valida teléfono colombiano
 */
function isValidPhone(phone) {
    const regex = /^[0-9]{7,10}$/;
    return regex.test(phone.replace(/\s/g, ''));
}

/**
 * Valida documento (cédula)
 */
function isValidDocument(doc) {
    const regex = /^[0-9]{6,10}$/;
    return regex.test(doc);
}

/**
 * Muestra loader
 */
function showLoader(element) {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.className = 'flex items-center justify-center py-8';
    loader.innerHTML = `
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    `;
    element.innerHTML = '';
    element.appendChild(loader);
}

/**
 * Oculta loader
 */
function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) loader.remove();
}

/**
 * Debounce para búsquedas
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Calcula edad desde fecha de nacimiento
 */
function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    return age;
}

/**
 * Exportar a CSV
 */
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function convertToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];
    
    for (const row of data) {
        const values = headers.map(header => {
            const value = row[header];
            return `"${value}"`;
        });
        csvRows.push(values.join(','));
    }
    
    return csvRows.join('\n');
}

/**
 * Copiar al portapapeles
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copiado al portapapeles', 'success');
    } catch (err) {
        showToast('Error al copiar', 'error');
    }
}

/**
 * Imprimir elemento
 */
function printElement(elementId) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '', 'height=600,width=800');
    
    printWindow.document.write('<html><head><title>Imprimir</title>');
    printWindow.document.write('<link href="https://cdn.tailwindcss.com" rel="stylesheet">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    
    printWindow.document.close();
    printWindow.print();
}

/**
 * Genera ID único
 */
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * Sistema de Permisos por Rol
 */
const Permissions = {
    // Obtener usuario actual
    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    // Verificar si es admin
    isAdmin() {
        const user = this.getCurrentUser();
        return user && user.rol === 'admin';
    },

    // Verificar si es doctor
    isDoctor() {
        const user = this.getCurrentUser();
        return user && user.rol === 'doctor';
    },

    // Verificar si es paciente
    isPaciente() {
        const user = this.getCurrentUser();
        return user && user.rol === 'paciente';
    },

    // Verificar permiso específico
    can(action) {
        const user = this.getCurrentUser();
        if (!user) return false;

        const permissions = {
            // Pacientes
            'registrar_paciente': ['admin', 'doctor'],
            'ver_pacientes': ['admin', 'doctor'],
            'eliminar_paciente': ['admin'],

            // Doctores
            'registrar_doctor': ['admin'],
            'ver_doctores': ['admin', 'doctor', 'paciente'],
            'editar_doctor': ['admin'],
            'eliminar_doctor': ['admin'],

            // Horarios
            'crear_horario': ['admin'],
            'ver_horarios': ['admin', 'doctor'],
            'eliminar_horario': ['admin'],

            // Citas
            'crear_cita': ['admin', 'doctor', 'paciente'],
            'ver_todas_citas': ['admin'],
            'ver_mis_citas': ['admin', 'doctor', 'paciente'],
            'editar_cita': ['admin', 'doctor'],
            'cancelar_cita': ['admin', 'doctor', 'paciente'],

            // Historias
            'crear_historia': ['doctor'],
            'ver_historias': ['admin', 'doctor'],

            // Facturas
            'crear_factura': ['admin'],
            'ver_todas_facturas': ['admin'],
            'ver_mis_facturas': ['admin', 'doctor', 'paciente'],

            // Reportes
            'ver_reportes': ['admin', 'doctor']
        };

        const allowedRoles = permissions[action];
        return allowedRoles && allowedRoles.includes(user.rol);
    },

    // Obtener ID del usuario según su rol
    getUserId() {
        const user = this.getCurrentUser();
        if (!user) return null;

        // Retornar el ID apropiado según el rol
        if (user.rol === 'paciente') return user.id_paciente;
        if (user.rol === 'doctor') return user.id_doctor;
        return user.id_usuario;
    }
};

/**
 * Ocultar elemento si no tiene permiso
 */
function hideIfNoPermission(elementId, permission) {
    if (!Permissions.can(permission)) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
        }
    }
}

/**
 * Mostrar mensaje de permiso denegado
 */
function showPermissionDenied() {
    showToast('No tienes permisos para realizar esta acción', 'error');
}