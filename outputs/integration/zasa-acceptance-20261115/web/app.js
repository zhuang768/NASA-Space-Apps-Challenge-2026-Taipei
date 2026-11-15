(function () {
'use strict';
var NS = 'http://www.w3.org/2000/svg';
var RAD = Math.PI / 180;
var COLORS = ['#8ec5e8', '#e0a64f', '#cf8fd6'];
var MARS_R_KM = 3389.5;

/* Values come from outputs/research/mars_reselection_20261114/final_candidates.csv
   (native-cell means and review-area statistics). Imagery counts come from the
   MS-01 and MS-02 local-validation ODE queries. Geologic units: USGS SIM 3292. */
var SITES = [
  { id: 'MS-01', hash: 'ms-01', lat: 56.75, lon: 72.75, coords: '56.75°N, 72.75°E',
    one: 'Strong ice evidence at both depths on low, level ground.',
    text: 'Ice evidence is consistent at both depths and the terrain is low and level. Thermal inertia is the highest of the three, but only 73 of 100 thermal cells hold direct measurements.',
    elev: -3700.9, slope: 0.287, relief: 76, ti: 325.2, swim1: 0.639, swim5: 0.647, p95: 0.222,
    tesValid: 73, ewKm: 16.2,
    dust34: [0.1236, 0.1005, 0.1662, 0.0921], dust35: [0.1344, 0.0920, 0.1021, 0.0969],
    night: 173.7, day: 247.5,
    unit: 'Middle Amazonian lowland unit (mAl)',
    imagery: '4 CTX images at about 6 m per pixel, no HiRISE images, 6 SHARAD radar tracks and 207 CRISM products are listed over the review area.' },
  { id: 'MS-02', hash: 'ms-02', lat: 52.75, lon: 168.25, coords: '52.75°N, 168.25°E',
    one: 'Southernmost, with the fullest thermal coverage.',
    text: 'The southernmost of the three, with the fullest thermal coverage: 93 of 100 cells. Dust haze peaks higher here and the ground has more relief, 117 meters across the area.',
    elev: -3898.7, slope: 0.302, relief: 117, ti: 217.3, swim1: 0.693, swim5: 0.622, p95: 0.240,
    tesValid: 93, ewKm: 17.9,
    dust34: [0.1295, 0.1091, 0.1534, 0.1131], dust35: [0.1412, 0.1066, 0.0904, 0.0934],
    night: 171.3, day: 246.3,
    unit: 'Middle Amazonian lowland unit (mAl)',
    imagery: '5 CTX images at about 6 m per pixel, no HiRISE images, 3 SHARAD radar observations and 383 CRISM products are listed over the review area.' },
  { id: 'MS-03', hash: 'ms-03', lat: 57.75, lon: 242.25, coords: '57.75°N, 242.25°E',
    one: 'Flattest and clearest air, with the strongest signal near the surface.',
    text: 'The flattest and least hazy of the three, with the strongest signal in the top meter. That signal weakens between 1 and 5 meters, and thermal coverage is partial: 79 of 100 cells.',
    elev: -2548.3, slope: 0.163, relief: 76, ti: 152.8, swim1: 0.911, swim5: 0.510, p95: 0.173,
    tesValid: 79, ewKm: 15.8,
    dust34: [0.1055, 0.0839, 0.1208, 0.0847], dust35: [0.1080, 0.0791, 0.0830, 0.0807],
    night: 154.6, day: 234.9,
    unit: 'Amazonian and Hesperian volcanic unit (AHv)',
    imagery: null }
];

function $(id) { return document.getElementById(id); }
function el(name, attrs, parent) {
  var n = document.createElementNS(NS, name);
  for (var k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}
function txt(parent, x, y, s, attrs) {
  var t = el('text', Object.assign({ x: x, y: y }, attrs || {}), parent);
  t.textContent = s; return t;
}
function h(tag, cls, html) {
  var n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
}
function num(v, d) { return v.toFixed(d).replace('-', '−'); }
var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- star field ---------- */
function stars() {
  var c = $('stars'), dpr = Math.min(window.devicePixelRatio || 1, 2);
  var w = window.innerWidth, hh = window.innerHeight;
  c.width = w * dpr; c.height = hh * dpr;
  var g = c.getContext('2d'); g.scale(dpr, dpr);
  var s = 7;
  function rnd() { s = (s * 16807) % 2147483647; return s / 2147483647; }
  var n = Math.round((w * hh) / 5500);
  for (var i = 0; i < n; i++) {
    g.globalAlpha = 0.2 + rnd() * 0.6;
    g.fillStyle = rnd() < 0.15 ? '#ffd9b0' : (rnd() < 0.3 ? '#cfe3ff' : '#ffffff');
    g.beginPath(); g.arc(rnd() * w, rnd() * hh, 0.3 + Math.pow(rnd(), 3), 0, 6.2832); g.fill();
  }
}

/* ---------- globe ---------- */
var HOME = { lon: 157 * RAD, lat: 40 * RAD, zoom: 1 };
var view = { lon: HOME.lon, lat: HOME.lat, zoom: 1 };
var selected = -1;
var texW = 0, texH = 0, tex = null;
var canvas = $('globe'), ctx = canvas.getContext('2d');
var N = canvas.width, R = N / 2;
var patch = null, patchFor = -1;
var TILE = 'https://trek.nasa.gov/tiles/Mars/EQ/Mars_MGS_MOLA_ClrShade_merge_global_463m/1.0.0/default/default028mm/6/';
function loadPatch(k) {
  if (patchFor === k) return;
  patchFor = k; patch = null;
  var s = SITES[k], lon = s.lon > 180 ? s.lon - 360 : s.lon;
  var c0 = Math.floor((lon - 10 + 180) / 360 * 128), c1 = Math.floor((lon + 10 + 180) / 360 * 128);
  var r0 = Math.floor((90 - s.lat - 5.5) / 180 * 64), r1 = Math.floor((90 - s.lat + 5.5) / 180 * 64);
  var w = (c1 - c0 + 1) * 256, hh = (r1 - r0 + 1) * 256;
  var cv = document.createElement('canvas'); cv.width = w; cv.height = hh;
  var g = cv.getContext('2d'), left = 0, bad = false;
  for (var r = r0; r <= r1; r++) for (var c = c0; c <= c1; c++) (function (r, c) {
    var im = new Image(); im.crossOrigin = 'anonymous';
    im.onload = function () {
      g.drawImage(im, (c - c0) * 256, (r - r0) * 256);
      if (--left === 0 && !bad && patchFor === k) finish();
    };
    im.onerror = function () { bad = true; };
    left++; im.src = TILE + r + '/' + c + '.jpg';
  })(r, c);
  function finish() {
    try {
      var d = g.getImageData(0, 0, w, hh).data;
      patch = { data: new Uint32Array(d.buffer), w: w, h: hh, lon0: c0 / 128 * 360 - 180, lon1: (c1 + 1) / 128 * 360 - 180,
        lat0: 90 - r0 / 64 * 180, lat1: 90 - (r1 + 1) / 64 * 180 };
      $('hint').textContent = hintText();
      drawGlobe();
    } catch (e) { patch = null; }
  }
}
function hintText() {
  return 'Drag to move. Colors show elevation, blue low to red high.' + (patch ? ' Detail: 463 m per pixel.' : '');
}
var frame = ctx.createImageData(N, N);
var out = new Uint32Array(frame.data.buffer);
var L = (function () { var v = [-0.45, 0.42, 0.78], m = Math.hypot(v[0], v[1], v[2]); return [v[0] / m, v[1] / m, v[2] / m]; })();

function project(latDeg, lonDeg) {
  var p = latDeg * RAD, dl = lonDeg * RAD - view.lon;
  var x = Math.cos(p) * Math.sin(dl);
  var y = Math.cos(view.lat) * Math.sin(p) - Math.sin(view.lat) * Math.cos(p) * Math.cos(dl);
  var z = Math.sin(view.lat) * Math.sin(p) + Math.cos(view.lat) * Math.cos(p) * Math.cos(dl);
  return { x: R + x * R * view.zoom, y: R - y * R * view.zoom, z: z };
}
function pixToLatLon(px, py) {
  var z = view.zoom, nx = ((px / N) * 2 - 1) / z, ny = (1 - (py / N) * 2) / z, r2 = nx * nx + ny * ny;
  if (r2 > 1) return null;
  var nz = Math.sqrt(1 - r2), s0 = Math.sin(view.lat), c0 = Math.cos(view.lat);
  return { lat: Math.asin(nz * s0 + ny * c0) / RAD, lon: (((view.lon + Math.atan2(nx, nz * c0 - ny * s0)) / RAD) % 360 + 360) % 360 };
}

function drawGlobe() {
  if (!tex) return;
  var z = view.zoom, sinP0 = Math.sin(view.lat), cosP0 = Math.cos(view.lat);
  var pz = z > 2 ? patch : null, smooth = z > 1.4, blend = Math.max(0, Math.min(1, (z - 1) / 1.5));
  var i = 0;
  for (var y = 0; y < N; y++) {
    var ny = (1 - 2 * (y + 0.5) / N) / z;
    for (var x = 0; x < N; x++, i++) {
      var nx = (2 * (x + 0.5) / N - 1) / z, r2 = nx * nx + ny * ny;
      if (r2 > 1) { out[i] = 0; continue; }
      var nz = Math.sqrt(1 - r2);
      var phi = Math.asin(nz * sinP0 + ny * cosP0);
      var lam = view.lon + Math.atan2(nx, nz * cosP0 - ny * sinP0);
      var u = lam / 6.283185307; u -= Math.floor(u);
      var v = (0.5 - phi / Math.PI) * texH;
      var rr, gg, bb;
      if (smooth) {
        var fx = u * texW - 0.5, fy = v - 0.5;
        var x0 = Math.floor(fx), y0 = Math.floor(fy), ax = fx - x0, ay = fy - y0;
        var xa = ((x0 % texW) + texW) % texW, xb = (xa + 1) % texW;
        var ya = y0 < 0 ? 0 : (y0 >= texH ? texH - 1 : y0), yb = ya + 1 >= texH ? texH - 1 : ya + 1;
        var c00 = tex[ya * texW + xa], c10 = tex[ya * texW + xb], c01 = tex[yb * texW + xa], c11 = tex[yb * texW + xb];
        var w00 = (1 - ax) * (1 - ay), w10 = ax * (1 - ay), w01 = (1 - ax) * ay, w11 = ax * ay;
        rr = (c00 & 255) * w00 + (c10 & 255) * w10 + (c01 & 255) * w01 + (c11 & 255) * w11;
        gg = ((c00 >> 8) & 255) * w00 + ((c10 >> 8) & 255) * w10 + ((c01 >> 8) & 255) * w01 + ((c11 >> 8) & 255) * w11;
        bb = ((c00 >> 16) & 255) * w00 + ((c10 >> 16) & 255) * w10 + ((c01 >> 16) & 255) * w01 + ((c11 >> 16) & 255) * w11;
      } else {
        var ty = v | 0; if (ty < 0) ty = 0; else if (ty >= texH) ty = texH - 1;
        var c = tex[ty * texW + ((u * texW) | 0)];
        rr = c & 255; gg = (c >> 8) & 255; bb = (c >> 16) & 255;
      }
      if (pz) {
        var ld = lam / RAD; ld -= Math.floor(ld / 360) * 360; if (ld > 180) ld -= 360;
        var pd = phi / RAD;
        var wx = (ld - pz.lon0) / (pz.lon1 - pz.lon0), wy = (pz.lat0 - pd) / (pz.lat0 - pz.lat1);
        if (wx > 0 && wx < 1 && wy > 0 && wy < 1) {
          var e = Math.min(wx, 1 - wx, wy, 1 - wy) * 12; if (e > 1) e = 1;
          var qx = wx * pz.w - 0.5, qy = wy * pz.h - 0.5, qx0 = Math.floor(qx), qy0 = Math.floor(qy), bx = qx - qx0, by = qy - qy0;
          if (qx0 < 0) qx0 = 0; if (qy0 < 0) qy0 = 0; if (qx0 > pz.w - 2) qx0 = pz.w - 2; if (qy0 > pz.h - 2) qy0 = pz.h - 2;
          var q = qy0 * pz.w + qx0, p00 = pz.data[q], p10 = pz.data[q + 1], p01 = pz.data[q + pz.w], p11 = pz.data[q + pz.w + 1];
          var v00 = (1 - bx) * (1 - by), v10 = bx * (1 - by), v01 = (1 - bx) * by, v11 = bx * by;
          var pr = (p00 & 255) * v00 + (p10 & 255) * v10 + (p01 & 255) * v01 + (p11 & 255) * v11;
          var pg = ((p00 >> 8) & 255) * v00 + ((p10 >> 8) & 255) * v10 + ((p01 >> 8) & 255) * v01 + ((p11 >> 8) & 255) * v11;
          var pb = ((p00 >> 16) & 255) * v00 + ((p10 >> 16) & 255) * v10 + ((p01 >> 16) & 255) * v01 + ((p11 >> 16) & 255) * v11;
          rr += (pr - rr) * e; gg += (pg - gg) * e; bb += (pb - bb) * e;
        }
      }
      var ux = nx * z, uy = ny * z, ur2 = ux * ux + uy * uy;
      var unz = Math.sqrt(ur2 < 1 ? 1 - ur2 : 0);
      var lam2 = ux * L[0] + uy * L[1] + unz * L[2];
      var sh = (0.16 + 0.84 * Math.pow(lam2 > 0 ? lam2 : 0, 0.8)) * (0.6 + 0.4 * unz);
      sh = sh + (1 - sh) * blend;
      rr *= sh; gg *= sh; bb *= sh;
      out[i] = 0xff000000 | ((bb > 255 ? 255 : bb) << 16) | ((gg > 255 ? 255 : gg) << 8) | (rr > 255 ? 255 : rr);
    }
  }
  ctx.putImageData(frame, 0, 0);
  if (z < 1.4) {
    var gr = ctx.createRadialGradient(R, R, R * 0.965 * z, R, R, R * z);
    gr.addColorStop(0, 'rgba(224,166,79,0)'); gr.addColorStop(1, 'rgba(224,166,79,0.35)');
    ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(R, R, R * z, 0, 6.2832); ctx.fill();
  }
  drawMarkers();
  if (z > 1.5) drawScale();
}

function reticle(x, y, size, color, w) {
  var g = size * 0.45;
  ctx.lineCap = 'square';
  [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(function (s) {
    ctx.beginPath();
    ctx.moveTo(x + s[0] * size, y + s[1] * g);
    ctx.lineTo(x + s[0] * size, y + s[1] * size);
    ctx.lineTo(x + s[0] * g, y + s[1] * size);
    ctx.stroke();
  });
}

function drawMarkers() {
  ctx.font = '600 22px "Schibsted Grotesk", system-ui, sans-serif';
  ctx.textBaseline = 'middle';
  SITES.forEach(function (s, k) {
    var p = project(s.lat, s.lon);
    if (p.z < 0.25) return;
    if (p.x < -20 || p.x > N + 20 || p.y < -20 || p.y > N + 20) return;
    var on = k === selected, size = on ? 16 : 12;
    if (view.zoom > 3) {
      /* true review-area outline: 0.5 deg by 0.5 deg */
      var a = project(s.lat + 0.25, s.lon - 0.25), b = project(s.lat - 0.25, s.lon + 0.25);
      var x0 = Math.min(a.x, b.x), y0 = Math.min(a.y, b.y), ww = Math.abs(b.x - a.x), hh = Math.abs(b.y - a.y);
      ctx.strokeStyle = 'rgba(4,6,10,0.8)'; ctx.lineWidth = 5; ctx.strokeRect(x0, y0, ww, hh);
      ctx.strokeStyle = COLORS[k]; ctx.lineWidth = 2; ctx.strokeRect(x0, y0, ww, hh);
      size = Math.max(size, Math.max(ww, hh) / 2 + 8);
    }
    ctx.strokeStyle = 'rgba(4,6,10,0.85)'; ctx.lineWidth = 6; reticle(p.x, p.y, size, '#000');
    ctx.strokeStyle = COLORS[k]; ctx.lineWidth = on ? 3.5 : 2.5; reticle(p.x, p.y, size, COLORS[k]);
    if (view.zoom <= 3) { ctx.fillStyle = COLORS[k]; ctx.fillRect(p.x - 2.5, p.y - 2.5, 5, 5); }
    var lx = p.x + size + 8, flip = lx + 64 > N;
    ctx.textAlign = flip ? 'right' : 'left';
    if (flip) lx = p.x - size - 8;
    ctx.strokeStyle = 'rgba(4,6,10,0.9)'; ctx.lineWidth = 5; ctx.lineJoin = 'round';
    ctx.strokeText(s.id, lx, p.y);
    ctx.fillStyle = '#ffffff'; ctx.fillText(s.id, lx, p.y);
  });
}

function drawScale() {
  var kmPerPx = MARS_R_KM / (view.zoom * R), nice = [5, 10, 20, 50, 100, 200, 500, 1000], km = 100, i;
  for (i = 0; i < nice.length; i++) { if (nice[i] / kmPerPx >= 90) { km = nice[i]; break; } }
  var len = km / kmPerPx, x = 24, y = N - 56;
  ctx.fillStyle = 'rgba(4,6,10,0.8)'; ctx.fillRect(x - 10, y - 34, len + 20 + 60, 56);
  ctx.strokeStyle = '#ebe8e1'; ctx.lineWidth = 2; ctx.lineCap = 'butt';
  ctx.beginPath(); ctx.moveTo(x, y - 6); ctx.lineTo(x, y + 4); ctx.lineTo(x + len, y + 4); ctx.lineTo(x + len, y - 6); ctx.stroke();
  ctx.font = '500 20px "Schibsted Grotesk", system-ui, sans-serif'; ctx.fillStyle = '#ebe8e1';
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillText(km + ' km', x, y - 14);
}

var raf = 0;
function schedule() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; drawGlobe(); }); }

var tween = 0;
function flyTo(lon, lat, zoom, done) {
  cancelAnimationFrame(tween);
  if (reduce) { view.lon = lon; view.lat = lat; view.zoom = zoom; drawGlobe(); if (done) done(); return; }
  var dl = ((lon - view.lon + Math.PI * 3) % (Math.PI * 2)) - Math.PI;
  var l0 = view.lon, p0 = view.lat, z0 = view.zoom, dp = lat - view.lat, t0 = performance.now(), D = 1100;
  (function step(now) {
    var t = Math.min(1, (now - t0) / D), e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    view.lon = l0 + dl * e; view.lat = p0 + dp * e; view.zoom = z0 * Math.pow(zoom / z0, e);
    drawGlobe();
    if (t < 1) tween = requestAnimationFrame(step); else if (done) done();
  })(t0);
}

function setZoomState() {
  var zoomed = selected >= 0;
  $('stage').classList.toggle('zoomed', zoomed);
  $('zoomctl').hidden = !zoomed;
  $('hint').textContent = zoomed ? hintText() : 'Drag to turn the globe. Click a marker to zoom in.';
}

/* drag + tap */
var drag = null;
canvas.addEventListener('pointerdown', function (e) {
  cancelAnimationFrame(tween);
  canvas.setPointerCapture(e.pointerId);
  drag = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY };
});
canvas.addEventListener('pointermove', function (e) {
  var rect = canvas.getBoundingClientRect(), k = N / rect.width;
  if (drag) {
    var dx = (e.clientX - drag.x) * k / (R * view.zoom), dy = (e.clientY - drag.y) * k / (R * view.zoom);
    drag.x = e.clientX; drag.y = e.clientY;
    view.lon -= dx / Math.max(0.2, Math.cos(view.lat));
    view.lat = Math.max(-1.45, Math.min(1.45, view.lat + dy));
    schedule();
  } else if (view.zoom > 1.5) {
    var p = pixToLatLon((e.clientX - rect.left) * k, (e.clientY - rect.top) * k);
    $('readout').textContent = p ? num(p.lat, 2) + '°N  ' + num(p.lon, 2) + '°E' : '';
  }
});
canvas.addEventListener('pointerleave', function () { $('readout').textContent = ''; });
canvas.addEventListener('pointerup', function (e) {
  if (!drag) return;
  var moved = Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy);
  drag = null;
  if (moved < 6) {
    var rect = canvas.getBoundingClientRect(), k = N / rect.width;
    var px = (e.clientX - rect.left) * k, py = (e.clientY - rect.top) * k;
    var best = -1, bd = 40;
    SITES.forEach(function (s, i) {
      var p = project(s.lat, s.lon), d = Math.hypot(p.x - px, p.y - py);
      if (p.z > 0.25 && d < bd) { bd = d; best = i; }
    });
    if (best >= 0 && best !== selected) select(best);
  }
});
canvas.addEventListener('pointercancel', function () { drag = null; });

$('zin').addEventListener('click', function () { flyTo(view.lon, view.lat, Math.min(12, view.zoom * 1.6)); });
$('zout').addEventListener('click', function () { flyTo(view.lon, view.lat, Math.max(2, view.zoom / 1.6)); });

/* ---------- panel ---------- */
var tab = 'terrain', dustYear = 34;
var TABS = [['terrain', 'Terrain'], ['heat', 'Heat'], ['ice', 'Ice evidence'], ['dust', 'Dust'], ['unknowns', 'Unknown']];

function buildOverview() {
  var host = $('regions');
  SITES.forEach(function (s, i) {
    var b = h('button', 'rbtn', '<b>' + s.id + '  ' + s.coords + '</b><span>' + s.one + '</span>');
    b.type = 'button'; b.setAttribute('data-i', i);
    b.addEventListener('click', function () { select(i); });
    host.appendChild(b);
  });
}

function select(i) {
  var first = selected < 0;
  selected = i;
  var s = SITES[i];
  $('overview').hidden = true; $('detail').hidden = false;
  $('d-title').textContent = s.id;
  $('d-coords').textContent = s.coords;
  $('d-text').textContent = s.text;
  $('detail').style.setProperty('--c', COLORS[i]);
  setZoomState();
  renderTabs();
  try { history.replaceState(null, '', '#' + s.hash); } catch (e) {}
  loadPatch(i);
  flyTo(s.lon * RAD, s.lat * RAD, 5);
  $('panel').scrollTop = 0;
  if (first) $('btn-back').focus({ preventScroll: true });
}
function home() {
  selected = -1;
  $('overview').hidden = false; $('detail').hidden = true;
  setZoomState();
  try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
  flyTo(HOME.lon, HOME.lat, 1);
  $('panel').scrollTop = 0;
}

function renderTabs() {
  var t = $('tabs'); t.innerHTML = '';
  TABS.forEach(function (d) {
    var b = h('button', 'tab', d[1]);
    b.type = 'button'; b.setAttribute('role', 'tab'); b.id = 'tab-' + d[0];
    b.setAttribute('aria-selected', d[0] === tab ? 'true' : 'false');
    b.tabIndex = d[0] === tab ? 0 : -1;
    b.addEventListener('click', function () { tab = d[0]; renderTabs(); });
    b.addEventListener('keydown', function (e) {
      var idx = TABS.map(function (x) { return x[0]; }).indexOf(d[0]), n = null;
      if (e.key === 'ArrowRight') n = (idx + 1) % TABS.length;
      if (e.key === 'ArrowLeft') n = (idx + TABS.length - 1) % TABS.length;
      if (n !== null) { e.preventDefault(); tab = TABS[n][0]; renderTabs(); $('tab-' + tab).focus(); }
    });
    t.appendChild(b);
  });
  $('tabpanel').setAttribute('aria-labelledby', 'tab-' + tab);
  renderTab();
}

/* ----- charts ----- */
var METRICS = {
  elev: { title: 'Average elevation', unit: 'meters above the Mars reference surface', dom: [-4200, -2400], d: 0, hi: 'Highest ground', lo: 'Lowest ground',
    note: 'Elevation sets how much atmosphere sits above a site. It is not a hazard measure.' },
  slope: { title: 'Average slope', unit: 'degrees', dom: [0, 0.4], d: 3, hi: 'Steepest', lo: 'Flattest',
    note: 'All three are nearly level at this scale. An average cannot show hazards at landing scale.' },
  relief: { title: 'Height range', unit: 'meters from lowest to highest point in the area', dom: [0, 140], d: 0, hi: 'Most height range', lo: 'Least height range',
    note: 'A bigger range means more regional undulation.' },
  ti: { title: 'Thermal inertia', unit: 'J m⁻² K⁻¹ s⁻½, how slowly the surface changes temperature', dom: [0, 350], d: 0, hi: 'Highest', lo: 'Lowest',
    note: 'Rock, sand, ice and cementation all raise it, so a high value does not show harder ground or more ice.' },
  swim1: { title: 'Ice evidence, top meter', unit: 'consistency index from 0 to 1', dom: [0, 1], d: 2, hi: 'Strongest', lo: 'Weakest',
    note: 'How well the data fits ice. It is not an amount or a probability.' },
  swim5: { title: 'Ice evidence, 1 to 5 meters', unit: 'consistency index from 0 to 1', dom: [0, 1], d: 2, hi: 'Strongest', lo: 'Weakest',
    note: 'Deeper layers are inferred with less certainty than the top meter.' },
  p95: { title: 'Peak dust haze', unit: 'opacity on the worst 5% of days, Mars year 34', dom: [0, 0.3], d: 3, hi: 'Hazier', lo: 'Clearer',
    note: 'Dust dims the surface and shifts temperatures. Higher is hazier.' }
};

function rankSentence(key, i) {
  var m = METRICS[key], v = SITES[i][key];
  var tie = SITES.filter(function (s, j) { return j !== i && Math.abs(s[key] - v) < 1e-9; });
  if (tie.length) return '<b>Tied with ' + tie.map(function (s) { return s.id; }).join(' and ') + '</b> at ' + num(v, m.d) + '.';
  var below = SITES.filter(function (s) { return s[key] < v; }).length;
  var word = below === 2 ? m.hi : (below === 0 ? m.lo : 'In the middle');
  return '<b>' + word + '</b> of the three at ' + num(v, m.d) + '.';
}

function strip(key, active) {
  var m = METRICS[key];
  var box = h('div', 'strip');
  box.appendChild(h('h3', null, m.title));
  box.appendChild(h('p', 'unit', m.unit));
  var W = 420, H = 100, x0 = 12, x1 = W - 12, ay = 44;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': m.title + ': ' + SITES.map(function (s) { return s.id + ' ' + num(s[key], m.d); }).join(', ') });
  function X(v) { return x0 + (v - m.dom[0]) / (m.dom[1] - m.dom[0]) * (x1 - x0); }
  el('line', { x1: x0, x2: x1, y1: ay, y2: ay, stroke: '#2c3542' }, svg);
  [m.dom[0], m.dom[1]].forEach(function (v, k) {
    el('line', { x1: X(v), x2: X(v), y1: ay - 5, y2: ay + 5, stroke: '#2c3542' }, svg);
    txt(svg, X(v) + (k ? 4 : -4), H - 4, num(v, m.d === 3 ? 1 : 0), { fill: '#8b929d', 'font-size': 11, 'text-anchor': k ? 'end' : 'start' });
  });
  var order = SITES.map(function (s, i) { return i; }).sort(function (a, b) { return SITES[a][key] - SITES[b][key]; });
  var groups = {}, seen = {};
  SITES.forEach(function (s) { var k = Math.round(X(s[key])); groups[k] = (groups[k] || 0) + 1; });
  var lanes = [{ y: ay - 16, end: -1e9 }, { y: ay + 30, end: -1e9 }, { y: ay + 47, end: -1e9 }];
  /* draw others first so the active region sits on top */
  var draw = order.slice().sort(function (a, b) { return (a === active) - (b === active); });
  draw.forEach(function (i) {
    var s = SITES[i], v = s[key], x = X(v), gk = Math.round(x);
    var tie = (seen[gk] = (seen[gk] || 0) + 1) - 1, off = groups[gk] > 1 ? (tie ? 6 : -6) : 0;
    var on = i === active, r = on ? 8 : 6, op = on ? 1 : 0.55;
    var d = 'M' + x + ' ' + (ay + off - r) + 'L' + (x + r) + ' ' + (ay + off) + 'L' + x + ' ' + (ay + off + r) + 'L' + (x - r) + ' ' + (ay + off) + 'Z';
    el('path', { d: d, fill: COLORS[i], stroke: '#04060a', 'stroke-width': 2, opacity: op }, svg);
    var label = s.id + '  ' + num(v, m.d), wd = label.length * 7.4 + 12;
    var anchor = x > W - 70 ? 'end' : (x < 70 ? 'start' : 'middle');
    var left = anchor === 'end' ? x - wd : (anchor === 'start' ? x : x - wd / 2);
    var lane = lanes.filter(function (l) { return left > l.end; })[0] || lanes[2];
    lane.end = left + wd;
    txt(svg, x, lane.y, label, { fill: on ? '#ffffff' : '#9aa1ab', 'font-size': on ? 13 : 12, 'font-weight': on ? 700 : 500, 'text-anchor': anchor });
  });
  box.appendChild(svg);
  box.appendChild(h('p', 'read', rankSentence(key, active) + ' ' + m.note));
  return box;
}

function swingBox(active) {
  var box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Temperature, night to day'));
  box.appendChild(h('p', 'unit', 'median air temperature in kelvin from the Mars Climate Sounder'));
  var W = 420, H = 150, x0 = 14, x1 = W - 14, lo = 140, hi = 260;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': SITES.map(function (s) { return s.id + ' ' + num(s.night, 0) + ' kelvin at night, ' + num(s.day, 0) + ' by day'; }).join('; ') });
  function X(v) { return x0 + (v - lo) / (hi - lo) * (x1 - x0); }
  [160, 180, 200, 220, 240].forEach(function (v) {
    el('line', { x1: X(v), x2: X(v), y1: 6, y2: H - 24, stroke: '#1d2531' }, svg);
    txt(svg, X(v), H - 8, String(v), { fill: '#8b929d', 'font-size': 11, 'text-anchor': 'middle' });
  });
  SITES.forEach(function (s, k) {
    var y = 26 + k * 38, on = k === active, op = on ? 1 : 0.45;
    el('line', { x1: X(s.night), x2: X(s.day), y1: y, y2: y, stroke: COLORS[k], 'stroke-width': on ? 4 : 2.5, opacity: op }, svg);
    el('rect', { x: X(s.night) - 5, y: y - 5, width: 10, height: 10, fill: '#04060a', stroke: COLORS[k], 'stroke-width': 2, opacity: op }, svg);
    el('rect', { x: X(s.day) - 5, y: y - 5, width: 10, height: 10, fill: COLORS[k], opacity: op }, svg);
    txt(svg, X(s.night) - 12, y + 4, num(s.night, 0), { fill: on ? '#fff' : '#9aa1ab', 'font-size': 12, 'font-weight': on ? 700 : 500, 'text-anchor': 'end' });
    txt(svg, X(s.day) + 12, y + 4, num(s.day, 0), { fill: on ? '#fff' : '#9aa1ab', 'font-size': 12, 'font-weight': on ? 700 : 500 });
    txt(svg, (X(s.night) + X(s.day)) / 2, y - 10, s.id, { fill: on ? '#fff' : '#9aa1ab', 'font-size': 11, 'font-weight': 600, 'text-anchor': 'middle' });
  });
  box.appendChild(svg);
  box.appendChild(h('p', 'read', 'Hollow square: night. Filled square: day. Bins are 5 degrees wide, so they sit near each region, not on it.'));
  return box;
}

function coverageBox(active) {
  var s = SITES[active], box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Thermal coverage'));
  box.appendChild(h('p', 'unit', 'TES cells with a measured value, out of 100 in the review area'));
  var bar = h('div', 'cov'); bar.style.setProperty('--c', COLORS[active]);
  var seg = h('i'); seg.style.width = s.tesValid + '%'; bar.appendChild(seg);
  box.appendChild(bar);
  box.appendChild(h('p', 'read', '<b>' + s.tesValid + ' of 100 measured.</b> The other ' + (100 - s.tesValid) + ' are filled in by interpolation and left out of the averages.'));
  return box;
}

function dustBox(active) {
  var box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Dust haze through the Martian year'));
  box.appendChild(h('p', 'unit', 'column dust opacity, averaged over each quarter of the year; higher is hazier'));
  var seg = h('div', 'seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', 'Mars year');
  [34, 35].forEach(function (y) {
    var b = h('button', null, 'Mars year ' + y); b.type = 'button'; b.setAttribute('aria-pressed', y === dustYear ? 'true' : 'false');
    b.addEventListener('click', function () { dustYear = y; renderTab(); });
    seg.appendChild(b);
  });
  box.appendChild(seg);
  var key = 'dust' + dustYear, W = 420, H = 230, left = 36, right = 56, top = 14, bot = 34, lo = 0.06, hi = 0.18;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Dust opacity by season, Mars year ' + dustYear });
  function Y(v) { return top + (hi - v) / (hi - lo) * (H - top - bot); }
  function X(i) { return left + i * (W - left - right) / 3; }
  [0.08, 0.12, 0.16].forEach(function (v) {
    el('line', { x1: left - 4, x2: W - right + 6, y1: Y(v), y2: Y(v), stroke: '#1d2531' }, svg);
    txt(svg, left - 8, Y(v) + 4, v.toFixed(2), { fill: '#8b929d', 'font-size': 11, 'text-anchor': 'end' });
  });
  ['Spring', 'Summer', 'Autumn', 'Winter'].forEach(function (n, i) {
    txt(svg, X(i), H - 10, n, { fill: '#a3a9b3', 'font-size': 11, 'text-anchor': i === 0 ? 'start' : (i === 3 ? 'end' : 'middle') });
  });
  var order = [0, 1, 2].sort(function (a, b) { return (a === active) - (b === active); });
  var ends = [];
  order.forEach(function (k) {
    var on = k === active, vals = SITES[k][key];
    el('polyline', { points: vals.map(function (v, i) { return X(i) + ',' + Y(v); }).join(' '), fill: 'none', stroke: COLORS[k],
      'stroke-width': on ? 3.5 : 2, 'stroke-linejoin': 'round', opacity: on ? 1 : 0.4 }, svg);
    if (on) vals.forEach(function (v, i) {
      el('rect', { x: X(i) - 4, y: Y(v) - 4, width: 8, height: 8, fill: COLORS[k], stroke: '#04060a', 'stroke-width': 1.5 }, svg);
      txt(svg, X(i), Y(v) - 11, v.toFixed(3), { fill: '#fff', 'font-size': 11, 'font-weight': 600, 'text-anchor': i === 3 ? 'end' : 'middle' });
    });
    ends.push({ k: k, y: Y(vals[3]) });
  });
  ends.sort(function (a, b) { return a.y - b.y; });
  for (var q = 1; q < ends.length; q++) if (ends[q].y - ends[q - 1].y < 14) ends[q].y = ends[q - 1].y + 14;
  ends.forEach(function (e) { txt(svg, W - right + 12, e.y + 4, SITES[e.k].id, { fill: e.k === active ? COLORS[e.k] : '#8b929d', 'font-size': 12, 'font-weight': 600 }); });
  box.appendChild(svg);
  return box;
}

function unknowns(i) {
  var s = SITES[i], d = h('dl', 'facts');
  function add(t, body) { d.appendChild(h('dt', null, t)); d.appendChild(h('dd', null, body)); }
  add('Map unit', 'The USGS global geologic map, drawn at 1:20 million, places this region in the ' + s.unit + '. That is a regional label, not a description of the rock or soil underfoot.');
  add('Imagery', s.imagery || 'Image counts for this region are not summarized on this page.');
  add('Not known', 'Whether ice is there, how deep, and how much. What the ground is made of, what covers it, and how rough it is at landing scale.');
  add('What would settle it', 'Projected high-resolution images, radar echoes, spectra, and an independent measurement on the ground. Earth sites such as University Valley and Haughton crater show how those methods work. They are not matches for this region.');
  return d;
}

function renderTab() {
  var p = $('tabpanel'); p.innerHTML = '';
  var i = selected; if (i < 0) return;
  p.style.setProperty('--c', COLORS[i]);
  $('tabs').style.setProperty('--c', COLORS[i]);
  if (tab === 'terrain') { p.appendChild(strip('slope', i)); p.appendChild(strip('relief', i)); p.appendChild(strip('elev', i)); }
  else if (tab === 'heat') { p.appendChild(strip('ti', i)); p.appendChild(coverageBox(i)); p.appendChild(swingBox(i)); }
  else if (tab === 'ice') { p.appendChild(strip('swim1', i)); p.appendChild(strip('swim5', i)); }
  else if (tab === 'dust') { p.appendChild(dustBox(i)); p.appendChild(strip('p95', i)); }
  else p.appendChild(unknowns(i));
}

/* ---------- wiring ---------- */
$('btn-back').addEventListener('click', home);
$('btn-overview').addEventListener('click', home);
$('btn-home').addEventListener('click', home);
var dlg = $('sources');
$('btn-sources').addEventListener('click', function () { if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); });
$('src-close').addEventListener('click', function () { if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); });
dlg.addEventListener('click', function (e) { if (e.target === dlg && dlg.close) dlg.close(); });

function fromHash() {
  var k = SITES.map(function (s) { return s.hash; }).indexOf((location.hash || '').slice(1));
  if (k >= 0 && k !== selected) select(k);
  else if (k < 0 && selected >= 0 && !location.hash) home();
}
window.addEventListener('hashchange', fromHash);

var img = new Image();
img.onload = function () {
  var o = document.createElement('canvas');
  o.width = texW = img.naturalWidth; o.height = texH = img.naturalHeight;
  var g = o.getContext('2d'); g.drawImage(img, 0, 0);
  tex = new Uint32Array(g.getImageData(0, 0, texW, texH).data.buffer);
  drawGlobe();
};
img.src = 'mola.jpg';

buildOverview();
setZoomState();
stars();
var rt = 0;
window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(stars, 150); });
fromHash();
})();
