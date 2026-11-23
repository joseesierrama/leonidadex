const test = require('node:test');
const assert = require('node:assert/strict');
const progress = require('../src/assets/mapa-progreso.js');

test('existing discovered places survive and community IDs do not collide', () => {
  let saved = '{"vice-beach":1,"g:234":true,"234":1}';
  const storage = {getItem:()=>saved,setItem:(_,value)=>{saved=value;}};
  const state = progress.read(storage);
  assert.equal(state['vice-beach'],1);
  assert.equal(state['g:234'],1);
  delete state['234'];
  assert.equal(progress.write(storage,state),true);
  assert.deepEqual(progress.read(storage),{'vice-beach':1,'g:234':1});
});

test('corrupted or blocked storage does not prevent exploration', () => {
  assert.deepEqual(progress.read(null),{});
  assert.deepEqual(progress.read({getItem:()=>'{bad'}),{});
  assert.deepEqual(progress.clean([]),{});
  assert.deepEqual(progress.clean(JSON.parse('{"__proto__":true,"constructor":1,"g:abc":1,"valid":true,"not-done":"true"}')), {valid:1});
  assert.equal(progress.write({setItem:()=>{throw Error('quota');}}, {valid:1}),false);
});

test('pending and completed filters use the same state for both map layers', () => {
  const state = {'vice-beach':1,'g:234':1};
  for (const id of ['vice-beach','g:234']) {
    assert.equal(progress.matches(state,id,'all'),true);
    assert.equal(progress.matches(state,id,'done'),true);
    assert.equal(progress.matches(state,id,'pending'),false);
  }
  assert.equal(progress.matches(state,'g:235','done'),false);
  assert.equal(progress.matches(state,'g:235','pending'),true);
});

test('portable backup merges progress without accepting another game or wiping marks', () => {
  const text = progress.backup({'g:234':1,granero:1});
  assert.deepEqual(progress.restore(text,{beach:1}),{beach:1,'g:234':1,granero:1});
  for (const bad of ['{}','null','[]','{bad',text.replace('GTA VI','GTA V'),text.replace('leonidadex.net','example.org')]) assert.throws(()=>progress.restore(bad,{}));
});
