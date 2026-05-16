/**
 * SoyStories — Inbound Conversion Engine
 * Dynamic features: OPEN NOW indicator, scroll animations
 */
(function() {
  'use strict';

  // ============================================
  // OPEN NOW INDICATOR
  // ============================================
  function updateOpenStatus() {
    const indicator = document.getElementById('open-indicator');
    if (!indicator) return;

    // SoyStories hours: 11:00 - 22:00 JST, every day
    const now = new Date();
    // Convert to JST (UTC+9)
    const jst = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Tokyo' }));
    const hour = jst.getHours();
    const minute = jst.getMinutes();
    const currentMinutes = hour * 60 + minute;
    
    const openTime = 11 * 60;  // 11:00
    const closeTime = 22 * 60; // 22:00

    const isOpen = currentMinutes >= openTime && currentMinutes < closeTime;
    
    const dot = indicator.querySelector('.open-indicator__dot');
    const text = indicator.querySelector('.open-indicator__text');
    
    if (isOpen) {
      indicator.className = 'open-indicator open-indicator--open';
      text.textContent = 'OPEN NOW · until 22:00';
    } else {
      indicator.className = 'open-indicator open-indicator--closed';
      if (currentMinutes < openTime) {
        text.textContent = 'Opens at 11:00 today';
      } else {
        text.textContent = 'Closed · Opens 11:00 tomorrow';
      }
    }
  }

  // Update every minute
  updateOpenStatus();
  setInterval(updateOpenStatus, 60000);

  // ============================================
  // SCROLL ANIMATIONS (Intersection Observer)
  // ============================================
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    document.querySelectorAll('.safety-card, .review-card').forEach(function(el) {
      observer.observe(el);
    });
  }

  // ============================================
  // LOCALIZED OPEN STATUS TEXT
  // ============================================
  // Detect language from URL path
  const path = window.location.pathname;
  let lang = 'en';
  if (path.includes('/ko/')) lang = 'ko';
  else if (path.includes('/zh-cn/')) lang = 'zh-cn';
  else if (path.includes('/zh-tw/')) lang = 'zh-tw';
  else if (!path.includes('/en/')) lang = 'ja';

  const translations = {
    'en': { open: 'OPEN NOW · until 22:00', closedTomorrow: 'Closed · Opens 11:00 tomorrow', opensToday: 'Opens at 11:00 today' },
    'ko': { open: '영업 중 · 22:00까지', closedTomorrow: '영업 종료 · 내일 11:00 오픈', opensToday: '오늘 11:00 오픈' },
    'zh-cn': { open: '营业中 · 至 22:00', closedTomorrow: '已关店 · 明天 11:00 开门', opensToday: '今天 11:00 开门' },
    'zh-tw': { open: '營業中 · 至 22:00', closedTomorrow: '已關店 · 明天 11:00 開門', opensToday: '今天 11:00 開門' },
    'ja': { open: '営業中 · 22:00まで', closedTomorrow: '閉店 · 明日 11:00 オープン', opensToday: '本日 11:00 オープン' }
  };

  // Override with localized text
  function updateLocalizedStatus() {
    const indicator = document.getElementById('open-indicator');
    if (!indicator) return;
    const text = indicator.querySelector('.open-indicator__text');
    if (!text) return;
    
    const t = translations[lang] || translations['en'];
    const now = new Date();
    const jst = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Tokyo' }));
    const currentMinutes = jst.getHours() * 60 + jst.getMinutes();
    
    if (currentMinutes >= 660 && currentMinutes < 1320) {
      text.textContent = t.open;
    } else if (currentMinutes < 660) {
      text.textContent = t.opensToday;
    } else {
      text.textContent = t.closedTomorrow;
    }
  }

  setTimeout(updateLocalizedStatus, 100);

})();
