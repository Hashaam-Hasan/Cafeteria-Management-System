let Orderstatus = document.getElementsByClassName("Orderstatus");
console.log("order",Orderstatus)
for (let i=0; i<Orderstatus.length ; i++){
let ord_status = Orderstatus[i].innerHTML;
console.log("Order",ord_status);
if(ord_status == "process"){
    Orderstatus[i].style.backgroundColor = "#0b66b6"
}
else if (ord_status == "Delivered") {
    Orderstatus[i].style.backgroundColor = "rgb(76, 182, 76)"
} 
 else {
    Orderstatus[i].style.backgroundColor = "rgb(227, 80, 62)"
}

}