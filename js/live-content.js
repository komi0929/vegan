/**
 * SoyStories — Live Content Engine
 * 
 * Self-evolving content system that automatically pulls and displays:
 * 1. Google Reviews via Places API (when API key configured)
 * 2. Fallback reviews from data/reviews.json
 * 3. Instagram feed embed
 * 4. Real-time freshness indicators
 * 
 * Architecture: Tries Google API first → Falls back to JSON → Always renders
 */
(function () {
  'use strict';

  // ============================================
  // CONFIG
  // ============================================
  const CONFIG = {
    // Set your Google Maps API key here to enable live reviews
    // Get one at: https://console.cloud.google.com/apis/credentials
    GOOGLE_API_KEY: '',
    GOOGLE_PLACE_ID: 'ChIJL8ZEXVgRVDURgePVwM_GJ6E',
    REVIEWS_JSON_PATH: (function() {
      var p = window.location.pathname;
      if (p.includes('/en/') || p.includes('/ko/') || p.includes('/zh-cn/') || p.includes('/zh-tw/')) {
        return '../data/reviews.json';
      }
      return './data/reviews.json';
    })(),
    INSTAGRAM_USERNAME: 'soystories_yakuin',
    MAX_REVIEWS: 6,
    ROTATION_INTERVAL: 5000, // ms between auto-scroll
  };

  // ============================================
  // LANGUAGE DETECTION
  // ============================================
  function detectLang() {
    const path = window.location.pathname;
    if (path.includes('/ko/')) return 'ko';
    if (path.includes('/zh-cn/')) return 'zh-cn';
    if (path.includes('/zh-tw/')) return 'zh-tw';
    if (path.includes('/en/')) return 'en';
    return 'ja';
  }

  const LANG = detectLang();

  // ============================================
  // I18N STRINGS
  // ============================================
  const I18N = {
    en: {
      liveTitle: 'Real Voices from Travelers',
      liveSub: 'Reviews update automatically',
      liveLabel: 'LIVE',
      googleLabel: 'Google Reviews',
      happycowLabel: 'HappyCow',
      basedOn: 'Based on {count} reviews',
      readMore: 'Read all reviews on {source}',
      via: 'via',
      instaTitle: 'Follow Our Story',
      instaSub: '@soystories_yakuin on Instagram',
      updated: 'Last updated',
      ago: 'ago',
      days: 'days',
      hours: 'hours',
      minutes: 'min',
    },
    ko: {
      liveTitle: '전 세계 여행자들의 생생한 후기',
      liveSub: '리뷰가 자동으로 업데이트됩니다',
      liveLabel: 'LIVE',
      googleLabel: 'Google 리뷰',
      happycowLabel: 'HappyCow',
      basedOn: '{count}개의 리뷰 기반',
      readMore: '{source}에서 모든 리뷰 보기',
      via: 'via',
      instaTitle: '우리의 이야기를 팔로우하세요',
      instaSub: 'Instagram @soystories_yakuin',
      updated: '최종 업데이트',
      ago: '전',
      days: '일',
      hours: '시간',
      minutes: '분',
    },
    'zh-cn': {
      liveTitle: '来自全球旅客的真实心声',
      liveSub: '评价自动实时更新',
      liveLabel: 'LIVE',
      googleLabel: 'Google 评价',
      happycowLabel: 'HappyCow',
      basedOn: '基于 {count} 条评价',
      readMore: '在 {source} 查看全部评价',
      via: 'via',
      instaTitle: '关注我们的故事',
      instaSub: 'Instagram @soystories_yakuin',
      updated: '最后更新',
      ago: '前',
      days: '天',
      hours: '小时',
      minutes: '分钟',
    },
    'zh-tw': {
      liveTitle: '來自全球旅客的真實心聲',
      liveSub: '評價自動即時更新',
      liveLabel: 'LIVE',
      googleLabel: 'Google 評價',
      happycowLabel: 'HappyCow',
      basedOn: '基於 {count} 則評價',
      readMore: '在 {source} 查看全部評價',
      via: 'via',
      instaTitle: '關注我們的故事',
      instaSub: 'Instagram @soystories_yakuin',
      updated: '最後更新',
      ago: '前',
      days: '天',
      hours: '小時',
      minutes: '分鐘',
    },
    ja: {
      liveTitle: '世界中の旅行者のリアルな声',
      liveSub: 'レビューは自動更新されます',
      liveLabel: 'LIVE',
      googleLabel: 'Google レビュー',
      happycowLabel: 'HappyCow',
      basedOn: '{count}件のレビューに基づく',
      readMore: '{source}で全レビューを見る',
      via: 'via',
      instaTitle: '私たちのストーリーをフォロー',
      instaSub: 'Instagram @soystories_yakuin',
      updated: '最終更新',
      ago: '前',
      days: '日',
      hours: '時間',
      minutes: '分',
    }
  };

  function t(key) {
    return (I18N[LANG] || I18N['en'])[key] || I18N['en'][key] || key;
  }

  // ============================================
  // COUNTRY FLAG EMOJI
  // ============================================
  function countryFlag(code) {
    if (!code || code.length !== 2) return '🌍';
    const offset = 127397;
    return String.fromCodePoint(
      code.charCodeAt(0) + offset,
      code.charCodeAt(1) + offset
    );
  }

  // ============================================
  // TIME AGO
  // ============================================
  function timeAgo(dateStr) {
    const now = new Date();
    const date = new Date(dateStr);
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / 86400000);
    if (diffDays > 0) return diffDays + ' ' + t('days') + ' ' + t('ago');
    const diffHours = Math.floor(diffMs / 3600000);
    if (diffHours > 0) return diffHours + ' ' + t('hours') + ' ' + t('ago');
    const diffMin = Math.floor(diffMs / 60000);
    return diffMin + ' ' + t('minutes') + ' ' + t('ago');
  }

  // ============================================
  // RENDER STARS
  // ============================================
  function renderStars(rating) {
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.5 ? 1 : 0;
    return '★'.repeat(full) + (half ? '☆' : '') + '☆'.repeat(5 - full - half);
  }

  // ============================================
  // BUILD REVIEW CARD HTML
  // ============================================
  function buildReviewCard(review) {
    const text = (typeof review.text === 'object')
      ? (review.text[LANG] || review.text['en'] || Object.values(review.text)[0])
      : review.text;
    const flag = countryFlag(review.countryCode);
    const ago = review.date ? timeAgo(review.date) : '';
    const photo = review.photoUrl
      ? '<img class="live-review__photo" src="' + review.photoUrl + '" alt="Review photo">'
      : '';

    return '<div class="live-review__card">' +
      '<div class="live-review__header">' +
        '<div class="live-review__avatar">' + flag + '</div>' +
        '<div class="live-review__meta">' +
          '<span class="live-review__author">' + (review.author || 'Traveler') + '</span>' +
          '<span class="live-review__origin">' + (review.country || '') + '</span>' +
        '</div>' +
        '<div class="live-review__source-badge">' + (review.source || 'Google') + '</div>' +
      '</div>' +
      '<div class="live-review__stars">' + renderStars(review.rating || 5) + '</div>' +
      photo +
      '<p class="live-review__text">"' + text + '"</p>' +
      '<span class="live-review__date">' + ago + '</span>' +
    '</div>';
  }

  // ============================================
  // RENDER LIVE REVIEWS SECTION
  // ============================================
  function renderLiveSection(reviews, meta) {
    const container = document.getElementById('live-reviews');
    if (!container) return;

    const googleRating = (meta && meta.sources && meta.sources.google)
      ? meta.sources.google.rating : 4.8;
    const googleCount = (meta && meta.sources && meta.sources.google)
      ? meta.sources.google.reviewCount : 120;
    const hcRating = (meta && meta.sources && meta.sources.happycow)
      ? meta.sources.happycow.rating : 5.0;

    let cardsHtml = '';
    const maxReviews = Math.min(reviews.length, CONFIG.MAX_REVIEWS);
    for (let i = 0; i < maxReviews; i++) {
      cardsHtml += buildReviewCard(reviews[i]);
    }

    container.innerHTML =
      '<div class="live-reviews__inner">' +
        '<div class="live-reviews__header">' +
          '<h2 class="live-reviews__title">' + t('liveTitle') + '</h2>' +
          '<div class="live-reviews__live-badge">' +
            '<span class="live-dot"></span> ' + t('liveLabel') +
          '</div>' +
        '</div>' +
        '<p class="live-reviews__subtitle">' + t('liveSub') + '</p>' +
        // Rating summary bar
        '<div class="live-reviews__summary">' +
          '<div class="live-reviews__source-card">' +
            '<img src="https://www.google.com/favicon.ico" alt="Google" class="live-reviews__source-icon">' +
            '<div>' +
              '<div class="live-reviews__source-rating">' + googleRating.toFixed(1) + ' <span class="live-reviews__source-stars">' + renderStars(googleRating) + '</span></div>' +
              '<div class="live-reviews__source-count">' + t('basedOn').replace('{count}', googleCount) + '</div>' +
            '</div>' +
          '</div>' +
          '<div class="live-reviews__source-card">' +
            '<img src="https://www.happycow.net/favicon.ico" alt="HappyCow" class="live-reviews__source-icon">' +
            '<div>' +
              '<div class="live-reviews__source-rating">' + hcRating.toFixed(1) + ' <span class="live-reviews__source-stars">' + renderStars(hcRating) + '</span></div>' +
              '<div class="live-reviews__source-count">' + t('basedOn').replace('{count}', '50+') + '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        // Review cards carousel
        '<div class="live-reviews__track-wrapper">' +
          '<div class="live-reviews__track" id="live-reviews-track">' +
            cardsHtml +
          '</div>' +
        '</div>' +
        '<div class="live-reviews__nav">' +
          '<button class="live-reviews__nav-btn" id="live-prev" aria-label="Previous">&lsaquo;</button>' +
          '<div class="live-reviews__dots" id="live-dots"></div>' +
          '<button class="live-reviews__nav-btn" id="live-next" aria-label="Next">&rsaquo;</button>' +
        '</div>' +
      '</div>';

    initCarousel(maxReviews);
  }

  // ============================================
  // CAROUSEL LOGIC
  // ============================================
  function initCarousel(totalCards) {
    const track = document.getElementById('live-reviews-track');
    const dotsContainer = document.getElementById('live-dots');
    const prevBtn = document.getElementById('live-prev');
    const nextBtn = document.getElementById('live-next');
    if (!track || !dotsContainer) return;

    let current = 0;
    // On mobile show 1, tablet 2, desktop 3
    function getVisible() {
      if (window.innerWidth < 640) return 1;
      if (window.innerWidth < 1024) return 2;
      return 3;
    }

    function getMaxIndex() {
      return Math.max(0, totalCards - getVisible());
    }

    function buildDots() {
      dotsContainer.innerHTML = '';
      const maxIdx = getMaxIndex();
      for (let i = 0; i <= maxIdx; i++) {
        var dot = document.createElement('span');
        dot.className = 'live-reviews__dot' + (i === current ? ' active' : '');
        dot.setAttribute('data-index', i);
        dot.addEventListener('click', function () {
          current = parseInt(this.getAttribute('data-index'));
          update();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function update() {
      var vis = getVisible();
      var pct = (current / totalCards) * 100;
      track.style.transform = 'translateX(-' + pct + '%)';
      // Update dots
      var dots = dotsContainer.querySelectorAll('.live-reviews__dot');
      for (var i = 0; i < dots.length; i++) {
        dots[i].className = 'live-reviews__dot' + (i === current ? ' active' : '');
      }
    }

    if (prevBtn) prevBtn.addEventListener('click', function () {
      current = Math.max(0, current - 1);
      update();
    });
    if (nextBtn) nextBtn.addEventListener('click', function () {
      current = Math.min(getMaxIndex(), current + 1);
      update();
    });

    buildDots();

    // Auto-rotate
    var autoTimer = setInterval(function () {
      current = current >= getMaxIndex() ? 0 : current + 1;
      update();
    }, CONFIG.ROTATION_INTERVAL);

    // Pause on hover
    track.addEventListener('mouseenter', function () { clearInterval(autoTimer); });
    track.addEventListener('mouseleave', function () {
      autoTimer = setInterval(function () {
        current = current >= getMaxIndex() ? 0 : current + 1;
        update();
      }, CONFIG.ROTATION_INTERVAL);
    });

    // Recalc on resize
    window.addEventListener('resize', function () {
      current = Math.min(current, getMaxIndex());
      buildDots();
      update();
    });
  }

  // ============================================
  // FETCH: GOOGLE PLACES API
  // ============================================
  function fetchGoogleReviews() {
    return new Promise(function (resolve, reject) {
      if (!CONFIG.GOOGLE_API_KEY) {
        reject('No API key');
        return;
      }
      // Dynamically load Google Maps JS API
      if (!window.google || !window.google.maps) {
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?key=' +
          CONFIG.GOOGLE_API_KEY + '&libraries=places&callback=__gmapsReady';
        script.async = true;
        window.__gmapsReady = function () {
          doFetch(resolve, reject);
        };
        document.head.appendChild(script);
      } else {
        doFetch(resolve, reject);
      }
    });

    function doFetch(resolve, reject) {
      var service = new google.maps.places.PlacesService(
        document.createElement('div')
      );
      service.getDetails(
        { placeId: CONFIG.GOOGLE_PLACE_ID, fields: ['reviews', 'rating', 'user_ratings_total'] },
        function (place, status) {
          if (status === google.maps.places.PlacesServiceStatus.OK && place.reviews) {
            var reviews = place.reviews.map(function (r) {
              return {
                source: 'Google',
                author: r.author_name,
                rating: r.rating,
                date: new Date(r.time * 1000).toISOString(),
                text: r.text,
                photoUrl: r.profile_photo_url || null,
                country: '',
                countryCode: ''
              };
            });
            resolve({
              reviews: reviews,
              meta: {
                sources: {
                  google: { rating: place.rating, reviewCount: place.user_ratings_total }
                }
              }
            });
          } else {
            reject('Places API error: ' + status);
          }
        }
      );
    }
  }

  // ============================================
  // FETCH: JSON FALLBACK
  // ============================================
  function fetchJsonReviews() {
    return fetch(CONFIG.REVIEWS_JSON_PATH)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        return {
          reviews: data.featured || [],
          meta: data
        };
      });
  }

  // ============================================
  // INSTAGRAM SECTION
  // ============================================
  
  // ============================================
  // INSTAGRAM SECTION (DYNAMIC FEED)
  // ============================================
  function renderInstagramSection() {
    var container = document.getElementById('instagram-feed');
    if (!container) return;

    var instaJsonPath = (function() {
      var p = window.location.pathname;
      if (p.includes('/en/') || p.includes('/ko/') || p.includes('/zh-cn/') || p.includes('/zh-tw/')) {
        return '../data/instagram.json';
      }
      return './data/instagram.json';
    })();

    fetch(instaJsonPath)
      .then(function(res) { return res.json(); })
      .then(function(data) {
        var postsHtml = '';
        var posts = data.posts || [];
        for (var i = 0; i < Math.min(posts.length, 6); i++) {
          var p = posts[i];
          postsHtml += '<a href="' + p.link + '" target="_blank" rel="noopener" class="instagram-feed__item" aria-label="View Instagram Post">' +
                         '<img src="' + p.imageUrl + '" alt="' + (p.caption || 'Instagram Post').replace(/"/g, '&quot;') + '" class="instagram-feed__img" loading="lazy">' +
                         '<div class="instagram-feed__overlay">' +
                           '<svg viewBox="0 0 24 24" width="24" height="24" fill="white"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>' +
                         '</div>' +
                       '</a>';
        }

        container.innerHTML =
          '<div class="instagram-section__inner inner">' +
            '<div class="instagram-section__header">' +
              '<h2 class="instagram-section__title">' + t('instaTitle') + '</h2>' +
              '<p class="instagram-section__subtitle">' + t('instaSub') + '</p>' +
            '</div>' +
            '<div class="instagram-feed__grid">' +
              postsHtml +
            '</div>' +
            '<div class="instagram-section__cta" style="margin-top:24px;text-align:center;">' +
              '<a href="https://www.instagram.com/' + CONFIG.INSTAGRAM_USERNAME + '/" target="_blank" rel="noopener" class="instagram-section__btn" style="display:inline-flex;align-items:center;gap:8px;padding:12px 24px;background:#e1306c;color:white;text-decoration:none;border-radius:24px;font-weight:bold;transition:opacity 0.3s;">' +
                '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>' +
                'Follow @' + CONFIG.INSTAGRAM_USERNAME +
              '</a>' +
            '</div>' +
          '</div>';
      })
      .catch(function(err) {
        console.warn('Could not load Instagram JSON', err);
      });
  }
// ============================================
  // MAIN INIT
  // ============================================
  function init() {
    // Try Google API first, fallback to JSON
    fetchGoogleReviews()
      .then(function (data) {
        // Merge Google reviews with JSON reviews for variety
        fetchJsonReviews().then(function (jsonData) {
          var merged = data.reviews.concat(jsonData.reviews || []);
          // Deduplicate by id/author
          var seen = {};
          var unique = [];
          merged.forEach(function (r) {
            var key = (r.id || r.author || '') + r.source;
            if (!seen[key]) { seen[key] = true; unique.push(r); }
          });
          renderLiveSection(unique, {
            sources: Object.assign({}, (jsonData.meta || {}).sources, data.meta.sources)
          });
        }).catch(function () {
          renderLiveSection(data.reviews, data.meta);
        });
      })
      .catch(function () {
        // Fallback: use JSON data
        fetchJsonReviews()
          .then(function (data) {
            renderLiveSection(data.reviews, data);
          })
          .catch(function (err) {
            console.warn('SoyStories Live Content: Could not load reviews', err);
          });
      });

    renderInstagramSection();
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
