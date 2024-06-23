// script.js
var nav = document.querySelector('nav');

window.addEventListener('scroll', function () {
  if (window.pageYOffset > 100) {
    nav.classList.add('bg-dark', 'shadow');
  } else {
    nav.classList.remove('bg-dark', 'shadow');
  }
});

// Autoplay carousel
$('#bannerCarousel').carousel({
  interval: 5000, // Changes slide every 5 seconds
  pause: false // Stops the carousel from pausing on mouse hover
});
