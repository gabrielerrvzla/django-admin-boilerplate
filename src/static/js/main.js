document.addEventListener("DOMContentLoaded", function () {
    // Show alerts
    let alertContainer = document.getElementById("alert-container");
    if (alertContainer) showAlerts(alertContainer);

    // Load sidebar
    const sidebarWrapper = document.querySelector('.sidebar-wrapper');
    if (sidebarWrapper && typeof OverlayScrollbarsGlobal?.OverlayScrollbars !== 'undefined') {
        OverlayScrollbarsGlobal.OverlayScrollbars(sidebarWrapper, {
            scrollbars: {
                theme: 'os-theme-light',
                autoHide: 'leave',
                clickScroll: true,
            },
        });
    }

    // Show tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(
        (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl),
    );
});


/**
 * Shows the alerts in the alert container and closes them after 5 seconds.
 * @param {HTMLElement} alertContainer - The alert container element.
 */
function showAlerts(alertContainer) {
    alertContainer.classList.remove("d-none");
    alertContainer.classList.add("slide-up");

    setTimeout(function () {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

/**
 * Retrieves the value of a specific cookie by name from the document's cookies.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @return {string} The value of the cookie with the specified name.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Creates a form, populates it with hidden inputs based on the 'inputs' object provided,
 * adds a CSRF token input, appends the form to the document body, and submits it.
 *
 * @param {string} url - The URL where the form data will be sent.
 * @param {Object} inputs - An object containing key-value pairs for input fields to be added to the form.
 */
function sendPostRequest(url, inputs = {}) {
    const form = document.createElement('form');
    form.action = url;
    form.method = 'POST';
    form.style.display = 'none';

    // Agregar inputs basados en el objeto 'inputs' proporcionado
    for (const [key, value] of Object.entries(inputs)) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value;
        form.appendChild(input);
    }

    // Agregar el token CSRF
    const inputCsrfToken = document.createElement('input');
    inputCsrfToken.type = 'hidden';
    inputCsrfToken.name = 'csrfmiddlewaretoken';
    inputCsrfToken.value = getCookie('csrftoken');
    form.appendChild(inputCsrfToken);

    // Agregar el formulario al cuerpo del documento y enviarlo
    document.body.appendChild(form);
    form.submit();
}
