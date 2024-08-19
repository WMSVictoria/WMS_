document.addEventListener('DOMContentLoaded', function() {
    const orderSelect = document.getElementById('id_order');
    const customerField = document.getElementById('id_customer');
    const addressField = document.getElementById('id_shipping_address');

    orderSelect.addEventListener('change', function() {
        const orderId = this.value;

        if (orderId) {
            fetch(`/get_customer_address/${orderId}/`)
                .then(response => response.json())
                .then(data => {
                    customerField.value = data.customer_name;
                    addressField.value = data.shipping_address;
                });
        } else {
            customerField.value = '';
            addressField.value = '';
        }
    });
});
