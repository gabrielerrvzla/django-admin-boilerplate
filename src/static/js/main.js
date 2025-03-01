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
});

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