document.addEventListener("DOMContentLoaded", () => {
    const cart = document.getElementById("cart-icon");
    const message = document.getElementById("cart-message");
  
    setTimeout(() => {
      cart.classList.add("move-cart");
      setTimeout(() => {
        message.style.opacity = 1;
      }, 2000);
    }, 500);
  });