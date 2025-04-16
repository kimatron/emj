document.addEventListener('DOMContentLoaded', function() {
  console.log('Loaded scripts:', document.scripts);
  
  // Check if Anita_GL_Carousel is defined
  console.log('Anita_GL_Carousel defined:', typeof Anita_GL_Carousel);
  
  // Try to initialize WebGL carousel
  if (jQuery('.anita-gl-carousel-gallery').length) {
      console.log('Found carousel element, attempting to initialize');
      try {
          new Anita_GL_Carousel(jQuery('.anita-gl-carousel-gallery'), {
              container: jQuery('.anita-main'),
              nav: true
          });
          console.log('Carousel initialized successfully');
      } catch(e) {
          console.error('Failed to initialize carousel:', e);
      }
  } else {
      console.log('No carousel element found');
  }
});