/* BespokeStudio — lean progressive enhancement.
   No dependencies. Everything degrades gracefully without JS. */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- year stamp ---- */
  var yr = document.querySelector("[data-year]");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- mobile drawer ---- */
  var burger = document.querySelector(".burger");
  var drawer = document.querySelector(".drawer");
  var scrim = document.querySelector(".scrim");
  var closeBtn = document.querySelector(".drawer__close");

  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("is-open", open);
    if (scrim) scrim.classList.toggle("is-open", open);
    if (burger) burger.classList.toggle("is-open", open);
    if (burger) burger.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (burger) burger.addEventListener("click", function () {
    setDrawer(!drawer.classList.contains("is-open"));
  });
  if (scrim) scrim.addEventListener("click", function () { setDrawer(false); });
  if (closeBtn) closeBtn.addEventListener("click", function () { setDrawer(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setDrawer(false);
  });
  if (drawer) {
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setDrawer(false); });
    });
  }

  /* ---- header stuck shadow ---- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---- scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---- analytics events (GA4-ready) ----
     Fires on any element with [data-evt]. Reads params from data-* attributes.
     Works whether or not gtag is present (buffers to dataLayer either way). */
  window.dataLayer = window.dataLayer || [];
  function track(name, params) {
    try {
      if (typeof window.gtag === "function") {
        window.gtag("event", name, params || {});
      } else {
        window.dataLayer.push(Object.assign({ event: name }, params || {}));
      }
    } catch (e) { /* never break the click */ }
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-evt]");
    if (!el) return;
    var name = el.getAttribute("data-evt");
    var params = {};
    for (var i = 0; i < el.attributes.length; i++) {
      var at = el.attributes[i];
      if (at.name.indexOf("data-p-") === 0) {
        params[at.name.slice(7).replace(/-/g, "_")] = at.value;
      }
    }
    params.page = document.body.getAttribute("data-page") || location.pathname;
    track(name, params);
  });

  /* service_page_view — fire once on service/guide pages */
  var svc = document.body.getAttribute("data-service");
  if (svc) track("service_page_view", { service_name: svc });

  /* ---- lazy map: load the iframe only when the map scrolls into view ---- */
  var mapHost = document.querySelector("[data-map]");
  if (mapHost) {
    var load = function () {
      if (mapHost.dataset.loaded) return;
      mapHost.dataset.loaded = "1";
      var ifr = document.createElement("iframe");
      ifr.src = mapHost.getAttribute("data-map");
      ifr.title = "Map to BespokeStudio, Basaveshwaranagar";
      ifr.loading = "lazy";
      ifr.referrerPolicy = "no-referrer-when-downgrade";
      ifr.allowFullscreen = true;
      mapHost.appendChild(ifr);
    };
    if ("IntersectionObserver" in window) {
      var mio = new IntersectionObserver(function (ents) {
        ents.forEach(function (en) { if (en.isIntersecting) { load(); mio.disconnect(); } });
      }, { rootMargin: "200px" });
      mio.observe(mapHost);
    } else { load(); }
  }
})();
