document.addEventListener('DOMContentLoaded', function() {
    fetch(getcartUrl)
        .then(response => response.json())
        .then(data => {
            const cartQuantityElement = document.getElementById('cart_quantity');
            if (data.cart_quantity > 0) {
                cartQuantityElement.textContent = data.cart_quantity;
                cartQuantityElement.style.display = 'block';
            } else {
                cartQuantityElement.style.display = 'none';
            }
        })
        .catch(error => console.error('Error fetching cart quantity:', error));
});