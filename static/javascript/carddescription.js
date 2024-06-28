var increment = document.getElementById("increment")
var decrement = document.getElementById("decrement")
var cart_value = document.getElementById("cart_value")
cart_value.value = 1
// cart_value.value++
console.log("card",cart_value , )

// function incrementvalue(){
//     if (cart_value<100){
//         cart_value.value++
//     }

// }


function incrementvalue(){
    console.log("++")
        if (cart_value.value<10){
        cart_value.value++
    }
}

function decrementvalue(){
    if(cart_value.value>1){
        cart_value.value--
    }
}



//Star Functionality
function setRating(rating) {
    var stars = document.querySelectorAll('.star');
    stars.forEach(function(star, index) {
        if (index < rating) {
            star.classList.add('filled');
        } else {
            star.classList.remove('filled');
        }
    });
}

// Example: Set rating to 3
setRating(3);

