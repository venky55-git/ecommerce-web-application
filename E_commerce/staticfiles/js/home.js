 // Auto-scrolling Carousel
 document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('imageCarousel');
    const carouselNav = document.getElementById('carouselNav');
    const items = carousel.querySelectorAll('.carousel-item');
    let currentIndex = 0;
    
    // Create navigation dots
    items.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('carousel-dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => {
            goToSlide(index);
        });
        carouselNav.appendChild(dot);
    });
    
    // Auto-scroll functionality
    function autoScroll() {
        currentIndex = (currentIndex + 1) % items.length;
        goToSlide(currentIndex);
    }
    
    function goToSlide(index) {
        currentIndex = index;
        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // Update active dot
        document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
    }
    
    // Start auto-scrolling (every 3 seconds)
    let scrollInterval = setInterval(autoScroll, 3000);
    
    // Pause on hover
    carousel.addEventListener('mouseenter', () => {
        clearInterval(scrollInterval);
    });
    
    carousel.addEventListener('mouseleave', () => {
        scrollInterval = setInterval(autoScroll, 3000);
    });
});


 