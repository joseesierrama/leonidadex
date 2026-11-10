const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../src/assets/privacidad.js'), 'utf8');

function setup({ choice = null, id = 'G-TEST123456', storageBlocked = false, dialogSupported = true } = {}) {
  const tags = [], events = {}, storage = new Map();
  if (choice) storage.set('ld:consent:v1', JSON.stringify(choice));
  const dialog = { open: false, close() { this.open = false; } };
  if (dialogSupported) dialog.showModal = function () { this.open = true; };
  const button = { hidden: true, focus() {}, addEventListener(type, fn) { events.open = fn; } };
  const context = {
    document: {
      currentScript: { dataset: { ga4: id } }, cookie: '',
      head: { appendChild(tag) { tags.push(tag); } },
      createElement() { return {}; },
      querySelectorAll() { return [button]; },
      getElementById(name) { return name === 'privacyDialog' ? dialog : { addEventListener(type, fn) { events[name] = fn; } }; }
    },
    location: { hostname: 'leonidadex.net', reload() { context.reloads++; } },
    localStorage: {
      getItem(key) { if (storageBlocked) throw Error('denied'); return storage.get(key) || null; },
      setItem(key, value) { if (storageBlocked) throw Error('denied'); storage.set(key, value); }
    },
    Date, Number, encodeURIComponent, reloads: 0
  };
  context.window = context;
  vm.runInNewContext(source, context);
  return { context, tags, events, storage, dialog };
}

test('no Google request before a first choice; rejecting stays offline', () => {
  const app = setup();
  assert.equal(app.dialog.open, true);
  assert.equal(app.tags.length, 0);
  app.events.privacyReject();
  assert.equal(app.tags.length, 0);
  assert.equal(JSON.parse(app.storage.get('ld:consent:v1')).analytics, false);
});
test('acceptance loads once, and withdrawal reloads to stop the tag', () => {
  const app = setup();
  app.events.privacyAccept();
  assert.equal(app.tags.length, 1);
  assert.match(app.tags[0].src, /gtag\/js\?id=G-TEST123456$/);
  app.events.open();
  app.events.privacyAccept();
  assert.equal(app.tags.length, 1);
  app.events.open();
  app.events.privacyReject();
  assert.equal(app.context.reloads, 1);
  assert.equal(JSON.parse(app.storage.get('ld:consent:v1')).analytics, false);
  const states = app.context.dataLayer.filter(x => x[0] === 'consent');
  assert.equal(states.at(-1)[2].analytics_storage, 'denied');
  assert.equal(states[0][2].ad_storage, 'denied');
});
test('remembered rejection prevents a request on the next page', () => {
  const app = setup({ choice: { analytics: false, at: Date.now() } });
  assert.equal(app.dialog.open, false);
  assert.equal(app.tags.length, 0);
});
test('expired or future consent is not reused', () => {
  for (const at of [Date.now() - 181 * 86400000, Date.now() + 86400000]) {
    const app = setup({ choice: { analytics: true, at } });
    assert.equal(app.dialog.open, true);
    assert.equal(app.tags.length, 0);
  }
});
test('blocked storage or unsupported dialog never grants consent', () => {
  assert.equal(setup({ storageBlocked: true }).tags.length, 0);
  assert.equal(setup({ dialogSupported: false }).tags.length, 0);
});
test('empty ID disables measurement entirely', () => {
  const app = setup({ id: '' });
  assert.equal(app.tags.length, 0);
  assert.equal(app.dialog.open, false);
});
