/**
 * Client Module
 */
import { showCustomModal, updateTitle, applyTransition } from './ui.js';
import { createSlug, formatCurrencyCLP, formatDateToSpanishLong } from './utils.js';

export async function loadAvailablePackages(state) {
    const header = document.getElementById('client-welcome-header');
    if (header) header.classList.add('hidden');

    updateTitle('Paquetes Disponibles');
    const content = document.getElementById('client-content');
    applyTransition('client-content');

    content.innerHTML = `
        <h3 class="client-section-title">Paquetes Disponibles</h3>
        <div id="client-packages-list" class="content-area"></div>
    `;

    try {
        const res = await fetch('/api/paquetes');
        const paquetes = await res.json();
        state.currentPaquetes = paquetes; // Sync state for gallery

        const list = document.getElementById('client-packages-list');
        list.innerHTML = '';

        paquetes.forEach(p => {
            // Collage
            let collageHtml = '';
            if (p.destinos && p.destinos.length > 0) {
                const maxDestinos = p.destinos.slice(0, 4);
                let imgs = '';
                maxDestinos.forEach((d, index) => {
                    const slug = createSlug(d.nombre);
                    imgs += `<img src="/static/img/${slug}.webp" alt="${d.nombre}" loading="lazy" 
                        onerror="this.src='/static/img/default.webp'"
                        data-pkg-id="${p.id_paquete}" data-idx="${index}" class="collage-img" style="cursor: pointer;">`;
                });
                collageHtml = `<div class="package-collage items-${maxDestinos.length}">${imgs}</div>`;
            } else {
                collageHtml = `<div class="package-collage items-1"><img src="/static/img/default.webp" alt="Default"></div>`;
            }

            const card = document.createElement('div');
            card.className = 'card';

            card.innerHTML = collageHtml;

            const cardContent = document.createElement('div');
            cardContent.className = 'card-content';

            const h4 = document.createElement('h4');
            h4.textContent = `Paquete #${p.id_paquete}`;

            const datesP = document.createElement('p');
            datesP.innerHTML = `<strong>Salida:</strong> ${formatDateToSpanishLong(p.fecha_salida)}`;

            const arriveP = document.createElement('p');
            arriveP.innerHTML = `<strong>Llegada:</strong> ${formatDateToSpanishLong(p.fecha_llegada)}`;

            const costP = document.createElement('p');
            costP.innerHTML = `<strong>Costo:</strong> ${formatCurrencyCLP(p.costo_destino)}`;

            const cuposP = document.createElement('p');
            cuposP.innerHTML = `<strong>Cupos:</strong> ${p.cupos}`;

            const destListDiv = document.createElement('div');
            destListDiv.className = 'destinos-list';
            destListDiv.innerHTML = '<strong>Destinos:</strong>';

            const ul = document.createElement('ul');
            if (p.destinos) {
                p.destinos.forEach(d => {
                    const li = document.createElement('li');
                    li.textContent = `${d.nombre} (${d.ciudad})`;
                    ul.appendChild(li);
                });
            }
            destListDiv.appendChild(ul);

            // Actions
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'card-actions';

            const reserveBtn = document.createElement('button');
            reserveBtn.className = 'btn-primary';
            reserveBtn.textContent = p.cupos > 0 ? 'Reservar' : 'Agotado';
            reserveBtn.disabled = p.cupos <= 0;
            reserveBtn.onclick = () => reservarPaquete(p.id_paquete, p.cupos, state);

            actionsDiv.appendChild(reserveBtn);

            cardContent.appendChild(h4);
            cardContent.appendChild(datesP);
            cardContent.appendChild(arriveP);
            cardContent.appendChild(costP);
            cardContent.appendChild(cuposP);
            cardContent.appendChild(destListDiv);
            cardContent.appendChild(actionsDiv);

            card.appendChild(cardContent);
            list.appendChild(card);
        });

        // Attach click handlers for collage images (Gallery)
        // Similar to admin, we invoke a custom event or shared logic
        document.querySelectorAll('.collage-img').forEach(img => {
            img.onclick = (e) => {
                const pkgId = parseInt(e.target.dataset.pkgId);
                const idx = parseInt(e.target.dataset.idx);
                const event = new CustomEvent('open-gallery', { detail: { packageId: pkgId, startIndex: idx } });
                document.dispatchEvent(event);
            };
        });

    } catch (e) {
        content.innerHTML += `<p class="error-msg">Error cargando paquetes: ${e.message}</p>`;
    }
}

export async function reservarPaquete(idPaquete, maxCupos, state) {
    try {
        const numCupos = await showCustomModal({
            title: 'Reservar Paquete',
            message: 'Ingrese la cantidad de cupos a reservar:',
            input: true,
            max: maxCupos
        });

        if (!numCupos) return;

        const res = await fetch('/api/reservas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_usuario: state.user.id_usuario,
                id_paquete: idPaquete,
                cupos: numCupos
            })
        });

        const data = await res.json();

        if (data.success) {
            await showCustomModal({
                title: '¡Reserva Exitosa!',
                message: `Has reservado ${numCupos} cupo(s). Revisa "Mis Reservas".`
            });
            loadAvailablePackages(state);
        } else {
            alert('Error: ' + data.message);
        }
    } catch (e) {
        console.error("Error reserva", e);
        alert('Error al procesar la reserva');
    }
}

export async function loadMyReservations(state) {
    const header = document.getElementById('client-welcome-header');
    if (header) header.classList.add('hidden');

    updateTitle('Mis Reservas');
    const content = document.getElementById('client-content');
    applyTransition('client-content');

    content.innerHTML = `
        <h3 class="client-section-title">Mis Reservas</h3>
        <div id="my-reservations-list" class="content-area"></div>
    `;

    try {
        const res = await fetch('/api/mis-reservas');
        const reservas = await res.json();

        const list = document.getElementById('my-reservations-list');
        list.innerHTML = '';

        if (reservas.length === 0) {
            list.innerHTML = '<p class="no-data-msg">No tienes reservas activas.</p>';
            return;
        }

        reservas.forEach(r => {
            const card = document.createElement('div');
            card.className = 'card';

            const cardContent = document.createElement('div');
            cardContent.className = 'card-content';

            const h4 = document.createElement('h4');
            h4.textContent = `Reserva #${r.id_reserva}`;

            const pkgP = document.createElement('p');
            pkgP.innerHTML = `<strong>Paquete ID:</strong> ${r.id_paquete_turistico}`;

            const cuposP = document.createElement('p');
            cuposP.innerHTML = `<strong>Cupos:</strong> ${r.cupos}`;

            const statusP = document.createElement('p');
            statusP.innerHTML = `<strong>Estado:</strong> ${r.estado}`;

            cardContent.appendChild(h4);
            cardContent.appendChild(pkgP);
            cardContent.appendChild(cuposP);
            cardContent.appendChild(statusP);

            card.appendChild(cardContent);
            list.appendChild(card);
        });

    } catch (e) {
        content.innerHTML += `<p class="error-msg">Error cargando reservas: ${e.message}</p>`;
    }
}
