// Create a file called webgl-failsafe.js in your static/js directory

(function($) {
  // Initialize after window loads
  $(window).on('load', function() {
      console.log('WebGL Failsafe: Window loaded');
      
      // Function to initialize fallback gallery if WebGL fails
      function initFallbackGallery() {
          console.log('WebGL Failsafe: Checking if gallery needs fallback');
          
          // Check if the WebGL gallery is visible/initialized
          const glContainer = $('.anita-gl-container');
          if (glContainer.length && (!glContainer.is(':visible') || glContainer.height() < 10)) {
              console.log('WebGL Failsafe: WebGL gallery appears to be missing, initializing fallback');
              
              // Create a simple carousel as fallback
              const galleryWrap = $('.anita-gl-container-wrap');
              const fallbackGallery = $('<div class="anita-fallback-gallery owl-carousel"></div>');
              
              // Add all gallery items to the fallback
              $('.anita-gl-gallery-item').each(function() {
                  const $item = $(this);
                  const imgSrc = $item.attr('data-src') || $item.attr('data-full-url') || '/static/img/placeholder.jpg';
                  const title = $item.attr('data-title') || '';
                  const albumLink = $item.find('.anita-album-link').attr('href') || '#';
                  
                  // Create a simple image slide
                  const slide = $(`
                      <div class="fallback-slide">
                          <a href="${albumLink}">
                              <img src="${imgSrc}" alt="${title}">
                              <div class="slide-caption">
                                  <h3>${title}</h3>
                              </div>
                          </a>
                      </div>
                  `);
                  
                  fallbackGallery.append(slide);
              });
              
              // Replace the WebGL gallery with the fallback
              galleryWrap.empty().append(fallbackGallery);
              
              // Initialize Owl Carousel if available
              if ($.fn.owlCarousel) {
                  fallbackGallery.owlCarousel({
                      items: 1,
                      loop: true,
                      nav: true,
                      dots: true,
                      autoplay: true,
                      autoplayTimeout: 5000
                  });
              }
          }
      }
      
      // Give the WebGL gallery time to initialize, then check if we need fallback
      setTimeout(initFallbackGallery, 3000);
  });
})(jQuery);