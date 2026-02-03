/* REVEAL ELEMENTS ON LOAD(ABOUT_US) */
function revealElements() {
    const reveals = document.querySelectorAll(".reveal");

    reveals.forEach((el) => {
        el.classList.add("active");
    });
}

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(revealElements, 100);
});




/* AUTO-HIDE FOR DJANGO MESSAGES (ALERTS) */
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });
});


/* SELECT2 INITIALIZATION(DROPDOWN MENUS TO SEARCH BOXES WITH CLEAR FIELD OPTION) */
$(document).ready(function() {
    $('.searchable-select').select2({
        width: '100%',
        placeholder: "Select an option",
        allowClear: true
    });
});


/* AUTOSCROLL TO MOVIES */
$(document).ready(function () {
    if (window.location.search.length > 0) {
        $('html, body').animate({
            scrollTop: $("#movies-list").offset().top
        }, 600);
    }
});




