(function () {
  "use strict";
  var script = document.currentScript;
  var source = script && script.dataset.source;
  if (["tiktok", "youtube"].indexOf(source) < 0) return;
  var target = new URL("../retos/", location.href);
  target.searchParams.set("utm_source", source);
  target.searchParams.set("utm_medium", "social");
  target.searchParams.set("utm_campaign", "leonida_retos");
  target.searchParams.set("utm_content", "perfil");
  location.replace(target.href);
})();
