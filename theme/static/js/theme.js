(function () {
  'use strict';

  const STORAGE_KEY = 'theme';
  const ATTR = 'data-theme';
  const TOGGLE_ID = 'themeToggle';

  function getStoredTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function setStoredTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      // ignored
    }
  }

  function getPreferredTheme() {
    const stored = getStoredTheme();
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute(ATTR, theme);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute(ATTR) || getPreferredTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    setStoredTheme(next);
  }

  // Initialize on load
  applyTheme(getPreferredTheme());

  // Bind toggle button
  const btn = document.getElementById(TOGGLE_ID);
  if (btn) {
    btn.addEventListener('click', toggleTheme);
  }

  // Listen for OS theme changes when no override is stored
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    if (!getStoredTheme()) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // Copy button for code blocks
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('pre').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = 'copy';
      btn.setAttribute('aria-label', 'Copy code');
      btn.addEventListener('click', function () {
        var code = pre.querySelector('code');
        var text = code ? code.innerText : pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = 'copied!';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'copy';
            btn.classList.remove('copied');
          }, 2000);
        });
      });
      pre.appendChild(btn);
    });
  });

})();
