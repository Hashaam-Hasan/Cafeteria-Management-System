
document.querySelectorAll(".animate-number").forEach(el => {
    let val = parseInt(el.textContent, 10);

    let odometer = new Odometer({
        el: el,
        value: 1, // initial value
        format: '', // format can be customized
        theme: 'default'
    });

    odometer.update(val); // update to the new value
});


// Toggle offcanvas sidebar
document.querySelector('.toggle-sidebar').addEventListener('click', function() {
    document.querySelector('.toggle-sidebar').classList.toggle('active');
    document.querySelector('.offcanvas-sidebar').classList.toggle('active');
});