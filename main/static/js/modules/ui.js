import { createSlug } from './utils.js';

/**
 * UI and Layout Management Module
 */

export const sectionTitles = {
    'home': 'Explora360 Chile | Viajes y Turismo',
    'login': 'Iniciar Sesión - Explora360',
    'register': 'Registro - Explora360',
    'admin-dashboard': 'Panel de Administración - Explora360',
    'client-dashboard': 'Panel de Cliente - Explora360',
    'profile-section': 'Mi Perfil - Explora360',
    'public-destinos': 'Nuestros Destinos - Explora360'
};

export function updateTitle(sectionId) {
    document.title = sectionTitles[sectionId] || 'Explora360 Chile';
}

export function showSection(sectionId, state) {
    const target = document.getElementById(sectionId);
    if (!target) return;

    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
    });
    target.classList.add('active');

    // Update Nav
    updateNav(state);

    // Section specific logic
    if (sectionId === 'login') {
        const navLogin = document.getElementById('nav-login');
        if (navLogin) navLogin.style.display = 'none';
    }

    if (sectionId === 'home') {
        const navHome = document.getElementById('nav-home');
        if (navHome) navHome.style.display = 'none';
        initHomeCarousel();
    }

    if (sectionId === 'public-destinos') {
        const navDestinos = document.getElementById('nav-destinos');
        if (navDestinos) navDestinos.style.display = 'none';
    }

    updateTitle(sectionId);
}

export function updateNav(state) {
    const navHome = document.getElementById('nav-home');
    if (!navHome) return;

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

export function showNotification(message) {
    const toast = document.getElementById('notification-toast');
    if (!toast) return;
    toast.innerText = message;
    toast.className = 'notification-toast show';
    setTimeout(() => {
        toast.className = toast.className.replace('show', '');
    }, 3000);
}

export function applyTransition(elementId) {
    const content = document.getElementById(elementId);
    if (!content) return;
    content.classList.remove('admin-transition');
    void content.offsetWidth; // Trigger reflow
    content.classList.add('admin-transition');
}

export function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    updateThemeIcon(isLight);
}

export function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        updateThemeIcon(true);
    }
}

function updateThemeIcon(isLight) {
    const icon = document.getElementById('theme-icon');
    const logo = document.getElementById('nav-logo');

    if (!icon) return;

    if (isLight) {
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
    } else {
        icon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    }

    if (logo) {
        logo.classList.add('fade-out');
        setTimeout(() => {
            logo.src = isLight ? '/static/img/favicon-light.svg' : '/static/img/favicon-dark.svg';
            logo.classList.remove('fade-out');
        }, 300);
    }
}

// Custom Modal
export function showCustomModal({ title, message, input = false, max = 1 }) {
    return new Promise((resolve) => {
        const modal = document.getElementById('custom-modal');
        const titleEl = document.getElementById('modal-title');
        const msgEl = document.getElementById('modal-msg');
        const inputEl = document.getElementById('modal-input');
        const btnConfirm = document.getElementById('modal-btn-confirm');
        const btnCancel = document.getElementById('modal-btn-cancel');

        titleEl.innerText = title;
        msgEl.innerText = message;
        inputEl.value = '';

        if (input) {
            inputEl.style.display = 'block';
            inputEl.max = max;
            inputEl.placeholder = `Máximo ${max}`;
            inputEl.value = 1;
            setTimeout(() => inputEl.focus(), 100);
        } else {
            inputEl.style.display = 'none';
        }

        modal.classList.add('active');

        // Handlers - defined here to close over resolve
        const close = (value) => {
            modal.classList.remove('active');
            // Clear handlers to avoid memory leaks/double fires if not fully cleaned (generic safety)
            btnConfirm.onclick = null;
            btnCancel.onclick = null;
            inputEl.onkeyup = null;
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

        inputEl.onkeyup = (e) => {
            if (e.key === 'Enter') btnConfirm.click();
        };
    });
}
// Carousel Logic - moved here as it's UI
export function initHomeCarousel() {
    // Only run on home page
    if (!document.getElementById('home-carousel')) return;
    loadHomeCarousel();
}

async function loadHomeCarousel() {
    const track = document.getElementById('home-carousel');
    if (!track) return;

    // Prevent double loading if already exists
    if (document.getElementById('carousel-track')) return;

    track.innerHTML = '<div class="carousel-track" id="carousel-track"></div>';
    const innerTrack = document.getElementById('carousel-track');

    try {
        const res = await fetch('/api/destinos');
        const destinos = await res.json();

        if (destinos.length === 0) return;

        const createCard = (d) => {
            const slug = createSlug(d.nombre);
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

        const itemsHtml = destinos.map(d => createCard(d)).join('');
        innerTrack.innerHTML = itemsHtml + itemsHtml + itemsHtml;

    } catch (e) {
        console.error('Error loading carousel:', e);
        track.style.display = 'none';
    }
}
