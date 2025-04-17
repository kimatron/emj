// Updated debug.js to safely initialize the carousel
document.addEventListener('DOMContentLoaded', function() {
    console.log('Loaded scripts:', document.scripts);
    
    // Check if Anita_GL_Carousel is defined
    if (typeof Anita_GL_Carousel === 'function') {
        console.log('Anita_GL_Carousel defined:', typeof Anita_GL_Carousel);
        
        // Find carousel element
        const carouselElement = document.querySelector('.anita-gl-carousel-gallery');
        if (carouselElement) {
            console.log('Found carousel element, attempting to initialize');
            
            // Safely initialize the carousel
            try {
                // Make sure all required elements exist
                if (!jQuery) {
                    console.error('jQuery is not defined');
                    return;
                }
                
                // Initialize with a safety check for data attributes
                setTimeout(function() {
                    // Ensure all galleries have the required data attributes
                    $('.anita-gl-gallery-item').each(function() {
                        const $item = $(this);
                        if (!$item.attr('data-src')) {
                            console.warn('Gallery item missing data-src attribute:', $item);
                            // Set a placeholder if missing
                            $item.attr('data-src', '/static/img/placeholder.jpg');
                        }
                        if (!$item.attr('data-size')) {
                            $item.attr('data-size', '1440x1080');
                        }
                    });
                    
                    // Now try to initialize
                    if (window.anitaInit && typeof window.anitaInit.glCarousel === 'function') {
                        window.anitaInit.glCarousel();
                    }
                }, 500);
            } catch (e) {
                console.error('Failed to initialize carousel:', e);
            }
        } else {
            console.log('No carousel element found');
        }
    } else {
        console.log('Anita_GL_Carousel not defined');
    }
});