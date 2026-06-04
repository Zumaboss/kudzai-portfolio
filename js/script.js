const obs = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 55);
      obs.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(r => obs.observe(r));

function updateThemeToggle(theme) {
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;
  const isDark = theme === 'dark';
  toggle.setAttribute('aria-pressed', String(isDark));
  toggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  updateThemeToggle(theme);
}

function initTheme() {
  const storedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = storedTheme || (prefersDark ? 'dark' : 'light');
  setTheme(theme);

  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;
  toggle.addEventListener('click', () => {
    const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', nextTheme);
    setTheme(nextTheme);
  });
}

function handleSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const nameField = form.querySelector('#fname');
  const emailField = form.querySelector('#email');
  const messageField = form.querySelector('#message');
  const serviceField = form.querySelector('#service');
  const btn = form.querySelector('.btn-submit');
  const msg = document.getElementById('form-msg');

  [nameField, emailField, messageField].forEach(field => field.classList.remove('invalid'));
  msg.textContent = '';

  let valid = true;
  if (!nameField.value.trim()) {
    nameField.classList.add('invalid');
    valid = false;
  }
  if (!emailField.value.trim() || !emailField.checkValidity()) {
    emailField.classList.add('invalid');
    valid = false;
  }
  if (!messageField.value.trim()) {
    messageField.classList.add('invalid');
    valid = false;
  }

  if (!valid) {
    msg.textContent = 'Please complete all required fields before sending.';
    msg.style.color = '#f96e6e';
    const firstInvalid = form.querySelector('.invalid');
    if (firstInvalid) firstInvalid.focus();
    return;
  }

  btn.textContent = 'Sending...';
  btn.disabled = true;
  msg.style.color = 'var(--accent)';
  msg.textContent = '';

  setTimeout(() => {
    btn.textContent = 'Message Sent \u2713';
    msg.textContent = 'Thank you! Kudzaiishe will be in touch shortly.';
    form.reset();
    btn.disabled = false;
  }, 1200);
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form.form-grid');
  if (form) form.addEventListener('submit', handleSubmit);
  initTheme();
});

// Lightbox functionality
const lightbox = document.getElementById('lightbox');
const lbImg = lightbox?.querySelector('.lb-img');
const lbCaption = lightbox?.querySelector('.lb-caption');
const lbClose = lightbox?.querySelector('.lb-close');
let lastFocusedElement = null;

function openLightbox(src, alt) {
  if (!lightbox || !lbImg || !lbCaption || !lbClose) return;

  lastFocusedElement = document.activeElement;
  lbImg.src = src;
  lbImg.alt = alt || '';
  lbCaption.textContent = alt || '';
  lightbox.classList.add('active');
  lightbox.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  lbClose.focus();
}

function closeLightbox() {
  if (!lightbox || !lbImg || !lbCaption) return;

  lightbox.classList.remove('active');
  lightbox.setAttribute('aria-hidden', 'true');
  lbImg.src = '';
  lbCaption.textContent = '';
  document.body.style.overflow = '';
  if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
    lastFocusedElement.focus();
  }
}

function handleLightboxKeydown(e) {
  if (!lightbox?.classList.contains('active')) return;
  if (e.key === 'Escape') {
    closeLightbox();
    return;
  }

  if (e.key === 'Tab') {
    e.preventDefault();
    lbClose.focus();
  }
}

function registerLightboxTriggers() {
  const thumbnails = document.querySelectorAll('.portfolio-gallery img, .portfolio-img img');
  thumbnails.forEach(img => {
    img.tabIndex = 0;
    img.addEventListener('click', (e) => {
      openLightbox(e.currentTarget.src, e.currentTarget.alt || e.currentTarget.getAttribute('data-caption') || '');
    });
    img.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openLightbox(e.currentTarget.src, e.currentTarget.alt || e.currentTarget.getAttribute('data-caption') || '');
      }
    });
  });

  if (lbClose) {
    lbClose.addEventListener('click', closeLightbox);
  }
  if (lightbox) {
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
    lightbox.addEventListener('keydown', handleLightboxKeydown);
  }
  document.addEventListener('keydown', handleLightboxKeydown);
}

if (document.readyState !== 'loading') {
  registerLightboxTriggers();
} else {
  document.addEventListener('DOMContentLoaded', registerLightboxTriggers);
}
