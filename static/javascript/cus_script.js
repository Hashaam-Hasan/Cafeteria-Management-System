
document.addEventListener('DOMContentLoaded', function(e) {
    e.preventDefault();
    const navbar = document.getElementById('navbar');
    const login_btn = document.querySelectorAll('#login-btn');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            navbar.id = "navbar-scrolled";
            login_btn.forEach((log)=>{
              log.id = "login-btn-scrolled";
            })
            
        } else {
            navbar.id = "navbar";
            login_btn.id = "login-btn"
            login_btn.forEach((log)=>{
              log.id = "login-btn";
            })
        }
    });
});

// script.js


function decreaseQuantity(button) {
  var input = button.nextElementSibling;
  var currentValue = parseInt(input.value);
  if (currentValue > 0) {
      input.value = currentValue - 1;
  }
}

function increaseQuantity(button) {
    var input = button.previousElementSibling;
    var currentValue = parseInt(input.value);
    input.value = currentValue + 1;
  }




let input_vals = document.querySelectorAll('#get_inp_val')
console.log(document.querySelector('.sub-check'))
document.querySelector('.sub-check').addEventListener('click', (e)=>{
  e.preventDefault();
  input_vals.forEach((inp_val)=>{
    let menuName = inp_val.getAttribute('data-menu-name');
    console.log(inp_val.value, menuName)
  })
})



