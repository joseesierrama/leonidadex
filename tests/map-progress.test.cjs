const test = require('node:test');
const assert = require('node:assert/strict');
const progress = require('../src/assets/mapa-progreso.js');
const icons = require('../src/assets/mapa-iconos.js');
const fs = require('node:fs');
const path = require('node:path');

test('game symbols are available locally and unknown places do not become gun shops', () => {
  for (const key of Object.keys(icons.files)) assert.ok(fs.existsSync(path.join(__dirname,'../src/assets/map-icons',icons.file(key))),key);
  assert.equal(icons.rowIcon([1,'',0,0,0,'','x',0]),'explore');
  assert.equal(icons.rowIcon([1,'',0,0,0,'','c',0,['guns','clothes']]),'gun');
  assert.equal(icons.isService([1,'',0,0,0,'','r',0]),false);
  assert.equal(icons.pinIcon({nombre:'Genuine Cowboy Hat · sombrero',cat:'raros'}),'collectible');
});

test('dense symbols separate on zoom while a selected location remains clickable', () => {
  const rows=[[1,'shop',0,10,10,'','c',0,['guns']],[2,'house',0,10.1,10,'','r',0],[3,'unknown',0,20,20,'','x',0]];
  const before=JSON.stringify(rows);
  assert.deepEqual(icons.layout(rows,1,null,true).map(r=>r[0]),[1]);
  assert.ok(icons.layout(rows,1,2,false).some(r=>r[0]===2));
  assert.equal(icons.layout(rows,.001,null,false).length,3);
  assert.equal(JSON.stringify(rows),before);
});

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
