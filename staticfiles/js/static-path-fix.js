// Create static/js/static-path-fix.js
document.addEventListener('DOMContentLoaded', function() {
  // Fix dynamic loading of resources
  const originalGetScript = $.getScript;
  $.getScript = function(url, callback) {
      // Add /static/ prefix to paths if needed
      if (url.startsWith('/js/') || url.startsWith('/img/')) {
          url = '/static' + url;
      }
      return originalGetScript(url, callback);
  };
  
  // Fix image loading in WebGL
  if (window.THREE && THREE.ImageLoader) {
      const originalLoad = THREE.ImageLoader.prototype.load;
      THREE.ImageLoader.prototype.load = function(url, onLoad, onProgress, onError) {
          // Add /static/ prefix to paths if needed
          if (url.startsWith('/img/')) {
              url = '/static' + url;
          }
          return originalLoad.call(this, url, onLoad, onProgress, onError);
      };
  }
});