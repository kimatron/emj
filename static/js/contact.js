document.addEventListener('DOMContentLoaded', function() {
  // Handle form label animation on focus/input
  const inputWraps = document.querySelectorAll('.anita-input-wrap');
  
  inputWraps.forEach(wrap => {
      const input = wrap.querySelector('input, textarea');
      
      // Set initial state
      if (input.value) {
          wrap.classList.add('is-valued');
      }
      
      // Handle focus
      input.addEventListener('focus', () => {
          wrap.classList.add('is-focus');
          wrap.classList.add('is-valued');
      });
      
      // Handle blur
      input.addEventListener('blur', () => {
          wrap.classList.remove('is-focus');
          if (!input.value) {
              wrap.classList.remove('is-valued');
          }
      });
  });
  
  // Add a hover effect to contact detail items
  const contactItems = document.querySelectorAll('.anita-contact-details__list li');
  contactItems.forEach(item => {
      item.addEventListener('mouseenter', function() {
          this.classList.add('is-hover');
      });
      
      item.addEventListener('mouseleave', function() {
          this.classList.remove('is-hover');
      });
  });
  
  // Form submission handling with validation
  const contactForm = document.querySelector('.anita-contact-form');
  if (contactForm) {
      contactForm.addEventListener('submit', function(event) {
          // Only perform frontend validation if not already handled by Django
          if (!validateForm()) {
              event.preventDefault();
          }
      });
  }
  
  // Basic form validation
  function validateForm() {
      let isValid = true;
      const requiredFields = contactForm.querySelectorAll('input[required], textarea[required]');
      
      // Reset previous error states
      document.querySelectorAll('.anita-input-wrap.is-error').forEach(wrap => {
          wrap.classList.remove('is-error');
      });
      
      // Check required fields
      requiredFields.forEach(field => {
          if (!field.value.trim()) {
              const wrap = field.closest('.anita-input-wrap');
              wrap.classList.add('is-error');
              isValid = false;
          }
      });
      
      // Validate email format if email is present
      const emailField = contactForm.querySelector('input[type="email"]');
      if (emailField && emailField.value.trim()) {
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailPattern.test(emailField.value.trim())) {
              const wrap = emailField.closest('.anita-input-wrap');
              wrap.classList.add('is-error');
              isValid = false;
          }
      }
      
      return isValid;
  }
  
  // Show success message with fade effect if present
  const successAlert = document.querySelector('.anita-alert-success');
  if (successAlert) {
      // Initially set opacity to 0
      successAlert.style.opacity = '0';
      successAlert.style.transition = 'opacity 0.5s ease-in-out';
      
      // Fade in
      setTimeout(() => {
          successAlert.style.opacity = '1';
      }, 100);
      
      // Fade out after some time
      setTimeout(() => {
          successAlert.style.opacity = '0';
          
          // Remove from DOM after fade out
          setTimeout(() => {
              successAlert.remove();
          }, 500);
      }, 5000);
  }
});