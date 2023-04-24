function get_cart() {
    return JSON.parse(localStorage.getItem("cart"))
}

function set_cart(value) {
    localStorage.setItem("cart", JSON.stringify(value))
}

window.onload = () => {
    if (!localStorage.cart) {
        set_cart({})
    }

    const bp = document.querySelector(".item_cart").cloneNode(true)
    const storage = document.querySelector(".card_storage")
    document.querySelector(".item_cart").remove()

    let price = 0

    for (let [key, value] of Object.entries(get_cart())) {
        let new_row = bp.cloneNode(true)

        new_row.childNodes[1].innerHTML = key
        new_row.childNodes[3].innerHTML = value
        price += Number.parseInt(value)
        storage.append(new_row)

    }

    document.querySelector(".total_price").innerHTML = price + " ₽"
}