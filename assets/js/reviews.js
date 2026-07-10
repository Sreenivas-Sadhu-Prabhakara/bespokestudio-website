/* BespokeStudio - live Google reviews (Maps JS Place class).
   Self-contained, no third-party widget. Renders ONLY live data.
   On any failure / missing key -> reveals the static "Read on Google" block. */
(function () {
  "use strict";

  var cfg = window.BSPK_REVIEWS || null;
  var mount = document.getElementById("gr-live");
  var fallback = document.getElementById("gr-fallback");

  function showFallback() {
    if (fallback) fallback.hidden = false;
    if (mount) mount.hidden = true;
  }
  function showLive() {
    if (fallback) fallback.hidden = true;
    if (mount) mount.hidden = false;
  }

  // Hard preconditions. No key or no place id -> static link only.
  if (!cfg || !cfg.placeId || !cfg.hasKey || !mount) { showFallback(); return; }

  var STAR = "★", DIM = "☆";
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function stars(n) {
    n = Math.round(Number(n) || 0);
    if (n < 0) n = 0; if (n > 5) n = 5;
    var out = ""; for (var i = 0; i < n; i++) out += STAR;
    for (var j = n; j < 5; j++) out += DIM;
    return out;
  }

  function render(place) {
    var rating = (typeof place.rating === "number") ? place.rating : null;
    var count = (typeof place.userRatingCount === "number") ? place.userRatingCount : null;
    var reviews = Array.isArray(place.reviews) ? place.reviews.slice(0, 5) : [];
    var mapsUri = place.googleMapsURI || cfg.profileUrl || "#";

    // Never render an empty/fabricated state: require at least the aggregate.
    if (rating == null || count == null) { showFallback(); return; }

    var head =
      '<div class="gr-head">' +
        '<div class="gr-score">' +
          '<span class="gr-rating">' + esc(rating.toFixed(1)) + '</span>' +
          '<span class="gr-stars" aria-hidden="true">' + stars(rating) + '</span>' +
          '<span class="gr-count">' + esc(String(count)) + ' Google reviews</span>' +
        '</div>' +
        '<a class="gr-badge" href="' + esc(mapsUri) + '" target="_blank" rel="noopener noreferrer">' +
          'Reviews from <strong>Google&nbsp;Maps</strong>' +
        '</a>' +
      '</div>';

    var cards = "";
    for (var i = 0; i < reviews.length; i++) {
      var r = reviews[i] || {};
      var a = r.authorAttribution || {};
      var name = a.displayName || "Google user";
      var uri = a.uri || mapsUri;
      var photo = a.photoURI || "";
      var when = r.relativePublishTimeDescription || "";
      var text = (r.text || "").trim();
      if (!text) continue; // some reviews are rating-only; skip empties

      // Mandatory per-review author attribution: avatar + name + profile link.
      var avatar = photo
        ? '<img class="gr-av" src="' + esc(photo) + '" width="40" height="40" alt="" referrerpolicy="no-referrer" loading="lazy">'
        : '<span class="gr-av gr-av--ph" aria-hidden="true">' + esc(name.charAt(0).toUpperCase()) + '</span>';

      cards +=
        '<figure class="review gr-card">' +
          '<div class="gr-card__top">' +
            '<a class="gr-author" href="' + esc(uri) + '" target="_blank" rel="noopener noreferrer">' +
              avatar + '<span class="gr-name">' + esc(name) + '</span>' +
            '</a>' +
            '<span class="review__stars" aria-label="' + esc(r.rating) + ' out of 5">' + stars(r.rating) + '</span>' +
          '</div>' +
          '<blockquote class="review__q">' + esc(text) + '</blockquote>' +
          '<figcaption class="review__meta">' +
            (when ? esc(when) + ' &middot; ' : '') +
            '<a href="' + esc(mapsUri) + '" target="_blank" rel="noopener noreferrer">View on Google Maps</a>' +
          '</figcaption>' +
        '</figure>';
    }

    if (!cards) { showFallback(); return; } // no usable review text -> degrade

    mount.innerHTML = head + '<div class="reviews gr-grid">' + cards + '</div>';
    showLive();
  }

  // Bootstrap: load the Maps JS API on demand, then fetch fields once.
  async function run() {
    try {
      if (!(window.google && google.maps && google.maps.importLibrary)) {
        showFallback(); return;
      }
      var lib = await google.maps.importLibrary("places");
      var Place = lib.Place;
      var place = new Place({ id: cfg.placeId });
      await place.fetchFields({
        fields: ["rating", "userRatingCount", "reviews", "googleMapsURI"]
      });
      render(place);
    } catch (e) {
      showFallback();
    }
  }

  run();
})();
