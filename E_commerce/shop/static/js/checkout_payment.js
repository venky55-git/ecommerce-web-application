document.addEventListener('DOMContentLoaded', function() {
        // Highlight selected payment method
        const paymentOptions = document.querySelectorAll('.payment-option');
        paymentOptions.forEach(option => {
            option.addEventListener('click', function() {
                paymentOptions.forEach(opt => opt.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    });