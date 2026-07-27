// Scroll reveal
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 55);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// Theme
const applyTheme = (theme) => {
  document.documentElement.dataset.theme = theme;
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;
  const isDark = theme === 'dark';
  toggle.setAttribute('aria-pressed', String(isDark));
  toggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
};

const initTheme = () => {
  const saved = localStorage.getItem('theme');
  const prefersDark = matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved ?? (prefersDark ? 'dark' : 'light'));

  document.querySelector('.theme-toggle')?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    applyTheme(next);
  });
};

// Contact form
const handleSubmit = (e) => {
  e.preventDefault();
  const form = e.currentTarget;
  const fields = {
    name:    form.querySelector('#fname'),
    email:   form.querySelector('#email'),
    message: form.querySelector('#message'),
  };
  const btn = form.querySelector('.btn-submit');
  const msg = document.getElementById('form-msg');

  Object.values(fields).forEach(f => f.classList.remove('invalid'));
  msg.textContent = '';

  const invalid = Object.values(fields).filter(
    f => !f.value.trim() || (f.type === 'email' && !f.checkValidity())
  );

  if (invalid.length) {
    invalid.forEach(f => f.classList.add('invalid'));
    msg.textContent = 'Please complete all required fields before sending.';
    msg.style.color = '#f96e6e';
    invalid[0].focus();
    return;
  }

  btn.textContent = 'Sending…';
  btn.disabled = true;

  fetch(form.action, {
    method: 'POST',
    body: new FormData(form),
    headers: { Accept: 'application/json' },
  })
    .then(async res => {
      if (res.ok) {
        btn.textContent = 'Message Sent ✓';
        msg.textContent = 'Thank you! Kudzaiishe will be in touch shortly.';
        msg.style.color = 'var(--accent-dk)';
        form.reset();
      } else {
        const data = await res.json().catch(() => null);
        msg.textContent =
          data?.errors?.map(err => err.message).join(', ') ??
          'Oops! There was a problem submitting your form.';
        msg.style.color = '#f96e6e';
        btn.textContent = 'Send Message →';
      }
    })
    .catch(() => {
      msg.textContent = 'Oops! There was a problem submitting your form.';
      msg.style.color = '#f96e6e';
      btn.textContent = 'Send Message →';
    })
    .finally(() => { btn.disabled = false; });
};

// Lightbox (IIFE keeps state private)
(() => {
  const lightbox = document.getElementById('lightbox');
  const lbImg     = lightbox?.querySelector('.lb-img');
  const lbCaption = lightbox?.querySelector('.lb-caption');
  const lbClose   = lightbox?.querySelector('.lb-close');
  let lastFocus   = null;

  const close = () => {
    lightbox?.classList.remove('active');
    lightbox?.setAttribute('aria-hidden', 'true');
    if (lbImg)     lbImg.src = '';
    if (lbCaption) lbCaption.textContent = '';
    document.body.style.overflow = '';
    lastFocus?.focus();
  };

  const open = (src, alt) => {
    if (!lightbox || !lbImg || !lbCaption) return;
    lastFocus = document.activeElement;
    lbImg.src = src;
    lbImg.alt = alt ?? '';
    lbCaption.textContent = alt ?? '';
    lightbox.classList.add('active');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    lbClose?.focus();
  };

  lbClose?.addEventListener('click', close);
  lightbox?.addEventListener('click', e => { if (e.target === lightbox) close(); });
  document.addEventListener('keydown', e => {
    if (!lightbox?.classList.contains('active')) return;
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'Tab') { e.preventDefault(); lbClose?.focus(); }
  });

  document.querySelectorAll('.portfolio-gallery img, .portfolio-img img').forEach(img => {
    img.tabIndex = 0;
    img.addEventListener('click', e => {
      open(e.currentTarget.src, e.currentTarget.alt || e.currentTarget.dataset.caption || '');
    });
    img.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open(e.currentTarget.src, e.currentTarget.alt || e.currentTarget.dataset.caption || '');
      }
    });
  });
})();

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('form.form-grid')?.addEventListener('submit', handleSubmit);
  initTheme();
});
