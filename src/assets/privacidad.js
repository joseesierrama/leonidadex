/* Medición opcional. No se carga Google antes del consentimiento explícito. */
(function () {
  "use strict";
  var script = document.currentScript;
  var id = script && script.dataset.ga4;
  if (!/^G-[A-Z0-9]{6,}$/.test(id || "")) return;
  var key = "ld:consent:v1", lifetime = 180 * 86400000, loaded = false, opener;
  var dialog = document.getElementById("privacyDialog");
  if (!dialog || typeof dialog.showModal !== "function") return;
  function read() {
    try {
      var choice = JSON.parse(localStorage.getItem(key));
      return choice && typeof choice.analytics === "boolean" && Number.isFinite(choice.at) &&
        choice.at <= Date.now() && Date.now() - choice.at < lifetime ? choice : null;
    } catch (e) { return null; }
  }
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag("consent", "default", { analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
  function start() {
    if (loaded) return;
    loaded = true;
    gtag("consent", "update", { analytics_storage: "granted" });
    gtag("js", new Date());
    gtag("config", id, { allow_google_signals: false, allow_ad_personalization_signals: false, cookie_expires: 15552000 });
    var tag = document.createElement("script");
    tag.async = true;
    tag.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(tag);
  }
  function clearAnalyticsCookies() {
    var hostname = location.hostname;
    document.cookie.split(";").forEach(function (cookie) {
      var name = cookie.split("=")[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      document.cookie = name + "=; Max-Age=0; Path=/; SameSite=Lax";
      var parts = hostname.split(".");
      while (parts.length > 1) {
        document.cookie = name + "=; Max-Age=0; Path=/; Domain=" + parts.join(".") + "; SameSite=Lax";
        parts.shift();
      }
    });
  }
  function choose(accepted) {
    try { localStorage.setItem(key, JSON.stringify({ analytics: accepted, at: Date.now() })); } catch (e) {}
    gtag("consent", "update", { analytics_storage: accepted ? "granted" : "denied" });
    if (accepted) start();
    else clearAnalyticsCookies();
    dialog.close();
    if (opener) opener.focus();
    if (!accepted && loaded) location.reload();
  }
  document.querySelectorAll("[data-privacy-open]").forEach(function (button) {
    button.hidden = false;
    button.addEventListener("click", function () { opener = button; dialog.showModal(); });
  });
  document.getElementById("privacyAccept").addEventListener("click", function () { choose(true); });
  document.getElementById("privacyReject").addEventListener("click", function () { choose(false); });
  document.getElementById("privacyClose").addEventListener("click", function () { dialog.close(); });
  var choice = read();
  if (choice && choice.analytics) start();
  else if (!choice) dialog.showModal();
})();
