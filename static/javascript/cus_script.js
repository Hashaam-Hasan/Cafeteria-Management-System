
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
document.addEventListener('DOMContentLoaded', function () {
    const categories = [
        { name: 'Pastries', text: 'Delicious pastries to satisfy your sweet tooth.', icon: '{% static "icons/pastry-icon.svg" %}', image: '{% static "images/customer_images/cover.jpg" %}' },
        { name: 'Desserts', text: 'Sweet and savory desserts to end your meal.', icon: '{% static "icons/dessert-icon.svg" %}', image: '{% static "images/customer_images/cat-dessert.jpeg" %}' },
        { name: 'Coffee and Tea', text: 'Savor the best in coffee and tea, any time of day', icon: '{% static "icons/coffee-icon.svg" %}', image: '{% static "images/customer_images/cat-tea.jpg" %}' },
        { name: 'Beverages', text: 'Refreshing drinks to quench your thirst.', icon: '{% static "icons/beverage-icon.svg" %}', image: '{% static "images/customer_images/cat-bev.jpeg" %}' },
        { name: 'Breakfast', text: 'Enjoy a hearty breakfast to fuel your day.', icon: '{% static "icons/breakfast-icon.svg" %}', image: '{% static "images/customer_images/cat-bf.jpg" %}' },
        { name: 'Lunch', text: 'Delicious lunch meals for your afternoon break.', icon: '{% static "icons/lunch-icon.svg" %}', image: '{% static "images/customer_images/cat-lunch.jpg" %}' },
        { name: 'Soups', text: 'Indulge in our variety of fresh, tasty soups.', icon: '{% static "icons/soup-icon.svg" %}', image: '{% static "images/customer_images/cat-soup.jpg" %}' }
    ];

    const carouselInner = document.getElementById('carousel-inner');

    categories.forEach((category, index) => {
        const div = document.createElement('div');
        div.className = `carousel-item ${index === 0 ? 'active' : ''}`;
        div.innerHTML = `
            <div class="card text-center mx-auto">
                <img src="${category.image}" class="card-img-top" alt="${category.name}">
                <div class="card-body">
                    <h5 class="card-title">${category.name}</h5>
                    <p class="card-text">${category.text}</p>
                    <div class="card-icon">
                        <button type="button" class="btn btn-outline-primary" style = "width:25%; color: black; border-color: black; border-radius: 15px;">Go!</button>
                        
                    </div>
                </div>
            </div>
        `;
        carouselInner.appendChild(div);
    });
});

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
