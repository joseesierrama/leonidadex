(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.LDXMapProgress = api;
})(typeof window === 'object' ? window : this, function () {
  'use strict';
  function clean(value) {
    var out = {};
    if (!value || typeof value !== 'object' || Array.isArray(value)) return out;
    Object.keys(value).forEach(function (id) {
      if (/^(?:[a-z0-9][a-z0-9-]{0,99}|g:[1-9][0-9]{0,7})$/.test(id) && id !== 'constructor' && id !== 'prototype' && (value[id] === 1 || value[id] === true)) out[id] = 1;
    });
    return out;
  }
  function read(storage) {
    try { return clean(JSON.parse(storage.getItem('ldx-found') || '{}')); } catch (_) { return {}; }
  }
  function write(storage, found) {
    try { storage.setItem('ldx-found', JSON.stringify(clean(found))); return true; } catch (_) { return false; }
  }
  function matches(found, id, status) {
    return status === 'pending' ? !found[id] : status === 'done' ? !!found[id] : true;
  }
  function backup(found) {
    return JSON.stringify({site: 'leonidadex.net', game: 'GTA VI', version: 1, completed: clean(found)}, null, 2);
  }
  function restore(text, current) {
    var data = JSON.parse(text);
    if (!data || data.site !== 'leonidadex.net' || data.game !== 'GTA VI' || data.version !== 1 || !data.completed || typeof data.completed !== 'object' || Array.isArray(data.completed)) throw Error('Elige una copia de progreso de LeonidaDex para GTA VI.');
    return Object.assign(clean(current), clean(data.completed));
  }
  return {clean: clean, read: read, write: write, matches: matches, backup: backup, restore: restore};
});
