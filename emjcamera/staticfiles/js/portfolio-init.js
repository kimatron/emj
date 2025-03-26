document.addEventListener('DOMContentLoaded', function() {
  // Initialize WebGL carousel if it exists
  if (jQuery('.anita-gl-carousel-gallery').length) {
      if (typeof Anita_GL_Carousel === 'function') {
          new Anita_GL_Carousel(jQuery('.anita-gl-carousel-gallery'), {
              container: jQuery('.anita-main'),
              nav: true
          });
      } else {
          console.warn('Anita_GL_Carousel not loaded');
      }
  }
});