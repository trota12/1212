// static/js/carrito.js
document.addEventListener("DOMContentLoaded", function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.href;  // Asegúrate de que el href contiene la URL correcta para añadir al carrito

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',  // Importante para Django detectar que es AJAX
                },
            })
            .then(response => response.json())
            .then(data => {
                const cartCounter = document.querySelector('#cart-counter');
                cartCounter.textContent = data.cart_count;
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
s