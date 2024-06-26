let currentIndex = 0;

function showSlide(index) {
  const slides = document.querySelectorAll('.carousel-item-custom');
  
  if (index >= slides.length) {
    currentIndex = 0;
  } else if (index < 0) {
    currentIndex = slides.length - 1;
  } else {
    currentIndex = index;
  }
  
  slides.forEach((slide, i) => {
    
    slide.classList.remove('active');
    slide.classList.add('not-active');
    if (i === currentIndex) {
      slide.classList.add('active');
      slide.classList.remove('not-active');
    }
  });
}

function nextSlide() {
  showSlide(currentIndex + 1);
}

function prevSlide() {
  showSlide(currentIndex - 1);
}

document.addEventListener('DOMContentLoaded', () => {
  showSlide(currentIndex);
});


