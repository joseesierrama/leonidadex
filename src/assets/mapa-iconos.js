(function (root) {
  'use strict';
  var files = {
    gun:'blip_ambient_store_gun', workshop:'blip_ambient_store_custom_autos', spray:'blip_ambient_store_paynspray',
    garage:'blip_ambient_garage', house:'blip_ambient_house', gas:'blip_ambient_store_gas_station',
    police:'blip_location_police_station', clothes:'blip_ambient_store_clothes', hair:'blip_ambient_store_barber',
    tattoo:'blip_ambient_store_tattoo', food:'blip_ambient_store_food', shop:'blip_ambient_store_convenience',
    dock:'blip_location_dock', plane:'blip_ambient_hanger', bus:'blip_ambient_bus_stop',
    race:'blip_ambient_activity_racing_bike', bar:'blip_ambient_bar', club:'blip_location_nightclub',
    monument:'blip_location_monument', explore:'blip_index_exploration', pawn:'blip_ambient_store_pawn',
    hotel:'blip_location_hotel', activity:'blip_index_activities', nature:'blip_ambient_flower',
    industry:'blip_location_enterprise', money:'blip_ambient_cash', car:'blip_index_vehicles',
    collectible:'blip_ambient_collectible', showroom:'blip_ambient_store_car_showroom',
    electronics:'blip_ambient_store_electronics', carwash:'blip_ambient_store_car_wash', shoes:'blip_ambient_store_shoe',
    liquor:'blip_ambient_store_liquor', gym:'blip_ambient_activity_gym', fishing:'blip_ambient_activity_fishing',
    basketball:'blip_ambient_activity_basketball', golf:'blip_ambient_activity_golf', kayak:'blip_ambient_activity_kayak',
    airboat:'blip_ambient_airboat_tour', hunting:'blip_ambient_hunting_area', pool:'blip_ambient_activity_pool',
    stripclub:'blip_location_strip_club', train:'tren-adaptado', hospital:'hospital-adaptado'
  };
  var service = {guns:'gun',fence:'pawn',modshop:'workshop',"pay'n'spray":'spray',garage:'garage',safehouse:'house',gas:'gas',
    hospital:'hospital',police:'police',clothes:'clothes',hair:'hair',tattoos:'tattoo',food:'food',supermarket:'shop',
    marina:'dock',airport:'plane',bus:'bus',train:'train',metro:'train',metromover:'train',racetrack:'race',bar:'bar',
    nightclub:'club',landmark:'monument',curiosity:'explore',electronics:'electronics',carwash:'carwash',shoes:'shoes',liquor:'liquor',
    gym:'gym',tennis:'activity',golf:'golf',jewelry:'shop',vendor:'shop',fastfood:'food',stripclub:'stripclub'};
  var priority = ['guns','fence','modshop',"pay'n'spray",'safehouse','garage','hospital','police','airport','marina','train','metro','metromover','bus','gas','clothes','hair','tattoos','food','supermarket','racetrack','bar','nightclub','landmark','curiosity'];
  var types = {h:'hotel',c:'shop',r:'house',o:'monument',t:'car',n:'nature',i:'industry',p:'monument',x:'explore'};
  var categories = {zona:'explore',ocio:'club',tiendas:'shop',propiedades:'house',transporte:'car',naturaleza:'nature',actividades:'activity',miami:'monument',armas:'gun',dinero:'money',raros:'collectible',encuentros:'explore'};
  function tags(row) { return Array.isArray(row[8]) ? row[8] : []; }
  function isService(row) { return tags(row).some(function(t){return !!service[t];}); }
  function rowIcon(row) {
    var t=tags(row), key=priority.find(function(k){return t.indexOf(k)>-1;});
    if(!key) key=t.find(function(k){return !!service[k];});
    return key ? service[key] : (types[row[6]]||'explore');
  }
  function pinIcon(pin) {
    var name=String(pin.nombre||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
    var special=[[/sombrero|cowboy/,'collectible'],[/bandito|penumbra|lowrider/,'car'],[/tatu|tattoo/,'tattoo'],[/customs|taller/,'workshop'],[/motel|hotel/,'hotel'],[/aeropuerto/,'plane'],[/puerto|embarcadero/,'dock'],[/gimnasio/,'gym'],[/pesca/,'fishing'],[/baloncesto/,'basketball'],[/billar/,'pool'],[/golf/,'golf'],[/kayak/,'kayak'],[/hidrodeslizador/,'airboat'],[/caza|cazadores/,'hunting']];
    for(var i=0;i<special.length;i++)if(special[i][0].test(name))return special[i][1];
    return categories[pin.cat]||'explore';
  }
  function file(key) { var name=files[key]||files.explore;return name+(name.indexOf('-adaptado')>-1?'.svg':'.webp'); }
  // Declutter in screen pixels; a selected place always keeps its exact coordinates.
  function layout(rows, unit, selected, overview) {
    var size=28*Math.max(.001,unit), cells=Object.create(null), out=[];
    rows.filter(function(r){return !overview || isService(r) || r[0]===selected;}).slice().sort(function(a,b){
      return (b[0]===selected?100:0)+(isService(b)?10:0)+(b[1]?1:0)-((a[0]===selected?100:0)+(isService(a)?10:0)+(a[1]?1:0)) || a[0]-b[0];
    }).forEach(function(r){
      if(!Number.isFinite(r[3])||!Number.isFinite(r[4]))return;
      var x=Math.floor(r[3]/size),y=Math.floor(r[4]/size),near=false;
      for(var dx=-1;dx<=1;dx++)for(var dy=-1;dy<=1;dy++){
        var list=cells[(x+dx)+','+(y+dy)]||[];
        if(list.some(function(p){return Math.hypot(p[3]-r[3],p[4]-r[4])<size;}))near=true;
      }
      if(near&&r[0]!==selected)return;
      var key=x+','+y;(cells[key]||(cells[key]=[])).push(r);out.push(r);
    });return out;
  }
  var api={files:files,services:service,types:types,categories:categories,file:file,rowIcon:rowIcon,pinIcon:pinIcon,isService:isService,layout:layout};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  if(root)root.LDXMapIcons=api;
}(typeof window==='undefined'?null:window));
