const logregBox = document.querySelector('.logreg-box');


const signInBtn = document.getElementById('signInBtn');
const userTypeSelect = document.getElementById('userType');



const loginLink = document.querySelector('.login-link');

const registerLink = document.querySelector('.register-link');



// Code smajhne k liye email outlawgod101@gmail.com

signInBtn.addEventListener('click', () => {
    const userType = userTypeSelect.value;

    logregBox.classList.remove('active-admin', 'active-customer', 'active-manager', 'active-sign-in');
    
    switch(userType) {
        case 'admin':
            logregBox.classList.add('active-admin');
            break;
        case 'customer':
            logregBox.classList.add('active-customer');
            break;
        case 'manager':
            logregBox.classList.add('active-manager');
            break;
    }

    logregBox.classList.add('active-sign-in');
});



const formBox = document.querySelector('.logreg-box');

userTypeSelect.addEventListener('change', function() {
    const selectedType = this.value;
    formBox.classList.remove('active-admin', 'active-customer', 'active-manager', 'active-sign-in');
    formBox.classList.add(`active-${selectedType}`);
});














registerLink.addEventListener('click', () => {
    logregBox.classList.add('active');
});

loginLink.addEventListener('click', () => {
    logregBox.classList.remove('active');
});












