// static/js/checkout.js
function toggleForm(formId) {
    console.log("Toggle function called with form ID:", formId);
    var form = document.getElementById(formId);
    var toggleBtn = document.getElementById("toggle_" + formId);
    if (form.style.display === "none") {
        form.style.display = "block";
        toggleBtn.textContent = "▲";
    } else {
        form.style.display = "none";
        toggleBtn.textContent = "▼";
    }
}

// submit only the main form
function makeOrder() {
    var form = document.getElementById('checkout_form');
    form.submit();
}