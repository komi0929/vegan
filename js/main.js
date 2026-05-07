/* ============================================
   SoyStories — Main JavaScript
   ============================================ */
(function () {
  'use strict';

  /* ---------- Mobile Drawer ---------- */
  const ham = document.querySelector('.header__ham');
  const drawer = document.querySelector('.drawer');
  const drawerLinks = document.querySelectorAll('.drawer a');
  if (ham && drawer) {
    ham.addEventListener('click', () => {
      ham.classList.toggle('open');
      drawer.classList.toggle('open');
      document.body.style.overflow = drawer.classList.contains('open') ? 'hidden' : '';
    });
    drawerLinks.forEach(link => {
      link.addEventListener('click', () => {
        ham.classList.remove('open');
        drawer.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- Header scroll shadow ---------- */
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  /* ---------- Language Switcher ---------- */
  const langBtn = document.querySelector('.lang-sw__btn');
  const langDd = document.querySelector('.lang-sw__dd');
  if (langBtn && langDd) {
    langBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      langDd.classList.toggle('open');
    });
    document.addEventListener('click', () => langDd.classList.remove('open'));
  }

  /* ---------- FAQ Accordion ---------- */
  document.querySelectorAll('.faq__q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.closest('.faq__item');
      const wasOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq__item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* ---------- Scroll Fade-up Animation ---------- */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  /* ---------- Taxi Card Fullscreen ---------- */
  const taxiFS = document.querySelector('.taxi__fullscreen-btn');
  if (taxiFS) {
    taxiFS.addEventListener('click', () => {
      const taxi = document.querySelector('.taxi');
      if (taxi && taxi.requestFullscreen) {
        taxi.requestFullscreen();
      }
    });
  }

  /* ---------- Smooth scroll for anchor links ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = header ? header.offsetHeight : 0;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  /* ---------- Image slider (simple auto-rotate) ---------- */
  const sliders = document.querySelectorAll('.simple-slider');
  sliders.forEach(slider => {
    const slides = slider.querySelectorAll('.simple-slider__slide');
    if (slides.length <= 1) return;
    let idx = 0;
    slides[0].classList.add('active');
    setInterval(() => {
      slides[idx].classList.remove('active');
      idx = (idx + 1) % slides.length;
      slides[idx].classList.add('active');
    }, 3000);
  });
})();
