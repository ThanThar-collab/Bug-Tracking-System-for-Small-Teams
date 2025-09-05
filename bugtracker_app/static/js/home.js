 // Get the right image
  const rightImage = document.querySelector('.right-item img');

  // Observe when the section is in viewport
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        // Add shake class when visible
        rightImage.classList.add('floatShake');
      } else {
        // Remove shake class when out of view
        rightImage.classList.remove('floatShake');
      }
    });
  }, { threshold: 0.5 }); // Trigger when 50% of section is visible

  // Observe the overview section
  observer.observe(document.querySelector('.overview-dashboard'));
