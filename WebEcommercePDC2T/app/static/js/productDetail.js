function addToCart(productId, quantity) {
  var quantity = $('[name="quantity"]').val() || 1;
  var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
  var cart_url = cartUrl;

  $.ajax({
      type: 'POST',
      url: cart_url,
      data: {
          'product_id': productId,
          'quantity': quantity,
          'csrfmiddlewaretoken': csrf_token
      },
      dataType: 'json',
      success: function(data) {
          if (data.redirect) {
              window.location.href = data.redirect;
          } else {
              console.log(data.message);
              updateCartQuantityDisplay(data.unique_item_count);
          }
      },
      error: function(xhr, status, error) {
          console.error(xhr.responseText);
      }
  });
}


function updateCartQuantityDisplay(uniqueItemCount) {
    var cartQuantityElement = document.getElementById('cart_quantity');
    if (uniqueItemCount > 0) {
        cartQuantityElement.textContent = uniqueItemCount;
        cartQuantityElement.style.display = 'block';
    } else {
        cartQuantityElement.style.display = 'none';
    }
}