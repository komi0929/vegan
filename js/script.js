const drawerIcon = document.querySelector('#js-drawer-icon');
const drawerContent = document.querySelector('#js-drawer-content');
const drawerLinks = document.querySelectorAll('.drawer-content__link');

if (drawerIcon) {
  drawerIcon.addEventListener('click', function(e) {
      e.preventDefault();
      drawerIcon.classList.toggle('is-checked');
      drawerContent.classList.toggle('is-checked');
  });
}

for(let i = 0; i < drawerLinks.length; i++) {
  drawerLinks[i].addEventListener('click', function(e) {
    drawerIcon.classList.remove('is-checked');
    drawerContent.classList.remove('is-checked');
  });
}

// if (drawerLinks) {
//   drawerLinks.forEach(function(link) {
//     link.addEventListener('click', function(e) {
//       drawerIcon.classList.remove('is-checked');
//       drawerContent.classList.remove('is-checked');
//     });
//   });
// }


const swiper = new Swiper('.swiper', {
    // Optional parameters
    loop: true,
    autoplay: {
      delay: 2000,
      pauseOnMouseEnter: true,
      disableOnInteraction: false,
  },
  speed: 2000,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  });