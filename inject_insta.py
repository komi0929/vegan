import os
import re

filepath = r"c:\Users\soyst\OneDrive\デスクトップ\vegan\js\live-content.js"

with open(filepath, 'r', encoding='utf-8') as f:
    js = f.read()

new_insta_func = """
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
"""

old_func_pattern = r'function renderInstagramSection\(\) \{[\s\S]*?(?=// ============================================|function init\(\))'

new_js = re.sub(old_func_pattern, new_insta_func, js)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_js)
