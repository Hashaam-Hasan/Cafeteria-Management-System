
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');
    const login_btn = document.getElementById('login-btn');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            navbar.id = "navbar-scrolled";
            login_btn.id = "login-btn-scrolled";
        } else {
            navbar.id = "navbar";
            login_btn.id = "login-btn"
        }
    });
});

// script.js


function decreaseQuantity(button) {
    var input = button.nextElementSibling;
    var currentValue = parseInt(input.value);
    if (currentValue > 1) {
      input.value = currentValue - 1;
    }
  }

function increaseQuantity(button) {
    var input = button.previousElementSibling;
    var currentValue = parseInt(input.value);
    input.value = currentValue + 1;
  }


// function increaseValue() {
//     var value = parseInt(document.getElementById('number').value, 10);
//     value = isNaN(value) ? 0 : value;
//     value++;
//     document.getElementById('number').value = value;
//   }
  
//   function decreaseValue() {
//     var value = parseInt(document.getElementById('number').value, 10);
//     value = isNaN(value) ? 0 : value;
//     value < 1 ? value = 1 : '';
//     value--;
//     document.getElementById('number').value = value;
//   }
