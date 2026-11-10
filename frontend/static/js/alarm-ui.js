/* Suas IoT Intelligent Alarm — shared UI helpers.
 * Plain JavaScript (no module imports) so it works alongside the Gentelella
 * theme bundle without depending on hashed chunk filenames.
 */
(function () {
  'use strict';

  /* ---- Toast feedback (mirrors the theme's own toast markup) ---- */
  function toast(message, variant) {
    var host = document.querySelector('.toast-host');
    if (!host) {
      host = document.createElement('div');
      host.className = 'toast-host';
      host.setAttribute('role', 'status');
      host.setAttribute('aria-live', 'polite');
      document.body.appendChild(host);
    }
    var el = document.createElement('div');
    el.className = 'toast toast-' + (variant || 'success');
    el.textContent = message;
    host.appendChild(el);
    void el.getBoundingClientRect(); // force reflow so the transition runs
    el.classList.add('show');
    var hide = function () {
      el.classList.remove('show');
      el.addEventListener('transitionend', function () { el.remove(); }, { once: true });
    };
    setTimeout(hide, 3200);
    el.addEventListener('click', hide);
  }

  /* ---- Live date / clock ---- */
  function updateClock() {
    var now = new Date();
    document.querySelectorAll('[data-live-clock]').forEach(function (el) {
      el.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    });
    document.querySelectorAll('[data-live-date]').forEach(function (el) {
      el.textContent = now.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    });
  }
  if (document.querySelector('[data-live-clock], [data-live-date]')) {
    updateClock();
    setInterval(updateClock, 1000);
  }

  /* ---- Generic async form submission (progressive enhancement) ----
   * Forms tagged with [data-async-form] POST to their `action` via fetch and
   * show success/error toasts. Endpoints are expected on the backend; see the
   * templates for the exact URLs used.
   */
  document.addEventListener('submit', function (e) {
    var form = e.target && e.target.closest ? e.target.closest('[data-async-form]') : null;
    if (!form) return;
    e.preventDefault();

    var btn = form.querySelector('[type="submit"]');
    if (btn) btn.disabled = true;

    var data = new FormData(form);
    var isFile = Array.from(data.values()).some(function (v) { return v instanceof File; });
    var url = form.action || window.location.href;
    var options = { method: (form.method || 'POST').toUpperCase(), headers: {}, body: null };

    if (isFile) {
      options.body = data;
    } else {
      options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      options.body = new URLSearchParams(data).toString();
    }

    fetch(url, options)
      .then(function (res) {
        if (!res.ok) throw new Error('Request failed (' + res.status + ')');
        return res.json().catch(function () { return {}; });
      })
      .then(function (json) {
        toast(json.detail || json.message || 'Saved successfully', 'success');
        if (json.redirect) {
          window.location.href = json.redirect;
        } else {
          setTimeout(function () { window.location.reload(); }, 900);
        }
      })
      .catch(function (err) {
        toast('Could not save: ' + err.message, 'error');
      })
      .finally(function () {
        if (btn) btn.disabled = false;
      });
  });

  /* ---- Delete an alarm with confirmation ----
   * Endpoint expected: DELETE {data-url}
   */
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-delete-alarm]') : null;
    if (!btn) return;
    e.preventDefault();

    var url = btn.getAttribute('data-url');
    var label = btn.getAttribute('data-label') || 'this alarm';
    if (!window.confirm('Delete ' + label + '? This cannot be undone.')) return;

    var row = btn.closest('tr') || btn.closest('[data-alarm-row]');
    fetch(url, { method: 'DELETE', headers: { 'Accept': 'application/json' } })
      .then(function (res) {
        if (!res.ok) throw new Error('Request failed (' + res.status + ')');
        toast('Alarm deleted', 'success');
        if (row) row.remove();
        setTimeout(function () { window.location.reload(); }, 600);
      })
      .catch(function (err) {
        toast('Could not delete: ' + err.message, 'error');
      });
  });
  /* ---- Inline edit: populate the create/edit alarm form ---- */
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-edit-alarm]') : null;
    if (!btn) return;
    var form = document.getElementById('alarm-form');
    if (!form) return;

    var id = btn.getAttribute('data-id') || '';
    var idInput = form.querySelector('[name="id"]');
    if (idInput) idInput.value = id;
    var time = form.querySelector('[name="alarm_time"]');
    if (time) time.value = btn.getAttribute('data-time') || '';
    var sound = form.querySelector('[name="sound_file"]');
    if (sound) sound.value = btn.getAttribute('data-sound') || 'default_alarm.mp3';
    var enabled = form.querySelector('[name="enabled"]');
    if (enabled) enabled.checked = btn.getAttribute('data-enabled') !== 'false';

    var base = form.getAttribute('data-action-create') || form.action;
    form.action = base.replace(/\/$/, '') + '/' + id + '/update';
    form.setAttribute('data-edit', 'true');

    var submit = form.querySelector('[type="submit"]');
    if (submit) submit.textContent = 'Update alarm';
    var title = form.querySelector('[data-form-title]');
    if (title) title.textContent = 'Edit alarm';

    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  /* ---- Reset edit state when the alarm form is reset ---- */
  document.addEventListener('reset', function (e) {
    var form = e.target && e.target.closest ? e.target.closest('#alarm-form') : null;
    if (!form) return;
    setTimeout(function () {
      form.removeAttribute('data-edit');
      form.action = form.getAttribute('data-action-create') || form.action;
      var submit = form.querySelector('[type="submit"]');
      if (submit) submit.textContent = 'Create alarm';
      var title = form.querySelector('[data-form-title]');
      if (title) title.textContent = 'Create alarm';
    }, 0);
  });

  /* ---- Password confirmation validation ---- */
  document.querySelectorAll('[data-match]').forEach(function (input) {
    var target = document.querySelector(input.getAttribute('data-match'));
    if (!target) return;
    function check() {
      var mismatch = input.value !== '' && input.value !== target.value;
      input.classList.toggle('is-invalid', mismatch);
      var err = input.parentElement.querySelector('.form-error');
      if (mismatch) {
        if (!err) {
          err = document.createElement('div');
          err.className = 'form-error';
          input.parentElement.appendChild(err);
        }
        err.textContent = 'Passwords do not match.';
        input.setCustomValidity('Passwords do not match.');
      } else {
        if (err) err.remove();
        input.setCustomValidity('');
      }
    }
    input.addEventListener('input', check);
    target.addEventListener('input', check);
  });

  /* ---- Alarm enable/disable toggle (schedule page) ----
   * Endpoint expected: PATCH {data-url}
   */
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-toggle-alarm]') : null;
    if (!btn) return;
    e.preventDefault();
    var url = btn.getAttribute('data-url');
    fetch(url, { method: 'PATCH', headers: { 'Accept': 'application/json' } })
      .then(function (res) {
        if (!res.ok) throw new Error('Request failed (' + res.status + ')');
        toast('Alarm updated', 'success');
        setTimeout(function () { window.location.reload(); }, 600);
      })
      .catch(function (err) {
        toast('Could not update: ' + err.message, 'error');
      });
  });
})();
