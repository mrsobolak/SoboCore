/* Sobolak Technologies */
(function () {
  'use strict';

  var UPDATED = 'November 18, 2026';

  /* menu */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* footer date */
  var upd = document.getElementById('updated');
  if (upd) upd.textContent = UPDATED;

})();
