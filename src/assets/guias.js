(function () {
  'use strict';
  function norm(value) { return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
  function matches(card, query, category, videoOnly) {
    return (!category || category === 'Todas' || card.category === category) &&
      (!videoOnly || card.video) && norm(query).split(/\s+/).filter(Boolean).every(function (word) { return norm(card.search).includes(word); });
  }
  function videoURL(id, start, end) {
    if (!/^[A-Za-z0-9_-]{11}$/.test(id) || !Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end < 0 || (end && end <= start)) return null;
    return 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1&rel=0&start=' + start + (end ? '&end=' + end : '');
  }
  function mountVideo(block, doc) {
    var url = videoURL(block.dataset.videoId, Number(block.dataset.start), Number(block.dataset.end));
    var player = block.querySelector('[data-video-player]');
    if (!url || !player) return null;
    var iframe = doc.createElement('iframe');
    iframe.src = url;
    iframe.title = block.dataset.title || 'Recorrido de GTA VI';
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    player.replaceChildren(iframe);
    return iframe;
  }
  function readProgress(storage, key, total) {
    try {
      var value = JSON.parse(storage.getItem(key) || '{}');
      if (!value || Array.isArray(value) || typeof value !== 'object') return {};
      var clean = {};
      for (var i = 1; i <= total; i++) if (value[i] === true) clean[i] = true;
      return clean;
    } catch (e) { return {}; }
  }
  function init(doc, storage) {
    var form = doc.querySelector('[data-guide-filters]');
    if (form) {
      var cards = Array.from(doc.querySelectorAll('[data-guide-card]'));
      var input = doc.querySelector('#guide-search');
      var video = doc.querySelector('#guide-video-only');
      var category = 'Todas';
      var chips = Array.from(doc.querySelectorAll('[data-category-filter]'));
      function filter() {
        var shown = 0;
        cards.forEach(function (card) {
          var visible = matches({ category: card.dataset.category, video: card.dataset.hasVideo === '1', search: card.dataset.search }, input.value, category, video.checked);
          card.hidden = !visible;
          if (visible) shown++;
        });
        chips.forEach(function (chip) { chip.setAttribute('aria-pressed', String(chip.dataset.categoryFilter === category)); });
        doc.querySelector('[data-guide-count]').textContent = shown + ' de ' + cards.length + ' guías';
        doc.querySelector('[data-guide-empty]').hidden = shown !== 0;
      }
      form.hidden = false;
      form.addEventListener('submit', function (e) { e.preventDefault(); filter(); });
      input.addEventListener('input', filter);
      video.addEventListener('change', filter);
      chips.forEach(function (chip) { chip.addEventListener('click', function () { category = chip.dataset.categoryFilter; filter(); }); });
      doc.querySelector('[data-clear-filters]').addEventListener('click', function () { category = 'Todas'; input.value = ''; video.checked = false; filter(); input.focus(); });
      filter();
    }
    doc.querySelectorAll('[data-video-block]').forEach(function (block) {
      var button = block.querySelector('[data-load-video]');
      var player = block.querySelector('[data-video-player]');
      var poster = player.querySelector('.gv-poster');
      button.addEventListener('click', function () {
        if (!mountVideo(block, doc)) return;
        var slot = block.querySelector('[data-video-reset-slot]');
        var stop = doc.createElement('button');
        stop.type = 'button'; stop.textContent = 'Cerrar reproductor';
        stop.addEventListener('click', function () { player.replaceChildren(poster); slot.replaceChildren(); button.focus(); });
        slot.replaceChildren(stop);
      });
    });
    function reveal(hash) {
      var id;
      try { id = decodeURIComponent(hash.slice(1)); } catch (e) { return; }
      var target = doc.getElementById(id);
      if (!target) return;
      var gate = target.closest('[data-guide-spoilers]');
      if (gate) gate.open = true;
    }
    doc.querySelectorAll('a[data-reveal-guide]').forEach(function (link) { link.addEventListener('click', function () { reveal(link.getAttribute('href')); }); });
    if (doc.defaultView) {
      if (doc.defaultView.location.hash) reveal(doc.defaultView.location.hash);
      doc.defaultView.addEventListener('hashchange', function () { reveal(doc.defaultView.location.hash); });
    }
    var guide = doc.querySelector('[data-guide-id]');
    if (guide) {
      var boxes = Array.from(guide.querySelectorAll('input[data-step]'));
      var key = 'ldx-guia:' + guide.dataset.guideId;
      var saved = readProgress(storage, key, boxes.length);
      boxes.forEach(function (box) { box.checked = saved[box.dataset.step] === true; });
      function progress(save) {
        var done = {}, count = 0;
        boxes.forEach(function (box) {
          if (box.checked) { done[box.dataset.step] = true; count++; }
          box.closest('.gv-step').classList.toggle('is-done', box.checked);
        });
        guide.querySelector('[data-guide-progress]').textContent = count + ' de ' + boxes.length + ' pasos marcados';
        if (save) { try { storage.setItem(key, JSON.stringify(done)); } catch (e) {} }
      }
      boxes.forEach(function (box) { box.addEventListener('change', function () { progress(true); }); });
      guide.querySelector('[data-reset-guide]').addEventListener('click', function () { boxes.forEach(function (box) { box.checked = false; }); progress(true); });
      progress(false);
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { norm: norm, matches: matches, videoURL: videoURL, mountVideo: mountVideo, readProgress: readProgress, init: init };
  if (typeof document !== 'undefined') {
    var storage = null;
    try { storage = window.localStorage; } catch (e) {}
    init(document, storage);
  }
}());
