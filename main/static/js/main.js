document.addEventListener('DOMContentLoaded', () => {
    checkSession();
    loadTheme();
});

const state = {
    user: null,
    currentPaquetes: [],
    galleryImages: [],
    galleryIndex: 0
};

// Helper to update page title
function updateTitle(sectionName) {
    document.title = `${sectionName} - Explora360`;
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        updateThemeIcon(true);
    }
}

function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    updateThemeIcon(isLight);
}

function updateThemeIcon(isLight) {
    const icon = document.getElementById('theme-icon');
    const logo = document.getElementById('nav-logo');

    // Update Theme Toggle Icon immediately
    if (isLight) {
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
    } else {
        icon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    }

    // Update Logo with Fade Animation
    if (logo) {
        // Start Fade Out
        logo.classList.add('fade-out');

        // Wait for fade out to finish (300ms matches css), then swap source and fade in
        setTimeout(() => {
            if (isLight) {
                logo.src = '/static/img/favicon-light.svg';
            } else {
                logo.src = '/static/img/favicon-dark.svg';
            }
            // Start Fade In
            logo.classList.remove('fade-out');
        }, 300);
    }
}

function showSection(sectionId) {
    const target = document.getElementById(sectionId);
    if (!target) return;

    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
    });
    target.classList.add('active');

    // Reset Nav to default state based on user status
    updateNav();

    // Specific overrides for current section
    if (sectionId === 'login') {
        const navLogin = document.getElementById('nav-login');
        if (navLogin) navLogin.style.display = 'none';
    }

    if (sectionId === 'home') {
        const navHome = document.getElementById('nav-home');
        if (navHome) navHome.style.display = 'none';
    }

    if (sectionId === 'public-destinos') {
        const navDestinos = document.getElementById('nav-destinos');
        if (navDestinos) navDestinos.style.display = 'none';
    }

    // Update Title dynamically
    switch (sectionId) {
        case 'home': document.title = 'Explora360 Chile | Viajes y Turismo'; break;
        case 'login': updateTitle('Iniciar Sesión'); break;
        case 'register': updateTitle('Registro'); break;
        case 'admin-dashboard': updateTitle('Panel de Administración'); break;
        case 'client-dashboard': updateTitle('Panel de Cliente'); break;
        case 'profile-section': updateTitle('Mi Perfil'); break;
        case 'public-destinos': updateTitle('Nuestros Destinos'); break;
    }
}

function updateNav() {
    const navHome = document.getElementById('nav-home');
    if (!navHome) return; // Exit if nav elements don't exist (e.g. secondary pages)

    if (state.user) {
        navHome.style.display = 'none';
        document.getElementById('nav-login').style.display = 'none';
        document.getElementById('nav-destinos').style.display = 'none';
        document.getElementById('nav-dashboard').style.display = 'inline-block';
        document.getElementById('nav-logout').style.display = 'inline-block';
    } else {
        navHome.style.display = 'inline-block';
        document.getElementById('nav-login').style.display = 'inline-block';
        document.getElementById('nav-destinos').style.display = 'inline-block';
        document.getElementById('nav-dashboard').style.display = 'none';
        document.getElementById('nav-logout').style.display = 'none';
    }
}

function showDashboard() {
    if (!state.user) return showSection('login');

    if (state.user.rol === 'Administrador') {
        resetWelcomeText();
        document.getElementById('admin-content').innerHTML = ''; // Clear previous content
        showSection('admin-dashboard');
    } else {
        resetClientHeader();
        document.getElementById('client-content').innerHTML = ''; // Clear previous content
        showSection('client-dashboard');
    }
}

async function login(e) {
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
            updateNav();
            showDashboard();
        } else {
            const errorElement = document.getElementById('login-error');
            errorElement.innerText = data.message;
            setTimeout(() => {
                errorElement.innerText = '';
            }, 5000); // Clear after 5 seconds
        }
    } catch (error) {
        console.error('Error logging in:', error);
    }
}

function togglePasswordVisibility(btn, targetId = 'password') {
    const passwordInput = document.getElementById(targetId);
    const isPassword = passwordInput.getAttribute('type') === 'password';

    passwordInput.setAttribute('type', isPassword ? 'text' : 'password');

    // Update Icon
    if (isPassword) {
        // Switch to Text (Visible) -> Show Eye Off (Slash)
        btn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
        `;
        btn.style.color = 'var(--accent)';
    } else {
        // Switch back to Password (Hidden) -> Show Eye
        btn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
            </svg>
        `;
        btn.style.color = ''; // Reset color
    }
}

async function logout() {
    await fetch('/api/logout', { method: 'POST' });
    state.user = null;

    // Clear login fields
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';

    updateNav();
    showSection('home');
}

document.getElementById('login-form').addEventListener('submit', login);

async function register(e) {
    e.preventDefault();
    const errorMsg = document.getElementById('register-error');
    errorMsg.innerText = '';

    // Front-end Password Validation
    const password = document.getElementById('reg-password').value;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[#$%&/!"?¿'@]).{8,}$/;

    if (!passwordRegex.test(password)) {
        errorMsg.innerText = 'La contraseña debe tener al menos 8 caracteres, letras, 1 número y 1 especial.';
        return;
    }

    // Capitalize names for frontend consistency
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
            // Replace form with success message (Minimalist & Professional)
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

function showNotification(message) {
    const toast = document.getElementById('notification-toast');
    toast.innerText = message;
    toast.className = 'notification-toast show';
    setTimeout(() => {
        toast.className = toast.className.replace('show', '');
    }, 3000);
}

// Admin Logic

// Refactored to be generic
function applyTransition(elementId) {
    const content = document.getElementById(elementId);
    content.classList.remove('admin-transition');
    void content.offsetWidth; // Trigger reflow
    content.classList.add('admin-transition');
}

function formatDateToSpanishLong(dateStr) {
    if (!dateStr) return '';
    const [year, month, day] = dateStr.split('-').map(Number);
    const date = new Date(year, month - 1, day);

    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    // Ensure we get the correct day of week for the specific date
    // Note: creating Date with (Y, M, D) uses local time 00:00:00. 
    // This is generally safe for finding the day of the week of a specific calendar date.
    const dayName = days[date.getDay()];
    const dayNum = String(day).padStart(2, '0');
    const monthName = months[date.getMonth()];

    return `${dayName} ${dayNum} de ${monthName} del ${year}`;
}

function formatCurrencyCLP(amount) {
    return Number(amount).toLocaleString('es-CL');
}

// Admin Logic

async function loadDestinos() {
    hideWelcomeText();
    updateTitle('Gestión de Destinos');
    const content = document.getElementById('admin-content');
    applyTransition('admin-content');

    content.innerHTML = `
        <div class="admin-top-bar" style="justify-content: center; gap: 2rem;">
            <h3>Gestión de Destinos</h3>
            <button onclick="showCreateDestinoForm()" class="btn-primary btn-sm">Nuevo Destino</button>
        </div>
        <div id="destinos-list" class="content-grid"></div>
    `;

    try {
        const res = await fetch('/api/destinos');
        const destinos = await res.json();

        const list = document.getElementById('destinos-list');
        list.className = 'content-area';
        list.innerHTML = '';

        destinos.forEach(d => {
            const card = document.createElement('div');
            card.className = 'card';
            const slug = d.nombre.toLowerCase()
                .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // Remove accents
                .replace(/ /g, '-')
                .replace(/[^\w-]+/g, '')
                .replace(/-+/g, '-');
            const imageUrl = `/static/img/${slug}.webp`;

            card.innerHTML = `
                <img src="${imageUrl}" class="card-img-top" alt="${d.nombre}" loading="lazy" onerror="this.src='https://via.placeholder.com/400x250?text=No+Image'">
                <div class="card-content">
                    <h4>${d.nombre}</h4>
                    <p><strong>Ubicación:</strong> ${d.ciudad}, ${d.pais}</p>
                    <p class="card-desc">${d.descripcion}</p>
                    <p class="card-activities"><strong>Actividades:</strong> ${d.actividades_disponibles}</p>
                    <div class="card-actions">
                        <button onclick="deleteDestino(${d.id_destino})" class="btn-danger btn-sm">Eliminar</button>
                    </div>
                </div>
            `;
            list.appendChild(card);
        });
    } catch (e) {
        content.innerHTML += `<p class="error-msg">Error cargando destinos: ${e.message}</p>`;
    }
}

async function loadPaquetes() {
    hideWelcomeText();
    updateTitle('Gestión de Paquetes');
    const content = document.getElementById('admin-content');
    applyTransition('admin-content');

    content.innerHTML = `
        <div class="admin-top-bar" style="justify-content: center; gap: 2rem;">
            <h3>Gestión de Paquetes</h3>
            <button onclick="showCreatePaqueteForm()" class="btn-primary btn-sm">Nuevo Paquete</button>
        </div>
        <div id="paquetes-list" class="content-grid"></div>
    `;

    try {
        const res = await fetch('/api/paquetes');
        state.currentPaquetes = await res.json();
        const paquetes = state.currentPaquetes;

        const list = document.getElementById('paquetes-list');
        list.className = 'content-area';
        list.innerHTML = '';

        paquetes.forEach(p => {
            let destinosHtml = '<ul>';
            if (p.destinos) {
                p.destinos.forEach(d => {
                    destinosHtml += `<li>${d.nombre} (${d.ciudad})</li>`;
                });
            }
            destinosHtml += '</ul>';

            // Collage Logic
            let collageHtml = '';
            if (p.destinos && p.destinos.length > 0) {
                const maxDestinos = p.destinos.slice(0, 4);
                collageHtml = `<div class="package-collage items-${maxDestinos.length}">`;
                maxDestinos.forEach((d, index) => {
                    const slug = d.nombre.toLowerCase()
                        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                        .replace(/ /g, '-')
                        .replace(/[^\w-]+/g, '')
                        .replace(/-+/g, '-');
                    collageHtml += `<img src="/static/img/${slug}.webp" alt="${d.nombre}" loading="lazy" 
                        onclick="openPackageGallery(${p.id_paquete}, ${index})" style="cursor: pointer;">`;
                });
                collageHtml += `</div>`;
            } else {
                collageHtml = `<div class="package-collage items-1"><img src="/static/img/default.webp" alt="Default"></div>`;
            }

            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                ${collageHtml}
                <div class="card-content">
                <h4>Paquete #${p.id_paquete}</h4>
                <p><strong>Fechas:</strong> ${formatDateToSpanishLong(p.fecha_salida)} hasta el ${formatDateToSpanishLong(p.fecha_llegada)}</p>
                <p><strong>Costo:</strong> $${formatCurrencyCLP(p.costo_destino)}</p>
                <p><strong>Cupos:</strong> ${p.cupos}</p>
                <div class="destinos-list">
                    <strong>Destinos:</strong>
                    ${destinosHtml}
                </div>
                 <div class="card-actions">
                    <button onclick="deletePaquete(${p.id_paquete})" class="btn-danger">Eliminar</button>
                </div>
                </div>
            `;
            list.appendChild(card);
        });
    } catch (e) {
        content.innerHTML += `<p class="error-msg">Error cargando paquetes: ${e.message}</p>`;
    }
}

// Client Logic

function hideClientHeader() {
    const title = document.getElementById('client-main-title');
    if (title) {
        title.classList.add('hidden-smooth');
    }
}

function resetClientHeader() {
    const title = document.getElementById('client-main-title');
    if (title) {
        title.classList.remove('hidden-smooth');
    }
}

async function loadAvailablePackages() {
    hideClientHeader();
    updateTitle('Paquetes Disponibles');
    const content = document.getElementById('client-content');
    applyTransition('client-content');

    // Ensure grid layout is active
    content.className = 'content-area';
    content.classList.add('content-area');

    content.innerHTML = '<p style="text-align:center; width:100%;">Cargando paquetes...</p>';

    try {
        const res = await fetch('/api/paquetes');
        state.currentPaquetes = await res.json();
        const paquetes = state.currentPaquetes;

        content.innerHTML = '';

        paquetes.forEach(p => {
            let destinosHtml = '<ul>';
            if (p.destinos) {
                p.destinos.forEach(d => {
                    destinosHtml += `<li>${d.nombre} (${d.ciudad})</li>`;
                });
            }
            destinosHtml += '</ul>';

            // Collage Logic
            let collageHtml = '';
            if (p.destinos && p.destinos.length > 0) {
                const maxDestinos = p.destinos.slice(0, 4);
                collageHtml = `<div class="package-collage items-${maxDestinos.length}">`;
                maxDestinos.forEach((d, index) => {
                    const slug = d.nombre.toLowerCase()
                        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                        .replace(/ /g, '-')
                        .replace(/[^\w-]+/g, '')
                        .replace(/-+/g, '-');
                    collageHtml += `<img src="/static/img/${slug}.webp" alt="${d.nombre}" loading="lazy" 
                        onclick="openPackageGallery(${p.id_paquete}, ${index})" style="cursor: pointer;">`;
                });
                collageHtml += `</div>`;
            } else {
                collageHtml = `<div class="package-collage items-1"><img src="/static/img/default.webp" alt="Default"></div>`;
            }

            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                ${collageHtml}
                <div class="card-content">
                    <h4>Paquete #${p.id_paquete}</h4>
                    <p><strong>Salida:</strong> ${formatDateToSpanishLong(p.fecha_salida)}</p>
                    <p><strong>Llegada:</strong> ${formatDateToSpanishLong(p.fecha_llegada)}</p>
                    <p><strong>Costo:</strong> $${formatCurrencyCLP(p.costo_destino)}</p>
                    <p><strong>Cupos:</strong> ${p.cupos}</p>
                    <div class="destinos-list">
                        <strong>Destinos:</strong>
                        ${destinosHtml}
                    </div>
                     <div class="card-actions">
                        <button onclick="reservarPaquete(${p.id_paquete}, ${p.cupos})" class="btn-primary" ${p.cupos <= 0 ? 'disabled' : ''}>
                            ${p.cupos > 0 ? 'Reservar' : 'Agotado'}
                        </button>
                    </div>
                </div>
            `;
            content.appendChild(card);
        });
    } catch (e) {
        content.innerHTML = `<p class="error-msg">Error: ${e.message}</p>`;
    }
}

// Public Destinos Logic

function showPublicDestinos() {
    showSection('public-destinos');
    loadPublicDestinos();
}

async function loadPublicDestinos() {
    updateTitle('Nuestros Destinos');
    const content = document.getElementById('public-destinos-content');

    // Smooth transition
    content.classList.remove('fade-in');
    void content.offsetWidth;
    content.classList.add('fade-in');

    content.innerHTML = '<p style="text-align:center; width:100%;">Cargando destinos...</p>';

    try {
        const res = await fetch('/api/destinos');
        const destinos = await res.json();

        content.innerHTML = '';

        if (destinos.length === 0) {
            content.innerHTML = '<p style="text-align:center; width:100%;">No hay destinos disponibles por el momento.</p>';
            return;
        }

        destinos.forEach(d => {
            const card = document.createElement('div');
            card.className = 'card';

            // Clean names for URL (Local WebP - Kebab Case)
            const slug = d.nombre.toLowerCase()
                .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                .replace(/ /g, '-')
                .replace(/[^\w-]+/g, '')
                .replace(/-+/g, '-');
            const imageUrl = `/static/img/${slug}.webp`;

            card.innerHTML = `
                <img src="${imageUrl}" class="card-img-top" alt="${d.nombre}" loading="lazy" onerror="this.src='https://via.placeholder.com/400x250?text=No+Image'">
                <div class="card-content">
                    <h4>${d.nombre}</h4>
                    <p><strong>Ubicación:</strong> ${d.ciudad}, ${d.pais}</p>
                    <p class="card-desc">${d.descripcion}</p>
                    <p class="card-activities"><strong>Actividades:</strong> ${d.actividades_disponibles}</p>
                </div>
            `;
            content.appendChild(card);
        });
    } catch (e) {
        content.innerHTML = `<p class="error-msg">Error: ${e.message}</p>`;
    }
}

// Custom Modal Utilities
function showCustomModal({ title, message, input = false, max = 1 }) {
    return new Promise((resolve) => {
        const modal = document.getElementById('custom-modal');
        const titleEl = document.getElementById('modal-title');
        const msgEl = document.getElementById('modal-msg');
        const inputEl = document.getElementById('modal-input');
        const btnConfirm = document.getElementById('modal-btn-confirm');
        const btnCancel = document.getElementById('modal-btn-cancel');

        titleEl.innerText = title;
        msgEl.innerText = message;

        // Reset state
        inputEl.value = '';

        if (input) {
            inputEl.style.display = 'block';
            inputEl.max = max;
            inputEl.placeholder = `Máximo ${max}`;
            inputEl.value = 1; // Default
            setTimeout(() => inputEl.focus(), 100);
        } else {
            inputEl.style.display = 'none';
        }

        modal.classList.add('active');

        // Handlers
        const close = (value) => {
            modal.classList.remove('active');
            // Clean up listeners to avoid dupes if reused without re-cloning (though simple here)
            btnConfirm.onclick = null;
            btnCancel.onclick = null;
            resolve(value);
        };

        btnConfirm.onclick = () => {
            if (input) {
                const val = parseInt(inputEl.value);
                if (val && val > 0 && val <= max) close(val);
                else {
                    inputEl.style.borderColor = 'var(--error)';
                    setTimeout(() => inputEl.style.borderColor = '', 1000);
                }
            } else {
                close(true);
            }
        };

        btnCancel.onclick = () => close(null);

        // Enter key support
        inputEl.onkeyup = (e) => {
            if (e.key === 'Enter') btnConfirm.click();
        };
    });
}

async function reservarPaquete(idPaquete, cuposDisponibles) {
    if (cuposDisponibles <= 0) {
        showCustomModal({
            title: 'Agotado',
            message: 'Lo sentimos, este paquete está agotado.'
        });
        return;
    }

    // Step 1: Ask for Quantity
    const quantity = await showCustomModal({
        title: 'Reservar Cupos',
        message: `¿Cuántos cupos deseas reservar? (Máximo ${cuposDisponibles})`,
        input: true,
        max: cuposDisponibles
    });

    if (!quantity) return; // Users cancelled

    // Step 2: Confirm
    const confirmed = await showCustomModal({
        title: 'Confirmación',
        message: `¿Estás seguro de reservar ${quantity} cupo(s)?`,
        input: false
    });

    if (!confirmed) return;

    try {
        const res = await fetch('/api/reservas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_paquete: idPaquete,
                cupos: quantity
            })
        });

        const result = await res.json();

        if (result.success) {
            // Success Modal
            await showCustomModal({
                title: '¡Éxito!',
                message: 'Tu reserva # ha sido creada exitosamente. ¡Prepárate para viajar!'
            });
            loadAvailablePackages(); // Refresh list to update quotas
        } else {
            // Failure Modal
            await showCustomModal({
                title: 'Error',
                message: result.message || 'No se pudo completar la reserva.'
            });
        }
    } catch (e) {
        // Connection Error Modal
        await showCustomModal({
            title: 'Error de Conexión',
            message: 'Ocurrió un problema al conectar con el servidor.'
        });
    }
}

async function loadMyReservations() {
    hideClientHeader();
    updateTitle('Mis Reservas');
    const content = document.getElementById('client-content');
    applyTransition('client-content');
    content.classList.add('content-area'); // Ensure grid

    content.innerHTML = '<p style="text-align:center; width:100%;">Cargando mis reservas...</p>';

    try {
        const res = await fetch('/api/mis-reservas');
        const reservas = await res.json();

        content.innerHTML = '';

        if (reservas.length === 0) {
            content.innerHTML = '<p style="text-align:center; width:100%;">No tienes reservas activas.</p>';
            return;
        }

        reservas.forEach(r => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h4>Reserva #${r.id_reserva}</h4>
                <p><strong>Paquete ID:</strong> ${r.id_paquete_turistico}</p>
                <p><strong>Cupos:</strong> ${r.cupos}</p>
                <p><strong>Estado:</strong> ${r.estado}</p>
            `;
            content.appendChild(card);
        });
    } catch (e) {
        content.innerHTML = `<p class="error-msg">Error: ${e.message}</p>`;
    }
}

// Forms

function showCreateDestinoForm() {
    const content = document.getElementById('admin-content');
    content.innerHTML = `
        <div class="create-form-container">
            <h3 style="margin-bottom: 1.5rem;">Nuevo Destino</h3>
            <form onsubmit="createDestino(event)" class="create-form">
                <input type="text" id="d-nombre" placeholder="Nombre" required>
                <input type="text" id="d-ciudad" placeholder="Ciudad" required>
                <input type="text" id="d-pais" placeholder="País" required>
                <input type="text" id="d-descripcion" placeholder="Descripción" required>
                <input type="text" id="d-actividades" placeholder="Actividades (sep. por comas)" required>
                <div style="margin-top: 1rem;">
                    <button type="submit" class="btn-primary">Guardar</button>
                    <button type="button" onclick="loadDestinos()" class="btn-secondary">Cancelar</button>
                </div>
            </form>
        </div>
    `;
}

async function createDestino(e) {
    e.preventDefault();
    const data = {
        nombre: document.getElementById('d-nombre').value,
        ciudad: document.getElementById('d-ciudad').value,
        pais: document.getElementById('d-pais').value,
        descripcion: document.getElementById('d-descripcion').value,
        actividades_disponibles: document.getElementById('d-actividades').value
    };

    const res = await fetch('/api/destinos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) loadDestinos();
    else alert('Error creando destino');
}

async function deleteDestino(id) {
    if (!confirm('¿Eliminar destino?')) return;
    const res = await fetch(`/api/destinos/${id}`, { method: 'DELETE' });
    if (res.ok) loadDestinos();
    else alert('Error eliminando destino');
}

async function showCreatePaqueteForm() {
    const content = document.getElementById('admin-content');

    let allDestinos = [];
    let selectedIds = new Set();

    // Continent Mapping Helper
    const getContinent = (pais) => {
        const p = pais.toLowerCase();
        if (['chile', 'argentina', 'perú', 'peru', 'brasil', 'colombia', 'uruguay', 'ecuador'].some(x => p.includes(x))) return 'Sudamérica';
        if (['estados unidos', 'méxico', 'mexico', 'canadá', 'canada'].some(x => p.includes(x))) return 'Norteamérica';
        if (['españa', 'francia', 'italia', 'alemania', 'inglaterra'].some(x => p.includes(x))) return 'Europa';
        if (['china', 'japón', 'japon', 'corea'].some(x => p.includes(x))) return 'Asia';
        return 'Otros';
    };

    // Render Function
    const renderList = (list) => {
        const container = document.getElementById('destinos-list-container');
        if (!container) return; // Guard

        if (list.length === 0) {
            container.innerHTML = '<p style="font-size: 0.9rem; color: var(--secondary-text); padding: 1rem;">No se encontraron destinos.</p>';
            return;
        }

        let html = '';
        list.forEach(d => {
            const isChecked = selectedIds.has(String(d.id_destino)) ? 'checked' : '';
            html += `
                <label class="destination-option-row">
                    <input type="checkbox" name="destinos" value="${d.id_destino}" ${isChecked} onchange="toggleDestinoSelection(this)">
                    <div class="destination-row-content">
                        <div class="destination-info">
                            <span class="destination-title">${d.nombre}</span>
                            <span class="destination-sub">${d.ciudad}, ${d.pais}</span>
                        </div>
                        <div class="custom-checkbox"></div>
                    </div>
                </label>
            `;
        });
        container.innerHTML = html;
    };

    // Filter & Sort Logic
    window.filterDestinos = () => {
        const searchVal = document.getElementById('dest-search').value.toLowerCase();
        const sortVal = document.getElementById('dest-sort').value;
        const regionVal = document.getElementById('dest-region').value;

        let filtered = allDestinos.filter(d => {
            const matchesSearch = d.nombre.toLowerCase().includes(searchVal) ||
                d.ciudad.toLowerCase().includes(searchVal) ||
                d.pais.toLowerCase().includes(searchVal);
            const matchesRegion = regionVal === 'all' || getContinent(d.pais) === regionVal;
            return matchesSearch && matchesRegion;
        });

        // Sorting
        if (sortVal === 'az') {
            filtered.sort((a, b) => a.nombre.localeCompare(b.nombre));
        } else if (sortVal === 'za') {
            filtered.sort((a, b) => b.nombre.localeCompare(a.nombre));
        } else if (sortVal === 'pais') {
            filtered.sort((a, b) => a.pais.localeCompare(b.pais));
        }

        renderList(filtered);
    };

    // Global helper for checkbox state persistence
    window.toggleDestinoSelection = (checkbox) => {
        if (checkbox.checked) selectedIds.add(checkbox.value);
        else selectedIds.delete(checkbox.value);
    };

    try {
        const res = await fetch('/api/destinos');
        allDestinos = await res.json();
    } catch (e) {
        console.error("Error loading destinations", e);
    }

    content.innerHTML = `
        <div class="create-form-container" style="max-width: 600px;">
            <h3 style="margin-bottom: 1.5rem;">Nuevo Paquete</h3>
            <form onsubmit="createPaquete(event)" class="create-form">
                <div style="display: flex; gap: 1rem; width: 100%; max-width: 500px;">
                    <div style="flex: 1;">
                        <label for="p-salida" style="display:block; text-align: left; margin-bottom: 0.5rem; font-size: 0.9rem;">Fecha Salida</label>
                        <input type="date" id="p-salida" required style="margin: 0;">
                    </div>
                    <div style="flex: 1;">
                        <label for="p-llegada" style="display:block; text-align: left; margin-bottom: 0.5rem; font-size: 0.9rem;">Fecha Llegada</label>
                        <input type="date" id="p-llegada" required style="margin: 0;">
                    </div>
                </div>
                
                <div style="display: flex; gap: 1rem; width: 100%; max-width: 500px;">
                    <input type="number" id="p-costo" placeholder="Costo Base" required style="flex: 1;">
                    <input type="number" id="p-cupos" placeholder="Cupos" required style="flex: 1;">
                </div>
                
                <div style="width: 100%; max-width: 480px; margin: 0.5rem auto;">
                    <label style="display: block; text-align: center; margin-bottom: 0.5rem; font-weight: 600; font-size: 0.9rem; color: var(--secondary-text);">Seleccionar Destinos</label>
                    
                    <div class="destination-controls">
                        <input type="text" id="dest-search" class="destination-search" placeholder="Buscar destino..." onkeyup="filterDestinos()">
                        
                        <select id="dest-region" class="destination-filter" onchange="filterDestinos()">
                            <option value="all">Todo el Mundo</option>
                            <option value="Sudamérica">Sudamérica</option>
                            <option value="Norteamérica">Norteamérica</option>
                            <option value="Europa">Europa</option>
                            <option value="Asia">Asia</option>
                            <option value="Otros">Otros</option>
                        </select>
                        
                         <select id="dest-sort" class="destination-filter" onchange="filterDestinos()">
                            <option value="az">A - Z</option>
                            <option value="za">Z - A</option>
                            <option value="pais">Por País</option>
                        </select>
                    </div>

                    <div id="destinos-list-container" class="destinations-list-container">
                        <!-- Populated by JS -->
                    </div>
                </div>

                <div style="margin-top: 1.5rem; width: 100%; max-width: 500px; display: flex; gap: 1rem;">
                    <button type="submit" class="btn-primary" style="flex: 1;">Guardar Paquete</button>
                    <button type="button" onclick="loadPaquetes()" class="btn-secondary" style="flex: 1;">Cancelar</button>
                </div>
            </form>
        </div>
    `;

    // Initial Render
    filterDestinos();
}

async function createPaquete(e) {
    e.preventDefault();

    // Get selected destinations
    const checkboxes = document.querySelectorAll('input[name="destinos"]:checked');
    const selectedDestinos = Array.from(checkboxes).map(cb => cb.value);

    if (selectedDestinos.length === 0) {
        alert('Debes seleccionar al menos un destino.');
        return;
    }

    const data = {
        fecha_salida: document.getElementById('p-salida').value,
        fecha_llegada: document.getElementById('p-llegada').value,
        costo_destino: document.getElementById('p-costo').value,
        cupos: document.getElementById('p-cupos').value,
        destinos: selectedDestinos
    };

    const res = await fetch('/api/paquetes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok) {
        loadPaquetes();
    } else {
        alert('Error creando paquete: ' + (result.message || 'Error desconocido'));
    }
}

async function deletePaquete(id) {
    if (!confirm('¿Eliminar paquete?')) return;
    const res = await fetch(`/api/paquetes/${id}`, { method: 'DELETE' });
    if (res.ok) loadPaquetes();
    else alert('Error eliminando paquete');
}

function hideWelcomeText() {
    const welcome = document.getElementById('welcome-text');
    if (welcome) {
        welcome.classList.add('hidden');
    }
}

function resetWelcomeText() {
    const welcome = document.getElementById('welcome-text');
    if (welcome) {
        welcome.classList.remove('hidden');
    }
}


// Profile Logic

function showHome() {
    if (state.user) {
        showDashboard();
    } else {
        showSection('home');
    }
}

async function showProfile() {
    showSection('profile-section');
    updateTitle('Mi Perfil');
    const msg = document.getElementById('profile-msg');
    msg.innerText = 'Cargando datos...';
    msg.style.color = '#fff';

    try {
        const res = await fetch('/api/me');
        const data = await res.json();

        if (data.success) {
            document.getElementById('prof-email').value = data.usuario.email;
            document.getElementById('prof-phone').value = data.usuario.telefono || '';
            msg.innerText = '';
        } else {
            msg.innerText = 'Error cargando perfil: ' + data.message;
            msg.style.color = 'var(--error)';
        }
    } catch (e) {
        msg.innerText = 'Error de conexión';
        msg.style.color = 'var(--error)';
    }
}

async function updateProfile(e) {
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
            msg.style.color = '#4ade80'; // Success green
            // Update session state locally if needed, though mostly visual
        } else {
            msg.innerText = 'Error: ' + data.message;
            msg.style.color = 'var(--error)';
        }
    } catch (e) {
        msg.innerText = 'Error al actualizar';
        msg.style.color = 'var(--error)';
    }
}

async function checkSession() {
    try {
        const res = await fetch('/api/me');
        const data = await res.json();

        // Check for deep link
        const urlParams = new URLSearchParams(window.location.search);
        const sectionParam = urlParams.get('section');

        let targetSection = 'home';
        if (sectionParam) {
            // Clean section to avoid XSS issues implicitly, verify it exists first
            if (document.getElementById(sectionParam)) {
                targetSection = sectionParam;
            }
        }

        if (data.success) {
            state.user = data.usuario;
            updateNav();
            // If logged in but user specifically asked for login, maybe redirect to dashboard
            if (targetSection === 'login') {
                showDashboard();
            } else {
                if (document.getElementById(targetSection)) {
                    showSection(targetSection);
                }
            }
        } else {
            // Not logged in
            if (document.getElementById(targetSection)) {
                showSection(targetSection);
            }
        }
    } catch (e) {
        if (document.getElementById('home')) {
            showSection('home');
        }
    }
}

// Image Gallery Logic (Global Scope)
function openPackageGallery(packageId, startIndex) {
    const paquete = state.currentPaquetes.find(p => p.id_paquete === packageId);
    if (!paquete || !paquete.destinos) return;

    state.galleryImages = paquete.destinos.map(d => {
        const slug = d.nombre.toLowerCase()
            .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
            .replace(/ /g, '-')
            .replace(/[^\w-]+/g, '')
            .replace(/-+/g, '-');
        return {
            src: `/static/img/${slug}.webp`,
            caption: `${d.nombre}, ${d.pais}`
        };
    });

    state.galleryIndex = startIndex;
    showGallery();
}

function showGallery() {
    const modal = document.getElementById('gallery-modal');
    const img = document.getElementById('gallery-image');
    const caption = document.getElementById('gallery-caption');
    const current = state.galleryImages[state.galleryIndex];

    img.src = current.src;
    caption.innerText = current.caption;
    modal.classList.add('active');

    // Add keyboard support
    document.addEventListener('keydown', handleGalleryKeys);
}

function closeGallery() {
    const modal = document.getElementById('gallery-modal');
    modal.classList.remove('active');
    document.removeEventListener('keydown', handleGalleryKeys);
}

function nextImage() {
    state.galleryIndex = (state.galleryIndex + 1) % state.galleryImages.length;
    showGallery(); // Refresh view
}

function prevImage() {
    state.galleryIndex = (state.galleryIndex - 1 + state.galleryImages.length) % state.galleryImages.length;
    showGallery();
}

function handleGalleryKeys(e) {
    if (e.key === 'Escape') closeGallery();
    if (e.key === 'ArrowRight') nextImage();
    if (e.key === 'ArrowLeft') prevImage();
}

// Home Carousel Logic
function showHome() {
    showSection('home');
    // Re-check carousel if needed, though initHomeCarousel runs on load
}

function initHomeCarousel() {
    // Only run on home page
    if (!document.getElementById('home-carousel')) return;
    loadHomeCarousel();
}

async function loadHomeCarousel() {
    const track = document.getElementById('home-carousel');
    if (!track) return;

    // Create inner track for scrolling
    track.innerHTML = '<div class="carousel-track" id="carousel-track"></div>';
    const innerTrack = document.getElementById('carousel-track');

    try {
        const res = await fetch('/api/destinos');
        const destinos = await res.json();

        if (destinos.length === 0) return;

        // Create cards
        const createCard = (d) => {
            const slug = d.nombre.toLowerCase()
                .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                .replace(/ /g, '-')
                .replace(/[^\w-]+/g, '')
                .replace(/-+/g, '-');
            return `
                <div class="carousel-item">
                    <img src="/static/img/${slug}.webp" alt="${d.nombre}" loading="lazy" onerror="this.src='/static/img/default.webp'">
                    <div class="carousel-caption">
                        <div>${d.nombre}</div>
                        <div style="font-size: 0.8rem; font-weight: normal;">${d.pais}</div>
                    </div>
                </div>
            `;
        };

        // Triple the content for smooth infinite loop
        const itemsHtml = destinos.map(d => createCard(d)).join('');
        innerTrack.innerHTML = itemsHtml + itemsHtml + itemsHtml;

    } catch (e) {
        console.error('Error loading carousel:', e);
        track.style.display = 'none';
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initHomeCarousel);
