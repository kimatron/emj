document.addEventListener('DOMContentLoaded', function() {
  // Add hover effects to service cards
  const serviceCards = document.querySelectorAll('.anita-service-card');
  serviceCards.forEach(card => {
      card.addEventListener('mouseenter', function() {
          // Add active class to the current card
          this.classList.add('is-active');
          
          // Dim other cards
          serviceCards.forEach(otherCard => {
              if (otherCard !== this) {
                  otherCard.classList.add('is-dimmed');
              }
          });
      });
      
      card.addEventListener('mouseleave', function() {
          // Remove active class from the current card
          this.classList.remove('is-active');
          
          // Restore other cards
          serviceCards.forEach(otherCard => {
              otherCard.classList.remove('is-dimmed');
          });
      });
  });
  
  // Add hover effects to equipment cards
  const equipmentCards = document.querySelectorAll('.anita-equipment-card');
  equipmentCards.forEach(card => {
      card.addEventListener('mouseenter', function() {
          // Add active class to the current card
          this.classList.add('is-active');
          
          // Dim other cards
          equipmentCards.forEach(otherCard => {
              if (otherCard !== this) {
                  otherCard.classList.add('is-dimmed');
              }
          });
      });
      
      card.addEventListener('mouseleave', function() {
          // Remove active class from the current card
          this.classList.remove('is-active');
          
          // Restore other cards
          equipmentCards.forEach(otherCard => {
              otherCard.classList.remove('is-dimmed');
          });
      });
  });
  
  // Add typing effect to the quote text
  const quoteText = document.querySelector('.anita-quote-text');
  if (quoteText) {
      // Store original text
      const originalText = quoteText.textContent.trim();
      
      // Create typing effect on scroll
      const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  // Start typing effect
                  typeWriter(originalText, quoteText);
                  // Unobserve after triggering once
                  observer.unobserve(quoteText);
              }
          });
      }, { threshold: 0.5 });
      
      // Observe the quote text element
      observer.observe(quoteText);
      
      // Clear the text initially
      quoteText.textContent = '';
  }
  
  // Typing effect function
  function typeWriter(text, element, i = 0, speed = 30) {
      if (i < text.length) {
          element.textContent += text.charAt(i);
          i++;
          setTimeout(() => typeWriter(text, element, i, speed), speed);
      }
  }
  
  // Counter animation for stats
  const counters = document.querySelectorAll('.anita-counter-number');
  
  counters.forEach(counter => {
      const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  const target = parseInt(counter.textContent.trim());
                  animateCounter(counter, 0, target, 2000);
                  observer.unobserve(counter);
              }
          });
      }, { threshold: 0.5 });
      
      observer.observe(counter);
  });
  
  function animateCounter(element, start, end, duration) {
      let startTimestamp = null;
      const step = (timestamp) => {
          if (!startTimestamp) startTimestamp = timestamp;
          const progress = Math.min((timestamp - startTimestamp) / duration, 1);
          const currentCount = Math.floor(progress * (end - start) + start);
          element.textContent = currentCount;
          
          if (progress < 1) {
              window.requestAnimationFrame(step);
          } else {
              element.textContent = end;
          }
      };
      window.requestAnimationFrame(step);
  }
});