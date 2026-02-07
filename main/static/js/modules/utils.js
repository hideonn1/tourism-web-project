/**
 * Utility functions for the application
 */

export function formatCurrencyCLP(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(amount);
}

export function formatDateToSpanishLong(dateStr) {
    if (!dateStr) return '';
    // Fix: Ensure we handle date string correctly to avoid timezone issues
    // Appending 'T00:00:00' ensures local time interpretation or splitting as before
    const [year, month, day] = dateStr.split('-').map(Number);
    const date = new Date(year, month - 1, day);

    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    const dayName = days[date.getDay()];
    const dayNum = String(day).padStart(2, '0');
    const monthName = months[date.getMonth()];

    // Note: year might be undefined if split fails, but assuming valid 'YYYY-MM-DD'
    return `${dayName} ${dayNum} de ${monthName} del ${year}`;
}

export function createSlug(text) {
    return text.toLowerCase()
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // Remove accents
        .replace(/ /g, '-')
        .replace(/[^\w-]+/g, '')
        .replace(/-+/g, '-');
}
