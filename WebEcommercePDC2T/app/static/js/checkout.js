function toggleForm(formId){
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

// submit all form
function makeOrder()
{
    var form = document.getElementById('contact_form');
    var form1 = document.getElementById('address_form');
    var form2 = document.getElementById('payment_form');

    form.submit();
    form1.submit();
    form2.submit();
}