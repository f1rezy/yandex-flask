function get_cart() {
    return JSON.parse(localStorage.getItem("cart"))
}

function set_cart(value) {
    localStorage.setItem("cart", JSON.stringify(value))
}

if (!localStorage.cart) {
    set_cart({})
}

const btn = document.querySelector(".cart-button")
btn.onclick = () => {
    let item = {}
    item[document.querySelector(".product-name").innerHTML] = document.querySelector(".product-price").innerHTML
    set_cart(Object.assign(get_cart(), item))
}