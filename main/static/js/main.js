/**
 * Main Entry Point
 * Agregates all modules and exposes necessary functions to window for HTML compatibility.
 */
import {
    showSection, showNotification, updateTitle, loadTheme, toggleTheme,
    updateNav, showCustomModal
} from './modules/ui.js';

import { login, logout, register, checkSession, updateProfile, togglePasswordVisibility } from './modules/auth.js';
import { loadDestinos, createDestino, loadPaquetes, deleteDestino, deletePaquete, showCreateDestinoForm, showCreatePaqueteForm } from './modules/admin.js';
import { loadAvailablePackages, loadMyReservations, reservarPaquete } from './modules/client.js';
import { createSlug, formatCurrencyCLP, formatDateToSpanishLong } from './modules/utils.js';

// Central State
const state = {
    user: null,
    currentPaquetes: [], // Used for gallery
    galleryImages: [],
    galleryIndex: 0
};

// --- Global Exposes for HTML Attributes (onclick) ---
// Since we are moving to modules, functions are no longer global by default.
// We must explicitly attach them to window.
window.showSection = (sectionId) => showSection(sectionId, state);
window.login = async (e) => {
    const success = await login(e, state);
    if (success) {
        showDashboard();
    }
};
window.logout = () => logout(state);
window.register = register;
window.updateProfile = updateProfile;
window.toggleTheme = toggleTheme;
window.togglePasswordVisibility = togglePasswordVisibility;

// Admin
window.loadDestinos = loadDestinos;
window.createDestino = createDestino;
window.showCreateDestinoForm = showCreateDestinoForm;
window.loadPaquetes = () => loadPaquetes(state);
window.createPaquete = null; // Handled within showCreatePaqueteForm logic mostly
window.showCreatePaqueteForm = showCreatePaqueteForm;
window.deleteDestino = deleteDestino;
window.deletePaquete = (id) => deletePaquete(id, state);

// Client
window.loadAvailablePackages = () => loadAvailablePackages(state);
window.loadMyReservations = () => loadMyReservations(state);
window.reservarPaquete = (id, cupos) => reservarPaquete(id, cupos, state);

// Public/Shared
window.showHome = () => showSection('home', state);
window.showPublicDestinos = loadPublicDestinos;
window.showProfile = () => {
    showSection('profile-section', state);
    if (state.user) {
        document.getElementById('prof-rut').value = state.user.rut || '';
        document.getElementById('prof-nombres').value = state.user.nombres || '';
        document.getElementById('prof-apellidos').value = `${state.user.apellido_paterno || ''} ${state.user.apellido_materno || ''}`.trim();
        document.getElementById('prof-email').value = state.user.email || '';
        document.getElementById('prof-phone').value = state.user.telefono || '';
    }
};
window.showDashboard = showDashboard;
window.showNotification = showNotification; // Used by flash messages in HTML
window.closeGallery = closeGallery;
window.prevImage = prevImage;
window.nextImage = nextImage;

// --- Initialization ---

document.addEventListener('DOMContentLoaded', async () => {
    loadTheme();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', window.login);
    }

    // Check Session
    const targetSection = await checkSession(state);

    if (targetSection === 'dashboard') {
        showDashboard();
    } else {
        showSection(targetSection, state);
        if (targetSection === 'home') {
            // Carousel loaded by showSection
        } else if (targetSection === 'public-destinos') {
            loadPublicDestinos();
        }
    }
});


// --- Helper Logic that bridges modules ---

function showDashboard() {
    if (!state.user) return showSection('login', state);

    if (state.user.rol === 'Administrador') {
        showSection('admin-dashboard', state);
        // Reset Admin View
        const welcome = document.getElementById('welcome-text');
        const panel = document.getElementById('panel-text');
        if (welcome) welcome.className = ''; // Remove hidden
        if (panel) panel.style.display = 'inline';
        document.getElementById('admin-content').innerHTML = '';
    } else {
        showSection('client-dashboard', state);
        // Reset Client View
        const header = document.getElementById('client-welcome-header');
        if (header) header.className = '';
        document.getElementById('client-content').innerHTML = '';
        document.getElementById('client-main-title').innerText = `Hola, ${state.user.nombres}`;
    }
}

// Replaced by new full-screen implementation
async function loadPublicDestinos() {
    showSection('public-destinos', state);
    const section = document.getElementById('public-destinos');

    // Override section padding for full screen effect
    section.style.padding = '0';
    section.style.height = '100vh'; // Ensure full height
    section.style.overflow = 'hidden';

    // Show loading state
    section.innerHTML = `
        <div style="height: 100vh; display: flex; align-items: center; justify-content: center;">
            <p style="font-size: 1.5rem; color: var(--text);">Cargando destinos...</p>
        </div>
    `;

    try {
        const res = await fetch('/api/destinos');
        const destinos = await res.json();

        // Clear loading
        section.innerHTML = '';

        // Create scroll container
        const container = document.createElement('div');
        container.className = 'destinations-scroll-container';
        section.appendChild(container);

        if (destinos.length === 0) {
            container.innerHTML = `
                <div class="destination-full-screen" style="align-items: center; justify-content: center;">
                    <p>No hay destinos disponibles.</p>
                </div>
            `;
            return;
        }

        destinos.forEach(d => {
            const destSection = document.createElement('div');
            destSection.className = 'destination-full-screen';

            const slug = createSlug(d.nombre);
            const imgUrl = `/static/img/${slug}.webp`;
            // Pricing placeholder (not in API response usually, defaulting if missing)
            const precio = d.precio ? formatCurrencyCLP(d.precio) : 'Consultar Precio';

            destSection.innerHTML = `
                <div class="destination-image-side">
                    <img src="${imgUrl}" alt="${d.nombre}" loading="lazy" onerror="this.src='/static/img/default.webp'">
                </div>
                <div class="destination-info-side">
                    <h2 class="dest-fs-title">${d.nombre}</h2>
                    <div class="dest-fs-location">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                        ${d.ciudad}, ${d.pais}
                    </div>
                    <p class="dest-fs-desc">${d.descripcion || 'Descubre las maravillas de este destino único, diseñado para ofrecerte experiencias inolvidables y momentos de relajación absoluta.'}</p>
                </div>

            `;
            container.appendChild(destSection);
        });

    } catch (e) {
        console.error("Error loading destinations:", e);
        section.innerHTML = `
            <div style="height: 100vh; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <p class="error-msg">Error cargando destinos.</p>
                <button class="btn-primary" onclick="loadPublicDestinos()">Reintentar</button>
            </div>
        `;
    }
}

// --- Gallery Logic (Kept here as it uses shared state primarily) ---

// Listen for custom open-gallery events from modules
document.addEventListener('open-gallery', (e) => {
    const { packageId, startIndex } = e.detail;
    openPackageGallery(packageId, startIndex);
});

function openPackageGallery(packageId, startIndex) {
    const pkg = state.currentPaquetes.find(p => p.id_paquete === packageId);
    if (!pkg || !pkg.destinos) return;

    state.galleryImages = pkg.destinos.map(d => ({
        src: `/static/img/${createSlug(d.nombre)}.webp`,
        caption: `${d.nombre} (${d.ciudad})`
    }));
    state.galleryIndex = startIndex;
    updateGallery();
    document.getElementById('gallery-modal').classList.add('active');
}

function updateGallery() {
    const img = document.getElementById('gallery-image');
    const cap = document.getElementById('gallery-caption');
    const data = state.galleryImages[state.galleryIndex];

    img.style.opacity = '0';
    setTimeout(() => {
        img.src = data.src;
        cap.innerText = `${data.caption} (${state.galleryIndex + 1}/${state.galleryImages.length})`;
        img.onload = () => { img.style.opacity = '1'; };
    }, 200);
}

function closeGallery() {
    document.getElementById('gallery-modal').classList.remove('active');
}

function nextImage() {
    state.galleryIndex = (state.galleryIndex + 1) % state.galleryImages.length;
    updateGallery();
}

function prevImage() {
    state.galleryIndex = (state.galleryIndex - 1 + state.galleryImages.length) % state.galleryImages.length;
    updateGallery();
}

// Re-expose gallery functions to window for onclick in HTML (modal buttons)
window.closeGallery = closeGallery;
window.nextImage = nextImage;
window.prevImage = prevImage;
