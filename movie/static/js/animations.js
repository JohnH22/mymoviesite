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


/* CLEAR ALL FILTERS BUTTON TOGGLE */
$(document).ready(function () {
    const checkFilters = () => {
        const txt = $('input[name="txt"]').val().trim();
        const cat = $('select[name="cat"]').val();
        const dir = $('select[name="dir"]').val();

        const $container = $('#clear-filters-container');

        if (txt.length > 0 || (cat && cat !== "") || (dir && dir !== "")) {
            $container.stop(true, true).fadeIn(200);
        } else {
            $container.stop(true, true).fadeOut(200);
        }
    };

    $(document).on('input', 'input[name="txt"]', checkFilters);

    $(document).on('change', 'select[name="cat"], select[name="dir"]', checkFilters);

    $(document).on('click', '#btn-clear-logic', function (e) {
        e.preventDefault()
        $('input[name="txt"]').val('');
        $('select[name="cat"], select[name="dir"]').val(null).trigger('change');
        checkFilters();
    });

    setTimeout(checkFilters, 300);
});







