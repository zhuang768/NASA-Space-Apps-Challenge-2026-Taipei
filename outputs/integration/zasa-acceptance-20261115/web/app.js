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
    one: 'Positive SWIM consistency in both depth zones on low regional slopes.',
    text: 'Both SWIM depth-zone consistency means are positive and regional slopes are low. Thermal inertia is the highest of the three; 73 of 100 native TES-derived cells remain after excluding infill.',
    elev: -3700.9, slope: 0.287, relief: 76, ti: 325.2, swim1: 0.639, swim5: 0.647, p95: 0.222,
    tesValid: 73, ewKm: 16.2,
    dust34: [0.1236, 0.1005, 0.1662, 0.0921], dust35: [0.1344, 0.0920, 0.1021, 0.0969],
    night: 173.7, day: 247.5,
    unit: 'Middle Amazonian lowland unit (mAl)',
    imagery: '4 CTX images at about 6 m per pixel, no HiRISE images, 6 SHARAD radar tracks and 207 CRISM products are listed over the review area.' },
  { id: 'MS-02', hash: 'ms-02', lat: 52.75, lon: 168.25, coords: '52.75°N, 168.25°E',
    one: 'Southernmost, with the fullest thermal coverage.',
    text: 'The southernmost of the three, with the fullest thermal coverage: 93 of 100 cells. Its MY34 reconstructed dust 95th percentile is higher and the regional relief is 117 meters.',
    elev: -3898.7, slope: 0.302, relief: 117, ti: 217.3, swim1: 0.693, swim5: 0.622, p95: 0.240,
    tesValid: 93, ewKm: 17.9,
    dust34: [0.1295, 0.1091, 0.1534, 0.1131], dust35: [0.1412, 0.1066, 0.0904, 0.0934],
    night: 171.3, day: 246.3,
    unit: 'Middle Amazonian lowland unit (mAl)',
    imagery: '5 CTX images at about 6 m per pixel, no HiRISE images, 3 SHARAD radar observations and 383 CRISM products are listed over the review area.' },
  { id: 'MS-03', hash: 'ms-03', lat: 57.75, lon: 242.25, coords: '57.75°N, 242.25°E',
    one: 'Lowest regional slope and highest shallow SWIM consistency of the three.',
    text: 'This region has the lowest mean slope and MY34 reconstructed dust 95th percentile of the three. Shallow SWIM consistency exceeds the deeper-zone mean; the layers share evidence. TES support is partial: 79 of 100 non-infill cells.',
    elev: -2548.3, slope: 0.163, relief: 76, ti: 152.8, swim1: 0.911, swim5: 0.510, p95: 0.173,
    tesValid: 79, ewKm: 15.8,
    dust34: [0.1055, 0.0839, 0.1208, 0.0847], dust35: [0.1080, 0.0791, 0.0830, 0.0807],
    night: 154.6, day: 234.9,
    unit: 'Amazonian and Hesperian volcanic unit (AHv)',
    imagery: 'Retained CTX and MOC fixed windows did not yield accepted adjacent closed polygon contours. Local morphology remains unknown; this does not establish absence.' }
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
var selected = -1, mono = false;
var texW = 0, texH = 0, tex = null;
var canvas = $('globe'), ctx = canvas.getContext('2d');
var N = canvas.width, R = N / 2;
var patch = null, patchFor = -1;
var patchState = 'idle';
var TILE = 'https://trek.nasa.gov/tiles/Mars/EQ/Mars_MGS_MOLA_ClrShade_merge_global_463m/1.0.0/default/default028mm/6/';
function loadPatch(k) {
  if (patchFor === k) return;
  patchFor = k; patch = null; patchState = 'loading';
  if (tex) $('map-message').hidden = true;
  $('hint').textContent = hintText();
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
    im.onerror = function () {
      bad = true;
      if (patchFor === k) {
        patchState = 'unavailable';
        mapMessage('Detail tiles are unavailable. The base map and research data remain available.');
        $('hint').textContent = hintText();
      }
    };
    left++; im.src = TILE + r + '/' + c + '.jpg';
  })(r, c);
  function finish() {
    try {
      var d = g.getImageData(0, 0, w, hh).data;
      patch = { data: new Uint32Array(d.buffer), w: w, h: hh, lon0: c0 / 128 * 360 - 180, lon1: (c1 + 1) / 128 * 360 - 180,
        lat0: 90 - r0 / 64 * 180, lat1: 90 - (r1 + 1) / 64 * 180, gain: [1, 1, 1] };
      patchState = 'ready';
      matchColor(patch);
      $('hint').textContent = hintText();
      drawGlobe();
    } catch (e) { patch = null; patchState = 'unavailable'; mapMessage('Detail tiles could not be read. The base map remains available.'); }
  }
}
function matchColor(p) {
  if (!tex) return;
  var bs = [0, 0, 0], ps = [0, 0, 0], n = 0;
  for (var a = 0; a < 24; a++) for (var b = 0; b < 24; b++) {
    var fx = (a + 0.5) / 24, fy = (b + 0.5) / 24;
    var lon = p.lon0 + fx * (p.lon1 - p.lon0), lat = p.lat0 + fy * (p.lat1 - p.lat0);
    var u = ((lon + 360) % 360) / 360, v = (90 - lat) / 180;
    var c = tex[Math.min(texH - 1, (v * texH) | 0) * texW + Math.min(texW - 1, (u * texW) | 0)];
    var d = p.data[Math.min(p.h - 1, (fy * p.h) | 0) * p.w + Math.min(p.w - 1, (fx * p.w) | 0)];
    bs[0] += c & 255; bs[1] += (c >> 8) & 255; bs[2] += (c >> 16) & 255;
    ps[0] += d & 255; ps[1] += (d >> 8) & 255; ps[2] += (d >> 16) & 255; n++;
  }
  for (var k = 0; k < 3; k++) p.gain[k] = ps[k] > 0 ? Math.max(0.6, Math.min(1.8, bs[k] / ps[k])) : 1;
}
function hintText() {
  return (mono ? 'Grayscale MOLA display.' : 'MOLA elevation: blue low, red high.') + (patch ? ' Detail map: 463 m/pixel.' : (patchState === 'loading' ? ' Loading detail map…' : ' Global base map.'));
}
function mapMessage(message) {
  $('map-message-text').textContent = message;
  $('map-message').hidden = false;
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
          var e = Math.min(wx, 1 - wx, wy, 1 - wy) * 5; if (e > 1) e = 1;
          var qx = wx * pz.w - 0.5, qy = wy * pz.h - 0.5, qx0 = Math.floor(qx), qy0 = Math.floor(qy), bx = qx - qx0, by = qy - qy0;
          if (qx0 < 0) qx0 = 0; if (qy0 < 0) qy0 = 0; if (qx0 > pz.w - 2) qx0 = pz.w - 2; if (qy0 > pz.h - 2) qy0 = pz.h - 2;
          var q = qy0 * pz.w + qx0, p00 = pz.data[q], p10 = pz.data[q + 1], p01 = pz.data[q + pz.w], p11 = pz.data[q + pz.w + 1];
          var v00 = (1 - bx) * (1 - by), v10 = bx * (1 - by), v01 = (1 - bx) * by, v11 = bx * by;
          var pr = (p00 & 255) * v00 + (p10 & 255) * v10 + (p01 & 255) * v01 + (p11 & 255) * v11;
          var pg = ((p00 >> 8) & 255) * v00 + ((p10 >> 8) & 255) * v10 + ((p01 >> 8) & 255) * v01 + ((p11 >> 8) & 255) * v11;
          var pb = ((p00 >> 16) & 255) * v00 + ((p10 >> 16) & 255) * v10 + ((p01 >> 16) & 255) * v01 + ((p11 >> 16) & 255) * v11;
          pr *= pz.gain[0]; pg *= pz.gain[1]; pb *= pz.gain[2];
          rr += (pr - rr) * e; gg += (pg - gg) * e; bb += (pb - bb) * e;
        }
      }
      if (mono) { var lm = (rr * 0.3 + gg * 0.59 + bb * 0.11) * 1.25; rr = gg = bb = lm; }
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

$('zmono').addEventListener('click', function () {
  mono = !mono; this.setAttribute('aria-pressed', mono ? 'true' : 'false');
  $('hint').textContent = hintText(); drawGlobe();
});
$('zin').addEventListener('click', function () { flyTo(view.lon, view.lat, Math.min(12, view.zoom * 1.6)); });
$('zout').addEventListener('click', function () { flyTo(view.lon, view.lat, Math.max(2, view.zoom / 1.6)); });

/* ---------- panel ---------- */
var tab = 'terrain', dustYear = 34;
var TABS = [['terrain', 'Terrain'], ['heat', 'Temperature'], ['ice', 'Water / ice'], ['dust', 'Air / dust'], ['earth', 'Earth references'], ['unknowns', 'Limits & next steps']];
var REPO = 'https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/25b0744ac3d2230803505e1679109c2c35b6204d/';
var RESEARCH = 'outputs/research/mars_reselection_20261114/';
var TAB_CONTEXT = {
  terrain: {
    takeaway: 'Regional terrain describes the wider setting. Landing-scale obstacles remain unresolved.',
    support: 'MOLA · 0.5° review cells',
    method: 'Native MOLA statistics inside each nominal cell. Slope uses an approximately 3.7 km baseline; relief is the cell’s elevation range. Map display detail does not improve these analysis scales.',
    provider: ['MOLA documentation', 'https://marsoweb.nas.nasa.gov/globalData/MOLA_notes.html']
  },
  heat: {
    takeaway: 'Material response and surface temperature are different measurements. Neither confirms ice on its own.',
    support: 'TES + MCS · different spatial supports',
    method: 'TES native-cell means exclude infill, with valid counts shown below. MCS uses nearest 5° bins, MY29–36, at nominal 03:00 / 15:00 LTST with provider model-time adjustments. Per-bin QA, counts and uncertainties were not supplied.',
    provider: ['TES product documentation', 'https://pds-geosciences.wustl.edu/missions/mgs/tes-timap.html'],
    extra: ['MCS derivative source', 'https://doi.org/10.5281/zenodo.17947556']
  },
  ice: {
    takeaway: 'SWIM measures consistency with ice. Local ice presence, depth and amount remain unconfirmed.',
    support: 'SWIM 2.0 · shared evidence across depth zones',
    method: 'The signed −1 to +1 index combines evidence that can be consistent with ice. These native-cell means are not probabilities or amounts. Both depth-zone products share inputs, so they are not independent confirmations.',
    provider: ['SWIM 2.0 products', 'https://swim.psi.edu/SWIM2Products.php']
  },
  dust: {
    takeaway: 'These reconstructed regional columns describe atmospheric context. They do not measure local visibility or deposited dust.',
    support: 'MY34 / MY35 · nearest 3° dust cell',
    method: 'Montabone reconstructed pressure-normalized column opacity. Each Mars year contains 669 reconstructed sols. Seasonal means use 90° Ls intervals; the percentile below uses MY34. Repeated coarse cells are not independent local measurements.',
    provider: ['Published dust reconstruction', 'https://doi.org/10.1029/2019JE006111']
  },
  earth: {
    takeaway: 'Earth observations provide method references. No matched Mars condition or new terrestrial analogue has been validated.',
    support: 'Published Earth records · separate footprints',
    method: 'Matrix states describe evidence at the Earth reference only. University Valley ground-response summaries, monthly air observations and Mars surface products have different periods, instruments and supports. They must not be treated as a paired experiment.',
    provider: ['Earth evidence ledger', REPO + 'docs/earth_submission_status.csv']
  },
  unknowns: {
    takeaway: 'Regional screening narrows questions. Independent local evidence is still needed to test them.',
    support: 'Research targets · no local ice confirmation',
    method: 'Catalogue intersection, valid pixels, inspected area and accepted measurements are different stages. The retained MS-03 fixed windows did not yield accepted closed contours; this is not proof that polygons are absent.',
    provider: ['MS-03 retained-image audit', REPO + 'outputs/research/MS-03/repository_validation_20261115/README.md']
  }
};

function buildOverview() {
  var host = $('regions');
  SITES.forEach(function (s, i) {
    var b = h('button', 'rbtn', '<span class="region-line"><b>' + s.id + '</b><span class="region-coords">' + s.coords + '</span><svg aria-hidden="true" viewBox="0 0 20 20"><path d="M4 10h12m-5-5 5 5-5 5"/></svg></span><span class="region-description">' + s.one + '</span>');
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
  $('region-select').value = String(i);
  $('study-scope').textContent = '0.5° review cell · ' + num(s.lat - 0.25, 2) + '–' + num(s.lat + 0.25, 2) + '°N · ' + num(s.lon - 0.25, 2) + '–' + num(s.lon + 0.25, 2) + '°E';
  $('detail').style.setProperty('--c', COLORS[i]);
  setZoomState();
  renderTabs();
  try { history.replaceState(null, '', '#' + s.hash); } catch (e) {}
  loadPatch(i);
  flyTo(s.lon * RAD, s.lat * RAD, 5);
  $('panel').scrollTop = 0;
  if (window.matchMedia('(max-width: 60rem)').matches && !first) $('detail').scrollIntoView({ block: 'start' });
  if (first) $('btn-back').focus({ preventScroll: true });
}
function home() {
  selected = -1;
  $('overview').hidden = false; $('detail').hidden = true;
  if (tex) $('map-message').hidden = true;
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
    b.setAttribute('aria-controls', 'tabpanel');
    b.setAttribute('aria-selected', d[0] === tab ? 'true' : 'false');
    b.tabIndex = d[0] === tab ? 0 : -1;
    b.addEventListener('click', function () { tab = d[0]; renderTabs(); $('tab-' + tab).focus({ preventScroll: true }); });
    b.addEventListener('keydown', function (e) {
      var idx = TABS.map(function (x) { return x[0]; }).indexOf(d[0]), n = null;
      if (e.key === 'ArrowRight') n = (idx + 1) % TABS.length;
      if (e.key === 'ArrowLeft') n = (idx + TABS.length - 1) % TABS.length;
      if (e.key === 'Home') n = 0;
      if (e.key === 'End') n = TABS.length - 1;
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
    note: 'Thermal inertia depends on material, particle size and cementation; it does not uniquely identify hardness or ice.' },
  swim1: { title: 'SWIM consistency, 0 to 1 m', unit: 'signed consistency index from −1 to +1', dom: [-1, 1], d: 2, hi: 'Highest consistency', lo: 'Lowest consistency',
    note: 'Composite consistency with ice: −1 to +1. It is not ice amount, probability or an independent detection.' },
  swim5: { title: 'SWIM consistency, 1 to 5 m', unit: 'signed consistency index from −1 to +1', dom: [-1, 1], d: 2, hi: 'Highest consistency', lo: 'Lowest consistency',
    note: 'The two depth-zone maps share evidence; neither establishes local ice depth or an independent confirmation.' },
  p95: { title: 'Reconstructed dust, 95th percentile', unit: 'dimensionless column opacity, Mars year 34', dom: [0, 0.3], d: 3, hi: 'Higher percentile', lo: 'Lower percentile',
    note: '95th percentile across 669 reconstructed sols; not a measured peak, local visibility or surface dust deposition.' }
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
  var m = METRICS[key], box = h('div', 'strip');
  box.appendChild(h('h3', null, m.title));
  box.appendChild(h('p', 'unit', m.unit));
  var W = 420, H = 136, x0 = 82, x1 = 318;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': m.title + ': ' + SITES.map(function (s) { return s.id + ' ' + num(s[key], m.d); }).join(', ') });
  function X(v) { return x0 + (v - m.dom[0]) / (m.dom[1] - m.dom[0]) * (x1 - x0); }
  if (m.dom[0] < 0 && m.dom[1] > 0) {
    el('line', { x1: X(0), x2: X(0), y1: 10, y2: 106, stroke: '#46515f', 'stroke-dasharray': '3 4' }, svg);
    txt(svg, X(0), 129, '0', { fill: '#a3a9b3', 'font-size': 13, 'text-anchor': 'middle' });
  }
  SITES.forEach(function (s, i) {
    var y = 24 + i * 34, on = i === active, x = X(s[key]);
    el('line', { x1: x0, x2: x1, y1: y, y2: y, stroke: '#2c3542' }, svg);
    txt(svg, 0, y + 5, s.id, { fill: on ? COLORS[i] : '#a3a9b3', 'font-size': 14, 'font-weight': on ? 600 : 400 });
    var r = on ? 7 : 5;
    el('path', { d: 'M' + x + ' ' + (y-r) + 'L' + (x+r) + ' ' + y + 'L' + x + ' ' + (y+r) + 'L' + (x-r) + ' ' + y + 'Z',
      fill: COLORS[i], opacity: on ? 1 : 0.65, stroke: '#04060a', 'stroke-width': 1.5 }, svg);
    txt(svg, W - 2, y + 5, num(s[key], m.d), { fill: on ? '#fff' : '#a3a9b3', 'font-size': 15, 'font-weight': on ? 600 : 400, 'text-anchor': 'end' });
  });
  [m.dom[0], m.dom[1]].forEach(function (v, k) {
    txt(svg, X(v), 129, num(v, m.d === 3 ? 1 : 0), { fill: '#a3a9b3', 'font-size': 13, 'text-anchor': k ? 'end' : 'start' });
  });
  box.appendChild(svg);
  box.appendChild(h('p', 'read', rankSentence(key, active) + ' ' + m.note));
  return box;
}

function swingBox(active) {
  var box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Surface temperature context'));
  box.appendChild(h('p', 'unit', 'model-time-adjusted surface temperature (K); separate populated-bin medians'));
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
  box.appendChild(h('p', 'read', 'Hollow: nominal 03:00 LTST. Filled: nominal 15:00 LTST. These separate medians use populated 5-degree bins in MY29–36; their difference is not a paired daily amplitude or local weather record.'));
  return box;
}

function coverageBox(active) {
  var s = SITES[active], box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Thermal coverage'));
  box.appendChild(h('p', 'unit', 'Non-infill TES-derived native cells, out of 100 in the review area'));
  var bar = h('div', 'cov'); bar.style.setProperty('--c', COLORS[active]);
  var seg = h('i'); seg.style.width = s.tesValid + '%'; bar.appendChild(seg);
  box.appendChild(bar);
  box.appendChild(h('p', 'read', '<b>' + s.tesValid + ' of 100 non-infill cells.</b> The other ' + (100 - s.tesValid) + ' are filled in by interpolation and left out of the averages.'));
  return box;
}

function dustBox(active) {
  var box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Reconstructed dust by season'));
  box.appendChild(h('p', 'unit', 'regional column dust opacity; mean within each 90-degree Ls interval'));
  var seg = h('div', 'seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', 'Mars year');
  [34, 35].forEach(function (y) {
    var b = h('button', null, 'Mars year ' + y); b.type = 'button'; b.setAttribute('aria-pressed', y === dustYear ? 'true' : 'false');
    b.addEventListener('click', function () { dustYear = y; renderTab(); $('tabpanel').querySelector('.seg button[aria-pressed="true"]').focus({ preventScroll: true }); });
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
  add('Image records and inspection', s.imagery || 'Image counts for this region are not summarized on this page.');
  add('Not known', 'Whether ice is there, how deep, and how much. What the ground is made of, what covers it, and how rough it is at landing scale.');
  add('Evidence needed next', 'Check valid, registered local image pixels and independent radar, spectral or ground evidence. Each constrains a different question; no single product establishes ice presence, depth and amount. Earth sites provide method references, with separate footprints and limits.');
  return d;
}

/* ---------- Earth check ----------
   Earth values come from outputs/research/MS-01..03 (Earth evidence tables) and
   MS-03/completion_20261115/earth_atmosphere_monthly.csv (University Valley, Jan-Nov 2010). */
var UV_MONTHLY_C = [-12.12, -18.08, -22.97, -27.02, -29.92, -31.36, -33.91, -31.35, -30.27, -23.98, -18.18];
var UV_DAMP = [['Surface', 8.38], ['10 cm down', 3.89], ['Ice, 42 cm', 0.21], ['In the ice, 49 cm', 0.13]];
var PTS = {
  uv: { name: 'University Valley, Antarctica', where: '77.86°S, 160.71°E, 1,677 m', url: 'https://doi.org/10.1017/S0954102022000025',
    yes: 'Published University Valley stations report shallow ice-cemented interfaces under dry cover. This location anchors W; valley-wide interface ranges and W temperature summaries have separate spatial and temporal support.',
    no: 'Station values, not a valley map. No slope or thermal inertia was derived.' },
  beacon: { name: 'Beacon Valley, Antarctica', where: '77.82°S, 160.65°E', url: 'https://doi.org/10.1029/2017JF004535',
    yes: 'About 0.3 m of dry soil over blocky ice, with polygons 10 to 20 m across. A published model gives about 0.11 mm of ice loss a year.',
    no: 'Original hourly records were not obtained. It does not show that this region has the same ice.' },
  adv: { name: 'Adventdalen, Svalbard', where: '78.17°N, 16.06°E', url: 'https://doi.org/10.5194/tc-17-3363-2023',
    yes: 'Separate Adventdalen studies report radar returns and core observations. Their coordinates and exact radar-to-core correspondence are not established as one validation test.',
    no: 'Coordinates are not matched across the studies. Wetter and warmer than Mars.' },
  hau: { name: 'Haughton crater, Devon Island', where: '75.37°N, 89.53°W', url: 'https://doi.org/10.1029/2012JE004053',
    yes: 'The bounded published radar/core subcase used a short line after overburden excavation. The July 2019 thaw observations are a separate study and footprint.',
    no: 'Excavated cover does not validate intact-cover detection. Separate thaw and radar records cannot be combined into one ice truth.' },
  ad1: { name: 'Adventdalen polygons (AD1), Svalbard', where: '78.18°N, 15.92°E', url: 'https://doi.pangaea.de/10.1594/PANGAEA.921087',
    yes: '185 mapped polygons, median equivalent-circle diameter about 18.5 m. The site is identified as active ice-wedge terrain.',
    no: 'No ice volume and no matched temperature record.' }
};
var EARTH = { 'ms-01': ['uv', 'beacon'], 'ms-02': ['uv', 'beacon', 'adv', 'hau'], 'ms-03': ['uv', 'ad1'] };
var THEMES = [['ice', 'Ice'], ['heat', 'Heat'], ['terrain', 'Terrain'], ['dust', 'Dust']];
var SHORT = { uv: 'University Valley', beacon: 'Beacon', adv: 'Adventdalen', hau: 'Haughton', ad1: 'AD1 polygons' };
var LAT = { uv: -77.86, beacon: -77.82, adv: 78.17, hau: 75.37, ad1: 78.18 };
var CELLS = {
  uv: { ice: ['yes', 'Published valley-wide interfaces 8 to 42 cm below dry cover; this range is not one W-station profile.'], heat: ['part', 'Published depth-response summary; different from the separate air-temperature series and Mars surface products.'], terrain: ['no', 'Station elevations only. No slope or relief measured.'], dust: ['no', 'No dust measure obtained.'] },
  beacon: { ice: ['yes', 'Blocky ice under about 0.3 m of dry soil.'], heat: ['part', 'Published ground-temperature model. Raw records not obtained.'], terrain: ['part', 'Polygons 10 to 20 m across. No elevation model.'], dust: ['no', 'No column-dust equivalent.'] },
  adv: { ice: ['yes', 'Separate radar and core studies; no established line-to-core registration or joint ice truth.'], heat: ['no', 'Borehole temperatures not read.'], terrain: ['part', 'Polygons 10 to 20 m across. No elevation model.'], dust: ['no', 'Local loess source. Not column dust.'] },
  hau: { ice: ['yes', 'Bounded radar/core method reference after overburden excavation; not intact-cover validation.'], heat: ['part', 'Mean annual air about −15 °C, from secondary sources.'], terrain: ['part', 'Polygons and stripes 5 to 31 m. Tiny LiDAR coverage.'], dust: ['no', 'Not covered in the sources read.'] },
  ad1: { ice: ['part', 'Active ice-wedge terrain. No ice volume measured.'], heat: ['no', 'Monitoring temperatures are not matched to the polygons.'], terrain: ['part', '185 source polygons; median equivalent-circle diameter about 18.5 m. No qualified MS-03 contours for a paired comparison.'], dust: ['no', 'No dust measure obtained.'] }
};
var VERDICT = { yes: ['Earth evidence', '◆'], part: ['Partial reference', '◇'], no: ['Not comparable', '○'] };
var UV_MIN_C = [-20.4, -28.8, -40.1, -35.5, -45.5, -40.5, -45.5, -43.1, -42.0, -36.0, -27.2];
var UV_MAX_C = [-2.9, -9.3, -10.1, -15.7, -17.5, -18.0, -22.0, -20.1, -17.2, -12.2, -4.1];
var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'];
var cellSel = { pt: 'uv', th: 'ice' }, showMars = true;
var earthThermalOpen = false, earthLocationsOpen = false;
var uvMonth = null;

function matrixBox(active) {
  var pts = EARTH[SITES[active].hash], box = h('div', 'strip');
  box.appendChild(h('h3', null, 'What Earth supports'));
  box.appendChild(h('p', 'unit', 'Select a cell to inspect the Earth evidence and its limits. No matched Mars condition is validated.'));
  box.appendChild(h('div', 'matrix-key', '<span>◆ Earth evidence</span><span>◇ Partial reference</span><span>○ No comparable data</span>'));
  if (pts.indexOf(cellSel.pt) < 0) cellSel.pt = pts[0];
  var grid = h('div', 'mx'); grid.style.setProperty('--n', pts.length);
  grid.appendChild(h('span', 'mxh'));
  pts.forEach(function (k) { grid.appendChild(h('span', 'mxh', SHORT[k])); });
  var read = h('p', 'mxread'); read.setAttribute('aria-live', 'polite');
  function show() {
    var p = PTS[cellSel.pt], c = CELLS[cellSel.pt][cellSel.th], v = VERDICT[c[0]];
    read.innerHTML = '<b>' + p.name + ', ' + THEMES.filter(function (t) { return t[0] === cellSel.th; })[0][1] + ': ' + v[0] + '</b><br>' + c[1] +
      ' <a href="' + p.url + '">Published source</a><span class="matrix-limit">Use here: a method reference. ' + p.no + '</span>';
    Array.prototype.forEach.call(grid.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b.dataset.pt === cellSel.pt && b.dataset.th === cellSel.th ? 'true' : 'false'); });
  }
  THEMES.forEach(function (t) {
    grid.appendChild(h('span', 'mxr', t[1]));
    pts.forEach(function (k) {
      var c = CELLS[k][t[0]], v = VERDICT[c[0]], b = h('button', 'mxc mxc-' + c[0], '<i aria-hidden="true">' + v[1] + '</i>');
      b.type = 'button'; b.dataset.pt = k; b.dataset.th = t[0];
      b.setAttribute('aria-label', SHORT[k] + ', ' + t[1] + ': ' + v[0]);
      b.addEventListener('click', function () { cellSel = { pt: k, th: t[0] }; show(); });
      grid.appendChild(b);
    });
  });
  box.appendChild(grid); box.appendChild(read); show();
  return box;
}

function wavesBox() {
  var box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Published Earth depth-response summary'));
  box.appendChild(h('p', 'unit', 'Reported variation values for University Valley, 7 to 18 November 2010 (K). Bars show published summary values, not observed daily waveforms or reconstructed timing.'));
  var W = 420, H = 178, x0 = 108, x1 = W - 52, k = 2.3;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': 'Published temperature-variation summary by depth: ' + UV_DAMP.map(function (d) { return d[0] + ' ' + d[1] + ' kelvin'; }).join(', ') });
  el('rect', { x: 0, y: 0, width: W, height: 4 * 42 - 0, fill: 'rgba(224,166,79,.07)' }, svg);
  el('rect', { x: 0, y: 2 * 42, width: W, height: 2 * 42, fill: 'rgba(142,197,232,.12)' }, svg);
  UV_DAMP.forEach(function (d, r) {
    var cy = 21 + r * 42;
    var barWidth = d[1] / 9 * (x1 - x0);
    el('line', { x1: x0, x2: x1, y1: cy, y2: cy, stroke: '#232a35' }, svg);
    el('rect', { x: x0, y: cy - 8, width: barWidth, height: 16, fill: r < 2 ? '#e0a64f' : '#8ec5e8' }, svg);
    txt(svg, x0 - 10, cy + 4, d[0], { fill: '#c7ccd4', 'font-size': 12, 'text-anchor': 'end' });
    txt(svg, x1 + 10, cy + 4, num(d[1], d[1] < 1 ? 2 : 1) + ' K', { fill: '#fff', 'font-size': 12, 'font-weight': 700 });
  });
  txt(svg, 8, 14, 'dry cover', { fill: '#a3a9b3', 'font-size': 10 });
  txt(svg, 8, 2 * 42 + 14, 'ice', { fill: '#8ec5e8', 'font-size': 10 });
  box.appendChild(svg);
  box.appendChild(h('p', 'read', 'Summary values are a published Earth method reference. No sine wave, phase delay or missing time series has been generated. TES/MCS are different measurements; this does not establish the same process or ice depth on Mars.'));
  return box;
}

function earthTempBox(active) {
  var s = SITES[active], box = h('div', 'strip');
  box.appendChild(h('h3', null, 'University Valley air temperature'));
  box.appendChild(h('p', 'unit', 'January–November 2010 · air at 1.2 m · K. Select a month for its mean and range.'));
  var seg = h('div', 'seg'), bt = h('button', null, 'Show Mars surface context');
  bt.type = 'button'; bt.setAttribute('aria-pressed', showMars ? 'true' : 'false');
  bt.addEventListener('click', function () { showMars = !showMars; renderTab(); $('tabpanel').querySelector('.seg button').focus({ preventScroll: true }); });
  seg.appendChild(bt); box.appendChild(seg);
  var info = h('p', 'tip'); info.setAttribute('aria-live', 'polite');
  var W = 420, H = 190, left = 40, right = 14, top = 12, bot = 28, lo = 160, hi = 270;
  function Y(v) { return top + (hi - v) / (hi - lo) * (H - top - bot); }
  function X(i) { return left + i * (W - left - right) / 10; }
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', style: 'touch-action:pan-y',
    'aria-label': 'University Valley monthly air temperature, ' + num(UV_MONTHLY_C[0] + 273.15, 0) + ' kelvin in January to ' + num(UV_MONTHLY_C[6] + 273.15, 0) + ' in July. ' + s.id + ' Mars night median ' + num(s.night, 0) + ', day median ' + num(s.day, 0) + '.' });
  [180, 200, 220, 240, 260].forEach(function (v) {
    el('line', { x1: left, x2: W - right, y1: Y(v), y2: Y(v), stroke: '#1d2531' }, svg);
    txt(svg, left - 8, Y(v) + 4, String(v), { fill: '#8b929d', 'font-size': 11, 'text-anchor': 'end' });
  });
  ['Jan', 'Apr', 'Jul', 'Oct'].forEach(function (n, q) { txt(svg, X(q * 3), H - 8, n, { fill: '#a3a9b3', 'font-size': 11, 'text-anchor': 'middle' }); });
  var band = UV_MAX_C.map(function (c, i) { return X(i) + ',' + Y(c + 273.15); }).concat(UV_MIN_C.map(function (c, i) { return X(10 - i) + ',' + Y(UV_MIN_C[10 - i] + 273.15); }));
  el('polygon', { points: band.join(' '), fill: 'rgba(235,232,225,.12)' }, svg);
  if (showMars) ['night', 'day'].forEach(function (d) {
    el('line', { x1: left, x2: W - right, y1: Y(s[d]), y2: Y(s[d]), stroke: COLORS[active], 'stroke-width': 2, 'stroke-dasharray': '6 5' }, svg);
    txt(svg, W - right, Y(s[d]) + (d === 'day' ? 16 : -6), 'Mars ' + d + ' ' + num(s[d], 0), { fill: COLORS[active], 'font-size': 11, 'font-weight': 600, 'text-anchor': 'end' });
  });
  el('polyline', { points: UV_MONTHLY_C.map(function (c, i) { return X(i) + ',' + Y(c + 273.15); }).join(' '), fill: 'none', stroke: '#ebe8e1', 'stroke-width': 2.5, 'stroke-linejoin': 'round' }, svg);
  var cur = el('line', { y1: top, y2: H - bot, stroke: '#fff', 'stroke-width': 1, visibility: 'hidden' }, svg);
  var dot = el('rect', { width: 9, height: 9, fill: '#fff', stroke: '#04060a', 'stroke-width': 1.5, visibility: 'hidden' }, svg);
  function pickMonth(i) {
    uvMonth = i;
    var m = UV_MONTHLY_C[i] + 273.15;
    cur.setAttribute('x1', X(i)); cur.setAttribute('x2', X(i)); cur.setAttribute('visibility', 'visible');
    dot.setAttribute('x', X(i) - 4.5); dot.setAttribute('y', Y(m) - 4.5); dot.setAttribute('visibility', 'visible');
    info.innerHTML = '<b>' + MONTHS[i] + '</b> mean ' + num(m, 0) + ' K, range ' + num(UV_MIN_C[i] + 273.15, 0) + ' to ' + num(UV_MAX_C[i] + 273.15, 0) + ' K';
    monthSelect.value = String(i);
  }
  function pick(e) {
    var r = svg.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * W;
    pickMonth(Math.max(0, Math.min(10, Math.round((x - left) / ((W - left - right) / 10)))));
  }
  var monthLabel = h('label', 'month-picker', 'Month');
  var monthSelect = h('select'); monthSelect.setAttribute('aria-label', 'University Valley month');
  MONTHS.forEach(function (m, i) { var option = h('option', null, m); option.value = i; monthSelect.appendChild(option); });
  monthSelect.addEventListener('change', function () { pickMonth(Number(this.value)); });
  monthLabel.appendChild(monthSelect); box.appendChild(monthLabel);
  svg.addEventListener('pointermove', pick); svg.addEventListener('pointerdown', pick);
  info.innerHTML = 'Mean <b>261 K in January, 239 K in July</b>. Air at 1.2 m, not surface.';
  if (uvMonth !== null) pickMonth(uvMonth);
  box.appendChild(info); box.appendChild(svg);
  box.appendChild(h('p', 'read', 'Earth air at 1.2 m and model-time-adjusted Mars surface medians have different instruments, periods and supports. These overlays are context, not a match or paired daily amplitude.'));
  return box;
}

function ladderBox(active) {
  var s = SITES[active], pts = EARTH[s.hash], box = h('div', 'strip');
  box.appendChild(h('h3', null, 'Where the Earth points sit'));
  box.appendChild(h('p', 'unit', 'Latitude of ' + s.id + ' and the Earth points used. Cold deserts, at very different latitudes.'));
  var W = 420, H = 110, x0 = 16, x1 = W - 16;
  function X(l) { return x0 + (l + 90) / 180 * (x1 - x0); }
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': s.id + ' at ' + num(s.lat, 1) + ' degrees north. Earth points: ' + pts.map(function (k) { return SHORT[k] + ' ' + num(LAT[k], 1); }).join(', ') });
  el('line', { x1: x0, x2: x1, y1: 56, y2: 56, stroke: '#3a4452', 'stroke-width': 2 }, svg);
  [-90, -60, -30, 0, 30, 60, 90].forEach(function (l) {
    el('line', { x1: X(l), x2: X(l), y1: 52, y2: 60, stroke: '#3a4452' }, svg);
    txt(svg, X(l), 76, (l < 0 ? '−' + (-l) : l) + '°', { fill: '#8b929d', 'font-size': 10, 'text-anchor': l === -90 ? 'start' : (l === 90 ? 'end' : 'middle') });
  });
  var items = pts.map(function (k) { return { x: X(LAT[k]), t: SHORT[k], earth: true }; });
  items.push({ x: X(s.lat), t: s.id + ' (Mars)', earth: false });
  items.sort(function (a, b) { return a.x - b.x; });
  var lanes = [{ y: 24, end: -99 }, { y: 100, end: -99 }, { y: 40, end: -99 }];
  items.forEach(function (it, q) {
    var wd = it.t.length * 6.4 + 8, left = it.x - wd / 2;
    left = Math.max(2, Math.min(W - wd - 2, left));
    var lane = lanes.filter(function (l) { return left > l.end; })[0] || lanes[q % 3];
    lane.end = left + wd;
    var col = it.earth ? '#ebe8e1' : COLORS[active];
    if (it.earth) el('circle', { cx: it.x, cy: 56, r: 5, fill: '#ebe8e1', stroke: '#04060a', 'stroke-width': 1.5 }, svg);
    else el('path', { d: 'M' + it.x + ' 49L' + (it.x + 7) + ' 56L' + it.x + ' 63L' + (it.x - 7) + ' 56Z', fill: col, stroke: '#04060a', 'stroke-width': 1.5 }, svg);
    txt(svg, left + wd / 2, lane.y, it.t, { fill: it.earth ? '#c7ccd4' : col, 'font-size': 11, 'font-weight': it.earth ? 500 : 700, 'text-anchor': 'middle' });
  });
  box.appendChild(svg);
  return box;
}

function renderTab() {
  var p = $('tabpanel'); p.innerHTML = '';
  var i = selected; if (i < 0) return;
  p.style.setProperty('--c', COLORS[i]);
  $('tabs').style.setProperty('--c', COLORS[i]);
  var context = TAB_CONTEXT[tab];
  p.appendChild(h('p', 'panel-summary', context.takeaway));
  p.appendChild(h('p', 'support-line', context.support));
  if (tab === 'terrain') { p.appendChild(strip('slope', i)); p.appendChild(strip('relief', i)); p.appendChild(strip('elev', i)); }
  else if (tab === 'heat') { p.appendChild(strip('ti', i)); p.appendChild(coverageBox(i)); p.appendChild(swingBox(i)); }
  else if (tab === 'ice') { p.appendChild(strip('swim1', i)); p.appendChild(strip('swim5', i)); }
  else if (tab === 'dust') { p.appendChild(dustBox(i)); p.appendChild(strip('p95', i)); }
  else if (tab === 'earth') {
    p.appendChild(matrixBox(i));
    var thermal = h('details', 'research-detail');
    thermal.open = earthThermalOpen;
    thermal.addEventListener('toggle', function () { earthThermalOpen = thermal.open; });
    thermal.appendChild(h('summary', null, 'Explore thermal observations<span>University Valley · separate ground and air records</span>'));
    thermal.appendChild(wavesBox()); thermal.appendChild(earthTempBox(i)); p.appendChild(thermal);
    var locations = h('details', 'research-detail');
    locations.open = earthLocationsOpen;
    locations.addEventListener('toggle', function () { earthLocationsOpen = locations.open; });
    locations.appendChild(h('summary', null, 'Compare reference locations<span>Latitude context across two planets</span>'));
    locations.appendChild(ladderBox(i)); p.appendChild(locations);
  }
  else p.appendChild(unknowns(i));
  var source = h('details', 'source-details');
  source.appendChild(h('summary', null, 'Source & scale'));
  source.appendChild(h('p', null, context.method));
  var links = h('ul');
  [context.provider, context.extra, ['Retained regional values (CSV)', REPO + RESEARCH + 'final_candidates.csv'], ['Processing and scale notes', REPO + RESEARCH + 'COMPUTATION.md']].filter(Boolean).forEach(function (item) {
    var li = h('li'); li.appendChild(h('a', null, item[0])); li.firstChild.href = item[1]; links.appendChild(li);
  });
  if (tab === 'earth') {
    var li = h('li');
    li.appendChild(h('a', null, SITES[i].id + ' Earth reference records'));
    li.firstChild.href = REPO + 'outputs/research/' + SITES[i].id + '/candidates.csv'; links.appendChild(li);
  }
  source.appendChild(links);
  source.appendChild(h('p', 'source-version', 'Repository source snapshot: 25b0744 · 15 Nov 2026. Provider observations have their own dates and footprints.'));
  p.appendChild(source);
}

/* ---------- wiring ---------- */
$('btn-back').addEventListener('click', home);
$('btn-overview').addEventListener('click', home);
$('btn-home').addEventListener('click', home);
$('region-select').addEventListener('change', function () { select(Number(this.value)); });
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
  $('map-message').hidden = true;
  drawGlobe();
};
img.onerror = function () { mapMessage('The base map could not load. Region controls and research data remain available.'); };
img.src = 'mola.jpg';
$('retry-map').addEventListener('click', function () {
  $('map-message').hidden = true;
  if (!tex) img.src = 'mola.jpg?retry=' + Date.now();
  else if (selected >= 0) { patchFor = -1; loadPatch(selected); }
});

buildOverview();
setZoomState();
stars();
var rt = 0;
window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(stars, 150); });
fromHash();
})();
