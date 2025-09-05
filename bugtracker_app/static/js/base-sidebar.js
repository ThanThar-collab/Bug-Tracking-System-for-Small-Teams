// base-sidebar.js

document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebar-toggle");
    const toggleIcon = document.getElementById("toggle-icon");

    // Load sidebar state from localStorage
    const isCollapsed = localStorage.getItem("sidebarCollapsed") === "true";

    if (isCollapsed) {
        sidebar.classList.add("sidebar-collapsed");
        toggleIcon.classList.remove("bi-arrow-left-short");
        toggleIcon.classList.add("bi-arrow-right-short");
    }

    // Toggle sidebar on button click
    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("sidebar-collapsed");

        const collapsed = sidebar.classList.contains("sidebar-collapsed");
        localStorage.setItem("sidebarCollapsed", collapsed);

        // Toggle icon direction
        if (collapsed) {
            toggleIcon.classList.remove("bi-arrow-left-short");
            toggleIcon.classList.add("bi-arrow-right-short");
        } else {
            toggleIcon.classList.remove("bi-arrow-right-short");
            toggleIcon.classList.add("bi-arrow-left-short");
        }
    });
});
