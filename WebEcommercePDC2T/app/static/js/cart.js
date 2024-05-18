
function updateCartQuantityDisplay(uniqueItemCount) {
    var cartQuantityElement = document.getElementById('cart_quantity');
    if (uniqueItemCount > 0) {
        cartQuantityElement.textContent = uniqueItemCount;
        cartQuantityElement.style.display = 'block';
    } else {
        cartQuantityElement.style.display = 'none';
    }
}

function updateQuantity(cartItemId, operation) {
    var quantityElement = document.getElementById('quantity_' + cartItemId);
    var quantityContent = quantityElement.textContent.trim();
    var newQuantity = parseInt(quantityContent, 10);

    if (operation === 'minus') {
        if (newQuantity > 1) {
            newQuantity--;
        }
    } else {
        newQuantity++;
    }
    var csrfToken = $('#csrf-form').find('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: cartUrl,
        type: 'PUT',
        headers: {'X-CSRFToken': csrfToken},
        data: {
            'cart_item_id': cartItemId,
            'new_quantity': newQuantity,
        },
        dataType: 'json',
        success: function(data) {
            if (data.success) {
                quantityElement.textContent = newQuantity;
                updateSubtotalAndTotal();
                updateCartQuantityDisplay(data.unique_item_count);
            } else {
                console.log('Failed to update cart item.');
            }
        },
        error: function() {
            console.log('Failed to update cart item.');
        }
    });
}

function removeItem(cartItemId) {
    var csrfToken = $('#csrf-form').find('input[name="csrfmiddlewaretoken"]').val();
    var cartItem = document.getElementById(cartItemId);
    $.ajax({
        url: cartUrl,
        type: 'DELETE',
        headers: {'X-CSRFToken': csrfToken},
        data: {
            'cart_item_id': cartItemId,
        },
        dataType: 'json',
        success: function(data) {
            if (data.success) {
                cartItem.remove();
                updateSubtotalAndTotal();
                updateCartQuantityDisplay(data.unique_item_count);
                console.log('Successfully deleted cart item.');
            } else {
                console.log('Failed to delete cart item.');
            }
        },
        error: function() {
            console.log('Failed to delete cart item.');
        }
    });
}

function removeCart() {
    var csrfToken = $('#csrf-form').find('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: cartUrl,
        type: 'DELETE',
        headers: {'X-CSRFToken': csrfToken},
        data: {
            'clear_cart': true
        },
        dataType: 'json',
        success: function(data) {
            if (data.success) {
                $('.cart_item').remove();
                updateSubtotalAndTotal();
                updateCartQuantityDisplay(0);
                console.log('Successfully cleared the cart.');
            } else {
                console.log('Failed to clear the cart.');
            }
        },
        error: function() {
            console.log('Failed to clear the cart.');
        }
    });
}

function updateSubtotalAndTotal() {
    var subtotal = 0;
    var quantityElements = document.querySelectorAll('.quantity');
    var priceElements = document.querySelectorAll('.price');
    for (var i = 0; i < quantityElements.length; i++) {
        var quantity = parseInt(quantityElements[i].textContent);
        var price = parseFloat(priceElements[i].textContent);
        subtotal += quantity * price;
    }

    let formattedSubtotal = subtotal.toFixed(0) + " VNĐ";
    document.getElementById('subtotal').textContent = formattedSubtotal;
    document.getElementById('total').textContent = formattedSubtotal;
}

$(document).ready(function() {
    updateSubtotalAndTotal();
    updateCartQuantity();
});

window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        updateSubtotalAndTotal();
        updateCartQuantity();
    }
});
