(function () {
'use strict';
var NS = 'http://www.w3.org/2000/svg';
var RAD = Math.PI / 180;
var COLORS = ['#8ec5e8', '#e0a64f', '#cf8fd6'];

/* Values are native-cell means or review-area statistics from
   outputs/research/mars_reselection_20261114/final_candidates.csv */
var SITES = [
  { id: 'MS-01', lat: 56.75, lon: 72.75,
    coords: '56.75°N, 72.75°E',
    text: 'Ice evidence is consistent at both depths and the terrain is low and level. Thermal inertia is the highest of the three, but only 73 of 100 thermal cells hold direct measurements.',
    slope: 0.287, relief: 76, ti: 325.2, swim1: 0.639, swim5: 0.647, p95: 0.222,
    dust34: [0.1236, 0.1005, 0.1662, 0.0921], dust35: [0.1344, 0.0920, 0.1021, 0.0969],
    night: 173.7, day: 247.5 },
  { id: 'MS-02', lat: 52.75, lon: 168.25,
    coords: '52.75°N, 168.25°E',
    text: 'The southernmost of the three, with the fullest thermal coverage: 93 of 100 cells. Dust haze peaks higher here and the ground has more relief, 117 meters across the area.',
    slope: 0.302, relief: 117, ti: 217.3, swim1: 0.693, swim5: 0.622, p95: 0.240,
    dust34: [0.1295, 0.1091, 0.1534, 0.1131], dust35: [0.1412, 0.1066, 0.0904, 0.0934],
    night: 171.3, day: 246.3 },
  { id: 'MS-03', lat: 57.75, lon: 242.25,
    coords: '57.75°N, 242.25°E',
    text: 'The flattest and least hazy of the three, with the strongest signal in the top meter. That signal weakens between 1 and 5 meters, and thermal coverage is partial: 79 of 100 cells.',
    slope: 0.163, relief: 76, ti: 152.8, swim1: 0.911, swim5: 0.510, p95: 0.173,
    dust34: [0.1055, 0.0839, 0.1208, 0.0847], dust35: [0.1080, 0.0791, 0.0830, 0.0807],
    night: 154.6, day: 234.9 }
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
  t.textContent = s;
  return t;
}
function fmt(v, d) { return v.toFixed(d); }

/* ---------- star field (static) ---------- */
function stars() {
  var c = $('stars'), dpr = Math.min(window.devicePixelRatio || 1, 2);
  var w = window.innerWidth, h = window.innerHeight;
  c.width = w * dpr; c.height = h * dpr;
  var g = c.getContext('2d');
  g.scale(dpr, dpr);
  var s = 7;
  function rnd() { s = (s * 16807) % 2147483647; return s / 2147483647; }
  var n = Math.round((w * h) / 5500);
  for (var i = 0; i < n; i++) {
    var r = 0.3 + Math.pow(rnd(), 3) * 1.0;
    g.globalAlpha = 0.2 + rnd() * 0.6;
    g.fillStyle = rnd() < 0.15 ? '#ffd9b0' : (rnd() < 0.3 ? '#cfe3ff' : '#ffffff');
    g.beginPath(); g.arc(rnd() * w, rnd() * h, r, 0, 6.2832); g.fill();
  }
}

/* ---------- globe ---------- */
var view = { lon: 157 * RAD, lat: 40 * RAD };
var selected = 0;
var texW = 0, texH = 0, tex = null;
var canvas = $('globe'), ctx = canvas.getContext('2d');
var N = canvas.width, R = N / 2;
var frame = ctx.createImageData(N, N);
var out = new Uint32Array(frame.data.buffer);
var L = (function () { var v = [-0.45, 0.42, 0.78], m = Math.hypot(v[0], v[1], v[2]); return [v[0] / m, v[1] / m, v[2] / m]; })();

function project(latDeg, lonDeg) {
  var p = latDeg * RAD, dl = lonDeg * RAD - view.lon;
  var x = Math.cos(p) * Math.sin(dl);
  var y = Math.cos(view.lat) * Math.sin(p) - Math.sin(view.lat) * Math.cos(p) * Math.cos(dl);
  var z = Math.sin(view.lat) * Math.sin(p) + Math.cos(view.lat) * Math.cos(p) * Math.cos(dl);
  return { x: R + x * R, y: R - y * R, z: z };
}

function drawGlobe() {
  if (!tex) return;
  var sinP0 = Math.sin(view.lat), cosP0 = Math.cos(view.lat);
  var i = 0;
  for (var y = 0; y < N; y++) {
    var ny = 1 - 2 * (y + 0.5) / N;
    for (var x = 0; x < N; x++, i++) {
      var nx = 2 * (x + 0.5) / N - 1, r2 = nx * nx + ny * ny;
      if (r2 > 1) { out[i] = 0; continue; }
      var nz = Math.sqrt(1 - r2);
      var phi = Math.asin(nz * sinP0 + ny * cosP0);
      var lam = view.lon + Math.atan2(nx, nz * cosP0 - ny * sinP0);
      var u = lam / 6.283185307; u -= Math.floor(u);
      var tx = (u * texW) | 0, ty = ((0.5 - phi / Math.PI) * texH) | 0;
      if (ty < 0) ty = 0; else if (ty >= texH) ty = texH - 1;
      var c = tex[ty * texW + tx];
      var lam2 = nx * L[0] + ny * L[1] + nz * L[2];
      var sh = (0.16 + 0.84 * Math.pow(lam2 > 0 ? lam2 : 0, 0.8)) * (0.6 + 0.4 * nz);
      var rr = (c & 255) * sh, gg = ((c >> 8) & 255) * sh, bb = ((c >> 16) & 255) * sh;
      out[i] = 0xff000000 | ((bb > 255 ? 255 : bb) << 16) | ((gg > 255 ? 255 : gg) << 8) | (rr > 255 ? 255 : rr);
    }
  }
  ctx.putImageData(frame, 0, 0);
  /* thin atmosphere edge */
  var gr = ctx.createRadialGradient(R, R, R * 0.965, R, R, R);
  gr.addColorStop(0, 'rgba(224,166,79,0)');
  gr.addColorStop(1, 'rgba(224,166,79,0.35)');
  ctx.fillStyle = gr;
  ctx.beginPath(); ctx.arc(R, R, R, 0, 6.2832); ctx.fill();
  /* markers */
  ctx.font = '600 22px "Schibsted Grotesk", system-ui, sans-serif';
  ctx.textBaseline = 'middle';
  SITES.forEach(function (s, k) {
    var p = project(s.lat, s.lon);
    if (p.z < 0.25) return;
    var on = k === selected, rad = on ? 15 : 11;
    ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(4,6,10,0.85)'; ctx.lineWidth = on ? 7 : 6;
    ctx.beginPath(); ctx.arc(p.x, p.y, rad, 0, 6.2832); ctx.stroke();
    ctx.strokeStyle = COLORS[k]; ctx.lineWidth = on ? 3.5 : 2.5;
    ctx.beginPath(); ctx.arc(p.x, p.y, rad, 0, 6.2832); ctx.stroke();
    ctx.fillStyle = COLORS[k];
    ctx.beginPath(); ctx.arc(p.x, p.y, 3.5, 0, 6.2832); ctx.fill();
    var lx = p.x + rad + 8;
    var flip = lx + 64 > N;
    ctx.textAlign = flip ? 'right' : 'left';
    if (flip) lx = p.x - rad - 8;
    ctx.strokeStyle = 'rgba(4,6,10,0.9)'; ctx.lineWidth = 5;
    ctx.strokeText(s.id, lx, p.y);
    ctx.fillStyle = '#ffffff';
    ctx.fillText(s.id, lx, p.y);
  });
}

var raf = 0;
function schedule() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; drawGlobe(); }); }

function select(k, move) {
  selected = k;
  var s = SITES[k];
  Array.prototype.forEach.call(document.querySelectorAll('.picker button'), function (b, i) {
    b.setAttribute('aria-pressed', i === k ? 'true' : 'false');
  });
  $('r-coords').textContent = s.id + '  ' + s.coords;
  $('r-text').textContent = s.text;
  if (move) rotateTo(s.lon * RAD, Math.min(s.lat * 0.75, 55) * RAD); else schedule();
}

var tween = 0;
function rotateTo(lon, lat) {
  cancelAnimationFrame(tween);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dl = ((lon - view.lon + Math.PI * 3) % (Math.PI * 2)) - Math.PI;
  var l0 = view.lon, p0 = view.lat, dp = lat - view.lat, t0 = performance.now(), D = 800;
  if (reduce) { view.lon = lon; view.lat = lat; drawGlobe(); return; }
  (function step(now) {
    var t = Math.min(1, (now - t0) / D), e = 1 - Math.pow(1 - t, 3);
    view.lon = l0 + dl * e; view.lat = p0 + dp * e;
    drawGlobe();
    if (t < 1) tween = requestAnimationFrame(step);
  })(t0);
}

/* drag + tap */
var drag = null;
canvas.addEventListener('pointerdown', function (e) {
  cancelAnimationFrame(tween);
  canvas.setPointerCapture(e.pointerId);
  drag = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY };
});
canvas.addEventListener('pointermove', function (e) {
  if (!drag) return;
  var k = N / canvas.getBoundingClientRect().width;
  var dx = (e.clientX - drag.x) * k / R, dy = (e.clientY - drag.y) * k / R;
  drag.x = e.clientX; drag.y = e.clientY;
  view.lon -= dx / Math.max(0.35, Math.cos(view.lat));
  view.lat = Math.max(-1.3, Math.min(1.3, view.lat + dy));
  schedule();
});
canvas.addEventListener('pointerup', function (e) {
  if (!drag) return;
  var moved = Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy);
  drag = null;
  if (moved < 6) {
    var rect = canvas.getBoundingClientRect(), k = N / rect.width;
    var px = (e.clientX - rect.left) * k, py = (e.clientY - rect.top) * k;
    var best = -1, bd = 34;
    SITES.forEach(function (s, i) {
      var p = project(s.lat, s.lon), d = Math.hypot(p.x - px, p.y - py);
      if (p.z > 0.25 && d < bd) { bd = d; best = i; }
    });
    if (best >= 0) select(best, true);
  }
});
canvas.addEventListener('pointercancel', function () { drag = null; });

Array.prototype.forEach.call(document.querySelectorAll('.picker button'), function (b) {
  b.addEventListener('click', function () { select(+b.getAttribute('data-i'), true); });
});

var img = new Image();
img.onload = function () {
  var o = document.createElement('canvas');
  o.width = texW = img.naturalWidth; o.height = texH = img.naturalHeight;
  var g = o.getContext('2d');
  g.drawImage(img, 0, 0);
  tex = new Uint32Array(g.getImageData(0, 0, texW, texH).data.buffer);
  drawGlobe();
};
img.src = 'mola.jpg';

/* ---------- charts ---------- */
var METRICS = [
  { key: 'slope', title: 'Average slope', unit: 'degrees', dom: [0, 0.4], d: 3,
    read: 'MS-03 is the flattest. All three are nearly level at this scale, and an average cannot show hazards at landing scale.' },
  { key: 'relief', title: 'Height range', unit: 'meters, lowest to highest point', dom: [0, 140], d: 0,
    read: 'MS-02 spans the most height. MS-01 and MS-03 are equal at 76 m.' },
  { key: 'ti', title: 'Thermal inertia', unit: 'J m⁻² K⁻¹ s⁻½, how slowly the surface changes temperature', dom: [0, 350], d: 0,
    read: 'MS-01 is highest. Thermal inertia can come from rock, sand, ice or cementation, so a high value does not show harder ground or more ice.' },
  { key: 'swim1', title: 'Ice evidence, top meter', unit: 'consistency index from 0 to 1', dom: [0, 1], d: 2,
    read: 'MS-03 is highest. This index measures how well the data fits ice. It is not an amount or a probability.' },
  { key: 'swim5', title: 'Ice evidence, 1 to 5 meters', unit: 'consistency index from 0 to 1', dom: [0, 1], d: 2,
    read: 'MS-03 drops to the lowest here, so its signal is concentrated near the surface.' },
  { key: 'p95', title: 'Peak dust haze', unit: 'opacity, Mars year 34, 95th percentile', dom: [0, 0.3], d: 3,
    read: 'MS-02 has the haziest air on its worst days. MS-03 has the clearest.' }
];

function dotRow(m) {
  var row = document.createElement('div'); row.className = 'dot-row';
  var head = document.createElement('div');
  head.innerHTML = '<h3></h3><p class="unit"></p>';
  head.firstChild.textContent = m.title; head.lastChild.textContent = m.unit;
  var box = document.createElement('div');
  var narrow = window.innerWidth < 640;
  var W = narrow ? 340 : 600, H = narrow ? 104 : 84, x0 = 14, x1 = W - 14, ay = 39;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': m.title + ': ' + SITES.map(function (s) { return s.id + ' ' + fmt(s[m.key], m.d); }).join(', ') });
  function X(v) { return x0 + (v - m.dom[0]) / (m.dom[1] - m.dom[0]) * (x1 - x0); }
  el('line', { x1: x0, x2: x1, y1: ay, y2: ay, stroke: '#2c3542', 'stroke-width': 1 }, svg);
  [m.dom[0], m.dom[1]].forEach(function (v, i) {
    el('line', { x1: X(v), x2: X(v), y1: ay - 5, y2: ay + 5, stroke: '#2c3542' }, svg);
    txt(svg, X(v) + (i ? 6 : -6), H - 4, String(v), { fill: '#8b929d', 'font-size': 11, 'text-anchor': i ? 'end' : 'start' });
  });
  var order = SITES.map(function (s, i) { return i; }).sort(function (a, b) { return SITES[a][m.key] - SITES[b][m.key]; });
  var groups = {};
  SITES.forEach(function (s) { var k = Math.round(X(s[m.key])); groups[k] = (groups[k] || 0) + 1; });
  var seen = {}, lanes = [{ y: ay - 15, end: -1e9 }, { y: ay + 30, end: -1e9 }, { y: ay + 48, end: -1e9 }];
  order.forEach(function (i) {
    var s = SITES[i], v = s[m.key], x = X(v), key = Math.round(x);
    var tie = (seen[key] = (seen[key] || 0) + 1) - 1;
    var off = groups[key] > 1 ? (tie ? 6 : -6) : 0;
    el('circle', { cx: x, cy: ay + off, r: 8, fill: COLORS[i], stroke: '#04060a', 'stroke-width': 2 }, svg);
    var label = s.id + '  ' + fmt(v, m.d), wd = label.length * 7.6 + 12;
    var anchor = x > W - 70 ? 'end' : (x < 70 ? 'start' : 'middle');
    var left = anchor === 'end' ? x - wd : (anchor === 'start' ? x : x - wd / 2);
    var lane = lanes.filter(function (l) { return left > l.end; })[0] || lanes[2];
    lane.end = left + wd;
    var t = txt(svg, x, lane.y, label, { fill: '#ebe8e1', 'font-size': 13, 'font-weight': 600, 'text-anchor': anchor });
    t.style.fontVariantNumeric = 'tabular-nums';
  });
  box.appendChild(svg);
  var read = document.createElement('p'); read.className = 'read'; read.textContent = m.read;
  row.appendChild(head); row.appendChild(box); row.appendChild(read);
  return row;
}

function seasonChart(host, key, title) {
  var W = 300, H = 236, left = 38, right = 58, top = 30, bot = 34;
  var lo = 0.06, hi = 0.18;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': title + ' dust opacity by season for MS-01, MS-02 and MS-03' });
  txt(svg, 0, 12, title, { fill: '#ebe8e1', 'font-size': 14, 'font-weight': 600 });
  function Y(v) { return top + (hi - v) / (hi - lo) * (H - top - bot); }
  function X(i) { return left + i * (W - left - right) / 3; }
  [0.08, 0.12, 0.16].forEach(function (v) {
    el('line', { x1: left - 4, x2: W - right + 6, y1: Y(v), y2: Y(v), stroke: '#1d2531' }, svg);
    txt(svg, left - 10, Y(v) + 4, v.toFixed(2), { fill: '#8b929d', 'font-size': 11, 'text-anchor': 'end' });
  });
  ['Spring', 'Summer', 'Autumn', 'Winter'].forEach(function (n, i) {
    txt(svg, X(i), H - 12, n, { fill: '#a3a9b3', 'font-size': 11, 'text-anchor': i === 0 ? 'start' : (i === 3 ? 'end' : 'middle') });
  });
  var ends = [];
  SITES.forEach(function (s, k) {
    var pts = s[key].map(function (v, i) { return X(i) + ',' + Y(v); }).join(' ');
    el('polyline', { points: pts, fill: 'none', stroke: COLORS[k], 'stroke-width': 2.5, 'stroke-linejoin': 'round' }, svg);
    s[key].forEach(function (v, i) { el('circle', { cx: X(i), cy: Y(v), r: 3.5, fill: COLORS[k], stroke: '#04060a', 'stroke-width': 1.5 }, svg); });
    ends.push({ k: k, y: Y(s[key][3]) });
  });
  ends.sort(function (a, b) { return a.y - b.y; });
  for (var i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 14) ends[i].y = ends[i - 1].y + 14;
  ends.forEach(function (e) { txt(svg, W - right + 14, e.y + 4, SITES[e.k].id, { fill: COLORS[e.k], 'font-size': 12, 'font-weight': 600 }); });
  host.appendChild(svg);
}

function swingChart(host) {
  var W = 460, H = 200, x0 = 20, x1 = W - 24, lo = 140, hi = 260, top = 14;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img',
    'aria-label': 'Median night and day temperature in kelvin: ' + SITES.map(function (s) { return s.id + ' ' + s.night.toFixed(0) + ' to ' + s.day.toFixed(0); }).join(', ') });
  function X(v) { return x0 + (v - lo) / (hi - lo) * (x1 - x0); }
  [160, 180, 200, 220, 240].forEach(function (v) {
    el('line', { x1: X(v), x2: X(v), y1: top, y2: H - 34, stroke: '#1d2531' }, svg);
    txt(svg, X(v), H - 16, String(v), { fill: '#8b929d', 'font-size': 11, 'text-anchor': 'middle' });
  });
  txt(svg, x1, H - 1, 'kelvin', { fill: '#8b929d', 'font-size': 11, 'text-anchor': 'end' });
  SITES.forEach(function (s, k) {
    var y = top + 24 + k * 50;
    el('line', { x1: X(s.night), x2: X(s.day), y1: y, y2: y, stroke: COLORS[k], 'stroke-width': 3, opacity: 0.55 }, svg);
    el('circle', { cx: X(s.night), cy: y, r: 7, fill: '#04060a', stroke: COLORS[k], 'stroke-width': 2.5 }, svg);
    el('circle', { cx: X(s.day), cy: y, r: 7, fill: COLORS[k], stroke: '#04060a', 'stroke-width': 2 }, svg);
    txt(svg, X(s.night) - 14, y + 4, fmt(s.night, 0), { fill: '#ebe8e1', 'font-size': 12, 'font-weight': 600, 'text-anchor': 'end' });
    txt(svg, X(s.day) + 14, y + 4, fmt(s.day, 0), { fill: '#ebe8e1', 'font-size': 12, 'font-weight': 600 });
    txt(svg, X(s.night) + (X(s.day) - X(s.night)) / 2, y - 13, s.id, { fill: COLORS[k], 'font-size': 12, 'font-weight': 600, 'text-anchor': 'middle' });
  });
  host.appendChild(svg);
  var key = document.createElement('p'); key.className = 'note';
  key.textContent = 'Hollow dot: night median. Filled dot: day median. Medians use every valid bin, so each gap differs from the paired day-and-night difference of 64 to 67 K.';
  host.appendChild(key);
}

var dots = $('dots');
METRICS.forEach(function (m) { dots.appendChild(dotRow(m)); });
seasonChart($('dust'), 'dust34', 'Mars year 34');
seasonChart($('dust'), 'dust35', 'Mars year 35');
swingChart($('swing'));

stars();
var rt = 0;
window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(stars, 150); });
select(0, false);
})();
