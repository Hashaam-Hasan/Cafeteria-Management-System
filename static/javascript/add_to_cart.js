document.addEventListener('DOMContentLoaded', function() {
    let buttons = document.querySelectorAll('.add-to-cart');
    buttons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            let menuName = button.getAttribute('data-menu-name');
            var cart_value = document.getElementById("cart_value").value
            console.log('Menu Name:', menuName);
            fetch(`/add-to-cart?menu-name=${menuName}&cart-quantity=${cart_value}`, {
            })
            .then(response => response.json())
            .then(data => {
                // console.log('Success:', data);
                console.log('Success:', data.check);
                    if (!data.check) {
                        console.log("ERROR")
                        Swal.fire({
                        title: 'Success!',
                        text: data.success,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    });
                    }
                    else if (data.check) {
                        Swal.fire({
                        title: 'Warning!',
                        text: data.error,
                        icon: 'warning',
                        confirmButtonText: 'OK'
                    });
                    }
                    
                
                // Handle success response
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error!',
                    text: 'Something went wrong!',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
        });
    });
});