document.addEventListener("DOMContentLoaded", function () {
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");
    const sidebarBackdrop = document.getElementById("sidebarBackdrop");
    const alerts = Array.from(document.querySelectorAll(".alert[data-alert-text]"));

    const setSidebarState = (isOpen) => {
        if (!sidebar || !sidebarToggle) {
            return;
        }

        sidebar.classList.toggle("active", isOpen);
        document.body.classList.toggle("sidebar-open", isOpen);
        sidebarToggle.setAttribute("aria-expanded", String(isOpen));
        sidebarToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");

        if (sidebarBackdrop) {
            sidebarBackdrop.hidden = !isOpen;
        }
    };

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            setSidebarState(!sidebar.classList.contains("active"));
        });
    }

    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener("click", function () {
            setSidebarState(false);
        });
    }

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            setSidebarState(false);
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth >= 768) {
            setSidebarState(false);
        }
    });

    const seenAlerts = new Set();
    alerts.forEach((alertElement) => {
        const normalizedText = alertElement.dataset.alertText.trim().replace(/\s+/g, " ");
        if (seenAlerts.has(normalizedText)) {
            alertElement.remove();
            return;
        }

        seenAlerts.add(normalizedText);

        if (alertElement.dataset.autohide === "true") {
            window.setTimeout(function () {
                const alertInstance = bootstrap.Alert.getOrCreateInstance(alertElement);
                alertInstance.close();
            }, 5000);
        }
    });
});

