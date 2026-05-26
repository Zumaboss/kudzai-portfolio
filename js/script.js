const obs = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 55);
      obs.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(r => obs.observe(r));

function handleSubmit(e) {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-submit');
  const msg = document.getElementById('form-msg');
  btn.textContent = 'Sending...';
  btn.disabled = true;
  setTimeout(() => {
    btn.textContent = 'Message Sent \u2713';
    msg.textContent = 'Thank you! Kudzaiishe will be in touch shortly.';
  }, 1200);
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form.form-grid');
  if (form) form.addEventListener('submit', handleSubmit);
});
