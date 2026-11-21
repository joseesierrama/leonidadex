const test = require('node:test');
const assert = require('node:assert/strict');
const ui = require('../src/assets/guias.js');

test('search combines topic, video and words without accents', () => {
  const card={category:'Exploración',video:true,search:'Meditación con Lucía en el balcón'};
  assert.equal(ui.matches(card,'lucia balcon','Exploración',true),true);
  assert.equal(ui.matches(card,'lucia coche','Todas',false),false);
  assert.equal(ui.matches(card,'','Armas',false),false);
  assert.equal(ui.matches({...card,video:false},'','Todas',true),false);
});
test('invalid IDs and clip ranges cannot create a player URL', () => {
  for(const id of ['<iframe>','../../secret','https://evil'])assert.equal(ui.videoURL(id,0,10),null);
  assert.equal(ui.videoURL('od4yuK67yhk',10,5),null);
  assert.equal(ui.videoURL('od4yuK67yhk',-1,5),null);
  assert.equal(ui.videoURL('od4yuK67yhk',1.2,5),null);
  assert.equal(ui.videoURL('od4yuK67yhk',350,382),'https://www.youtube-nocookie.com/embed/od4yuK67yhk?autoplay=1&playsinline=1&rel=0&start=350&end=382');
});
test('initialisation does not create a remote player; only clicking does', () => {
  let listener;let frames=0;let mounted;
  const poster={};
  const player={querySelector:()=>poster,replaceChildren:x=>{mounted=x;}};
  const slot={replaceChildren:()=>{}};
  const button={addEventListener:(_,fn)=>{listener=fn;},focus:()=>{}};
  const block={dataset:{videoId:'od4yuK67yhk',start:'401',end:'443',title:'Loro'},querySelector:s=>s==='[data-video-player]'?player:s==='[data-load-video]'?button:slot};
  const doc={querySelector:()=>null,querySelectorAll:s=>s==='[data-video-block]'?[block]:[],createElement:tag=>{if(tag==='iframe')frames++;return {addEventListener:()=>{}};}};
  ui.init(doc,null);assert.equal(frames,0);assert.equal(mounted,undefined);
  listener();assert.equal(frames,1);assert.match(mounted.src,/youtube-nocookie\.com\/embed/);assert.equal(mounted.referrerPolicy,'strict-origin-when-cross-origin');
});
test('blocked or corrupted local storage never prevents reading', () => {
  assert.deepEqual(ui.readProgress(null,'guide',4),{});
  assert.deepEqual(ui.readProgress({getItem:()=>{throw Error('blocked');}},'guide',4),{});
  assert.deepEqual(ui.readProgress({getItem:()=>'{broken'},'guide',4),{});
  assert.deepEqual(ui.readProgress({getItem:()=>'[]'},'guide',4),{});
  assert.deepEqual(ui.readProgress({getItem:()=>' {"1":true,"2":"true","9":true} '},'guide',4),{'1':true});
});
