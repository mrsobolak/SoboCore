/* Sobolak Technologies */
(function () {
  'use strict';

  // How people reach you. Fill these in and the Contact section shows the buttons.
  var CONTACT = {
    email: '',
    phone: ''
  };
  var UPDATED = 'November 18, 2026';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

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

  /* contact buttons */
  var contact = document.getElementById('contact-actions');
  if (contact) {
    var html = '';
    if (CONTACT.email) {
      html += '<a class="btn btn-gel" href="mailto:' + esc(CONTACT.email) + '?subject=' +
        encodeURIComponent('Question for Sobolak Technologies') + '">Email ' + esc(CONTACT.email) + '</a>';
    }
    if (CONTACT.phone) {
      html += '<a class="btn btn-glass" href="tel:' + esc(String(CONTACT.phone).replace(/[^+\d]/g, '')) +
        '">Call or text ' + esc(CONTACT.phone) + '</a>';
    }
    if (!html) html = '<p class="contact-pending">Contact details are being set up. Check back shortly.</p>';
    contact.innerHTML = html;
  }
})();
