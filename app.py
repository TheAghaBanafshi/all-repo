# -*- coding: utf-8 -*-
"""
Funk Land v5.0 - بدون اکولایزر + فونت خفن
اجرا: python app.py
"""
import os
import json
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "funkland-super-secret-key-change-me"

# ================== تنظیمات ==================
ADMIN_PATH = "/adminer/aghabanafshi/1/managepanel/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)
DATA_FILE = os.path.join(BASE_DIR, "songs.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"username": "admin", "password": "funkland1400"}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def load_songs():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

def save_songs(songs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)

# ================== تمپلیت اصلی ==================
MAIN_HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Funk Land</title>

<!-- فونت‌های گوگل -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">

<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { overflow-x: hidden; }

  /* ============ فونت‌ها ============ */
  body {
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    background: #0a0014;
    color: #fff;
    min-height: 100vh;
  }

  .funk-title {
    font-family: 'Orbitron', 'Vazirmatn', Tahoma, sans-serif;
    letter-spacing: 4px;
  }

  /* ============ کرسر سفارشی ============ */
  @media (hover: hover) and (pointer: fine) {
    * { cursor: none !important; }
  }

  #cursor-dot {
    position: fixed; width: 10px; height: 10px;
    background: #b366ff; border-radius: 50%;
    pointer-events: none; z-index: 99999;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 15px #b366ff, 0 0 30px #8a2be2;
    transition: transform 0.05s ease-out, width 0.2s, height 0.2s;
    mix-blend-mode: screen;
  }
  #cursor-ring {
    position: fixed; width: 40px; height: 40px;
    border: 2px solid #b366ff; border-radius: 50%;
    pointer-events: none; z-index: 99998;
    transform: translate(-50%, -50%);
    transition: transform 0.15s ease-out, width 0.25s, height 0.25s, border-color 0.25s, background 0.25s;
    background: rgba(179,102,255,0.08);
    box-shadow: 0 0 20px rgba(179,102,255,0.6);
  }
  #cursor-ring.hover {
    width: 65px; height: 65px;
    border-color: #fff;
    background: rgba(179,102,255,0.25);
    box-shadow: 0 0 30px #b366ff, 0 0 60px #8a2be2;
  }
  #cursor-dot.hover { width: 16px; height: 16px; background: #fff; }

  @media (hover: none), (pointer: coarse) {
    #cursor-dot, #cursor-ring { display: none !important; }
    * { cursor: auto !important; }
  }

  /* ============ تریلر ============ */
  #trailer {
    position: fixed; inset: 0;
    background: radial-gradient(circle at 50% 50%, #2a0050 0%, #0a0014 70%);
    display: flex; justify-content: center; align-items: center;
    z-index: 9999; overflow: hidden; flex-direction: column;
    padding: 20px;
  }

  .particle {
    position: absolute; width: 6px; height: 6px;
    background: #b366ff; border-radius: 50%;
    box-shadow: 0 0 20px #b366ff, 0 0 40px #8a2be2;
    animation: floatParticle 8s infinite ease-in-out;
  }
  @keyframes floatParticle {
    0%,100% { transform: translate(0,0) scale(1); opacity: 0.3; }
    50% { transform: translate(40px,-60px) scale(1.8); opacity: 1; }
  }

  #trailer-text {
    font-size: clamp(1.5rem, 6vw, 5rem);
    font-weight: 900; text-align: center; color: #fff;
    text-shadow: 0 0 20px #b366ff, 0 0 40px #8a2be2, 0 0 80px #6a0dad;
    animation: pulse 2s infinite ease-in-out;
    padding: 20px; z-index: 2;
    transition: all 0.5s ease;
    position: relative;
    max-width: 95vw;
    word-wrap: break-word;
  }
  @keyframes pulse { 0%,100%{transform:scale(1);} 50%{transform:scale(1.05);} }

  .glitch { animation: glitch 0.3s infinite; }
  @keyframes glitch {
    0% { transform: translate(0); text-shadow: 0 0 20px #b366ff, 0 0 40px #8a2be2; }
    20% { transform: translate(-3px, 2px); text-shadow: 3px 0 #ff00ff, -3px 0 #00ffff; }
    40% { transform: translate(3px, -2px); text-shadow: -3px 0 #ff00ff, 3px 0 #00ffff; }
    60% { transform: translate(-2px, -3px); text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
    80% { transform: translate(2px, 3px); text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
    100% { transform: translate(0); text-shadow: 0 0 20px #b366ff, 0 0 40px #8a2be2; }
  }

  .shake { animation: shake 0.5s; }
  @keyframes shake {
    0%,100% { transform: translate(0); }
    10%,30%,50%,70%,90% { transform: translate(-8px, 4px); }
    20%,40%,60%,80% { transform: translate(8px, -4px); }
  }

  #enter-btn {
    position: absolute; bottom: 15%;
    padding: 16px 45px;
    font-size: clamp(1rem, 3vw, 1.4rem); font-weight: bold;
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    color: #fff;
    background: linear-gradient(135deg, #8a2be2, #b366ff);
    border: none; border-radius: 50px; cursor: pointer;
    box-shadow: 0 0 30px #8a2be2, 0 0 60px #6a0dad;
    animation: pulse 1.5s infinite;
    transition: transform 0.3s;
    z-index: 3;
  }
  #enter-btn:hover { transform: scale(1.1); }

  #loading-bar {
    position: absolute; bottom: 8%;
    width: 70%; max-width: 500px; height: 6px;
    background: rgba(179,102,255,0.2);
    border-radius: 10px; overflow: hidden;
  }
  #loading-fill {
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #8a2be2, #b366ff);
    box-shadow: 0 0 20px #b366ff;
    transition: width 0.3s linear;
  }

  #flash {
    position: fixed; inset: 0; background: #fff;
    opacity: 0; pointer-events: none; z-index: 10000;
    transition: opacity 0.3s;
  }

  /* ============ صفحه اصلی ============ */
  #main-site {
    display: none; padding: 30px 15px; min-height: 100vh;
    background:
      radial-gradient(circle at 20% 10%, #3a0060 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, #6a0dad 0%, transparent 50%),
      #0a0014;
    position: relative; overflow: hidden;
  }
  #main-site::before {
    content:''; position: absolute; inset: 0;
    background-image:
      radial-gradient(2px 2px at 20% 30%, #b366ff, transparent),
      radial-gradient(2px 2px at 60% 70%, #8a2be2, transparent),
      radial-gradient(2px 2px at 80% 20%, #b366ff, transparent),
      radial-gradient(2px 2px at 30% 80%, #8a2be2, transparent);
    background-size: 200px 200px;
    animation: moveBg 20s linear infinite;
    opacity: 0.6; pointer-events: none;
  }
  @keyframes moveBg { from{background-position:0 0;} to{background-position:200px 200px;} }

  .header { text-align: center; margin-bottom: 30px; position: relative; z-index: 1; }
  .header h1 {
    font-family: 'Orbitron', 'Vazirmatn', Tahoma, sans-serif;
    font-size: clamp(2rem, 8vw, 5rem); font-weight: 900;
    letter-spacing: 6px;
    background: linear-gradient(90deg, #b366ff, #fff, #b366ff);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    margin-bottom: 10px;
    word-wrap: break-word;
    text-shadow: 0 0 40px rgba(179,102,255,0.5);
  }
  @keyframes shine { to { background-position: 200% center; } }
  .header p {
    color: #b366ff;
    font-size: clamp(0.9rem, 3vw, 1.2rem);
    text-shadow: 0 0 15px #8a2be2;
    font-weight: 700;
  }

  #replay-btn {
    display: block; margin: 15px auto 30px;
    padding: 12px 30px;
    background: transparent;
    border: 2px solid #b366ff;
    color: #b366ff;
    border-radius: 30px; cursor: pointer;
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    font-size: clamp(0.9rem, 2.5vw, 1rem); font-weight: bold;
    transition: all 0.3s;
    position: relative; z-index: 1;
  }
  #replay-btn:hover {
    background: #b366ff; color: #0a0014;
    box-shadow: 0 0 30px #b366ff;
    transform: scale(1.05);
  }

  .songs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px; max-width: 1200px; margin: 0 auto;
    position: relative; z-index: 1;
  }

  @media (max-width: 600px) {
    .songs-grid { grid-template-columns: 1fr; gap: 15px; }
    .song-card { padding: 18px; }
    #replay-btn { padding: 10px 20px; }
    #enter-btn { bottom: 20%; padding: 14px 30px; }
  }

  /* ============ کارت آهنگ ============ */
  .song-card {
    background: rgba(138, 43, 226, 0.15);
    border: 2px solid rgba(179, 102, 255, 0.4);
    border-radius: 20px; padding: 25px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative; overflow: hidden;
  }
  .song-card::before {
    content:''; position: absolute; inset: 0;
    background: linear-gradient(135deg, transparent, rgba(179,102,255,0.3), transparent);
    transform: translateX(-100%); transition: transform 0.6s;
    pointer-events: none;
  }
  .song-card:hover::before { transform: translateX(100%); }
  .song-card:hover {
    transform: translateY(-10px) scale(1.03);
    border-color: #b366ff;
    box-shadow: 0 0 40px #8a2be2, 0 0 80px rgba(138,43,226,0.5);
  }

  .song-title {
    font-size: clamp(1.1rem, 3vw, 1.4rem); font-weight: 900;
    color: #fff; margin-bottom: 15px;
    text-shadow: 0 0 10px #b366ff;
    word-wrap: break-word;
    display: flex; align-items: center; gap: 8px;
  }
  .song-title::before {
    content: '🎵';
    filter: hue-rotate(270deg);
  }

  /* ============ پلیر سفارشی بنفش ============ */
  .custom-player {
    display: flex; flex-direction: column; gap: 14px;
    margin-top: 12px;
  }

  /* ردیف بالا: پلی + نوار پیشرفت + زمان */
  .player-main {
    display: flex; align-items: center; gap: 12px;
  }

  .play-btn {
    flex-shrink: 0;
    width: 48px; height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8a2be2, #b366ff);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 20px rgba(179,102,255,0.6);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
  }
  .play-btn:hover {
    transform: scale(1.08);
    box-shadow: 0 0 30px #b366ff, 0 0 60px #8a2be2;
  }
  .play-btn svg {
    width: 22px; height: 22px;
    fill: #fff;
    margin-right: -2px;
  }
  .play-btn.playing svg.play-icon { display: none; }
  .play-btn:not(.playing) svg.pause-icon { display: none; }

  /* نوار پیشرفت */
  .progress-wrap {
    flex: 1;
    position: relative;
    height: 6px;
    background: rgba(179,102,255,0.2);
    border-radius: 10px;
    cursor: pointer;
    overflow: hidden;
    min-width: 60px;
  }
  .progress-fill {
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #8a2be2, #b366ff);
    border-radius: 10px;
    box-shadow: 0 0 10px #b366ff;
    transition: width 0.1s linear;
    position: relative;
  }
  .progress-fill::after {
    content: '';
    position: absolute;
    right: -6px; top: 50%;
    transform: translateY(-50%);
    width: 12px; height: 12px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 15px #b366ff, 0 0 25px #8a2be2;
    opacity: 0;
    transition: opacity 0.2s;
  }
  .progress-wrap:hover .progress-fill::after { opacity: 1; }

  .time-display {
    flex-shrink: 0;
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    color: #b366ff;
    letter-spacing: 1px;
    min-width: 75px;
    text-align: left;
    direction: ltr;
  }

  /* ردیف پایین: ولوم + دانلود */
  .player-controls {
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
  }

  .volume-wrap {
    display: flex; align-items: center; gap: 8px;
    flex: 1;
    max-width: 200px;
  }
  .volume-icon {
    width: 20px; height: 20px;
    fill: #b366ff;
    flex-shrink: 0;
    cursor: pointer;
    transition: fill 0.2s;
  }
  .volume-icon:hover { fill: #fff; }

  .volume-slider {
    flex: 1;
    -webkit-appearance: none;
    appearance: none;
    height: 4px;
    background: rgba(179,102,255,0.25);
    border-radius: 10px;
    outline: none;
    cursor: pointer;
  }
  .volume-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 14px; height: 14px;
    background: linear-gradient(135deg, #8a2be2, #b366ff);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 10px #b366ff;
    transition: transform 0.2s;
  }
  .volume-slider::-webkit-slider-thumb:hover { transform: scale(1.3); }
  .volume-slider::-moz-range-thumb {
    width: 14px; height: 14px;
    background: linear-gradient(135deg, #8a2be2, #b366ff);
    border: none; border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 10px #b366ff;
  }

  /* دکمه دانلود */
  .download-btn {
    display: flex; align-items: center; gap: 6px;
    padding: 8px 14px;
    background: transparent;
    border: 2px solid #b366ff;
    color: #b366ff;
    border-radius: 20px;
    text-decoration: none;
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    font-size: 0.85rem; font-weight: bold;
    transition: all 0.25s;
    flex-shrink: 0;
  }
  .download-btn:hover {
    background: #b366ff; color: #0a0014;
    box-shadow: 0 0 20px #b366ff;
    transform: scale(1.05);
  }
  .download-btn svg {
    width: 14px; height: 14px;
    fill: currentColor;
  }

  .empty-msg {
    text-align: center; color: #b366ff;
    font-size: clamp(1rem, 3vw, 1.3rem);
    padding: 60px 20px; grid-column: 1/-1;
  }

  /* حلقه‌های نور */
  .light-ring {
    position: absolute;
    border: 2px solid #b366ff;
    border-radius: 50%;
    pointer-events: none;
    animation: ringExpand 2s ease-out infinite;
  }
  @keyframes ringExpand {
    from { width: 0; height: 0; opacity: 1; }
    to { width: 300px; height: 300px; opacity: 0; transform: translate(-50%, -50%); }
  }

  @media (max-width: 600px) {
    #trailer-text { padding: 15px; }
    #loading-bar { bottom: 5%; width: 85%; }
    #enter-btn { bottom: 12%; }
    .time-display { font-size: 0.65rem; min-width: 60px; }
    .play-btn { width: 42px; height: 42px; }
    .download-btn { padding: 6px 10px; font-size: 0.75rem; }
  }

  @supports (-webkit-touch-callout: none) {
    body, #trailer, #main-site { min-height: -webkit-fill-available; }
  }
</style>
</head>
<body>

<!-- کرسر -->
<div id="cursor-ring"></div>
<div id="cursor-dot"></div>

<div id="flash"></div>

<!-- ============ تریلر ============ -->
<div id="trailer">
  <div id="particles"></div>
  <h1 id="trailer-text">🎧 آماده‌ای؟</h1>
  <button id="enter-btn">ورود به فانک لند</button>
  <div id="loading-bar"><div id="loading-fill"></div></div>
  <audio id="trailer-audio" src="/static/audio/tentana.m4a" preload="auto"></audio>
</div>

<!-- ============ صفحه اصلی ============ -->
<div id="main-site">
  <div class="header">
    <h1>FUNK LAND</h1>
    <p>💜 سرزمین فانک 💜</p>
  </div>
  <button id="replay-btn">🔁 پخش دوباره تریلر</button>

  <div class="songs-grid" id="songs-grid">
    {% if songs %}
      {% for song in songs %}
      <div class="song-card" data-src="/static/audio/{{ song.file }}">
        <div class="song-title">{{ song.name }}</div>

        <div class="custom-player">
          <div class="player-main">
            <button class="play-btn" data-action="play" aria-label="پخش">
              <svg class="play-icon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              <svg class="pause-icon" viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>
            </button>

            <div class="progress-wrap">
              <div class="progress-fill"></div>
            </div>

            <div class="time-display">0:00 / 0:00</div>
          </div>

          <div class="player-controls">
            <div class="volume-wrap">
              <svg class="volume-icon" viewBox="0 0 24 24"><path d="M3 10v4h4l5 5V5L7 10H3zm13.5 2c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>
              <input type="range" class="volume-slider" min="0" max="1" step="0.01" value="1">
            </div>

            <a class="download-btn" href="/static/audio/{{ song.file }}" download>
              <svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg>
              دانلود
            </a>
          </div>
        </div>
      </div>
      {% endfor %}
    {% else %}
      <div class="empty-msg">هنوز آهنگی اضافه نشده 🎵</div>
    {% endif %}
  </div>
</div>

<script>
// ==================== کرسر ====================
const cursorDot = document.getElementById('cursor-dot');
const cursorRing = document.getElementById('cursor-ring');
let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;
const isDesktop = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

if (isDesktop) {
  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX; mouseY = e.clientY;
    cursorDot.style.left = mouseX + 'px';
    cursorDot.style.top = mouseY + 'px';
  });
  (function animateRing() {
    ringX += (mouseX - ringX) * 0.18;
    ringY += (mouseY - ringY) * 0.18;
    cursorRing.style.left = ringX + 'px';
    cursorRing.style.top = ringY + 'px';
    requestAnimationFrame(animateRing);
  })();
  function bindHover() {
    document.querySelectorAll('a, button, input, [role="button"], .progress-wrap, .song-card').forEach(el => {
      if (el.dataset.cursorBound) return;
      el.dataset.cursorBound = '1';
      el.addEventListener('mouseenter', () => {
        cursorDot.classList.add('hover');
        cursorRing.classList.add('hover');
      });
      el.addEventListener('mouseleave', () => {
        cursorDot.classList.remove('hover');
        cursorRing.classList.remove('hover');
      });
    });
  }
  bindHover();
  setInterval(bindHover, 2000);
}

// ==================== ذرات ====================
const particlesBox = document.getElementById('particles');
const particleCount = window.innerWidth < 600 ? 30 : 70;
for (let i = 0; i < particleCount; i++) {
  const p = document.createElement('div');
  p.className = 'particle';
  p.style.left = Math.random() * 100 + '%';
  p.style.top = Math.random() * 100 + '%';
  p.style.animationDelay = (Math.random() * 8) + 's';
  p.style.animationDuration = (6 + Math.random() * 6) + 's';
  particlesBox.appendChild(p);
}

// ==================== عناصر تریلر ====================
const enterBtn = document.getElementById('enter-btn');
const trailerText = document.getElementById('trailer-text');
const audio = document.getElementById('trailer-audio');
const loadingFill = document.getElementById('loading-fill');
const trailer = document.getElementById('trailer');
const mainSite = document.getElementById('main-site');
const flash = document.getElementById('flash');
const replayBtn = document.getElementById('replay-btn');

let started = false;

function shakeScreen() {
  document.body.classList.add('shake');
  setTimeout(() => document.body.classList.remove('shake'), 500);
}

function doFlash() {
  flash.style.opacity = '0.8';
  setTimeout(() => flash.style.opacity = '0', 300);
}

function spawnRing(x, y) {
  const ring = document.createElement('div');
  ring.className = 'light-ring';
  ring.style.left = x + 'px';
  ring.style.top = y + 'px';
  ring.style.transform = 'translate(-50%, -50%)';
  document.body.appendChild(ring);
  setTimeout(() => ring.remove(), 2000);
}

function startTrailer() {
  if (started) return;
  started = true;
  enterBtn.style.display = 'none';

  trailer.style.display = 'flex';
  trailer.style.opacity = '1';
  mainSite.style.display = 'none';

  audio.currentTime = 0;
  audio.volume = 0.9;

  audio.play().catch(err => {
    console.log('پخش نشد:', err);
    showMainSite();
    return;
  });

  trailerText.textContent = 'به فانک لند خوش اومدید :)';
  trailerText.classList.remove('glitch');

  const totalSeconds = 25;
  const interval = setInterval(() => {
    const t = audio.currentTime;
    loadingFill.style.width = Math.min((t / totalSeconds) * 100, 100) + '%';
  }, 100);

  setTimeout(() => {
    shakeScreen();
    spawnRing(window.innerWidth / 2, window.innerHeight / 2);
    trailerText.classList.add('glitch');
    setTimeout(() => { trailerText.textContent = 'شاهکارترین سایت فانک'; }, 200);
    setTimeout(() => { trailerText.classList.remove('glitch'); }, 800);
  }, 10000);

  setTimeout(() => {
    clearInterval(interval);
    doFlash();
    setTimeout(() => {
      audio.pause();
      showMainSite();
    }, 300);
  }, 25000);
}

function showMainSite() {
  trailer.style.transition = 'opacity 1s ease';
  trailer.style.opacity = '0';
  setTimeout(() => {
    trailer.style.display = 'none';
    mainSite.style.display = 'block';
    mainSite.style.opacity = '0';
    mainSite.style.transition = 'opacity 1s ease';
    setTimeout(() => mainSite.style.opacity = '1', 50);
  }, 1000);
}

enterBtn.addEventListener('click', startTrailer);
replayBtn.addEventListener('click', () => {
  started = false;
  enterBtn.style.display = 'block';
  startTrailer();
});

setInterval(() => {
  if (trailer.style.display !== 'none' && started) {
    spawnRing(Math.random() * window.innerWidth, Math.random() * window.innerHeight);
  }
}, 1500);

// ==================== پلیر سفارشی ====================
function formatTime(sec) {
  if (isNaN(sec)) return '0:00';
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return m + ':' + (s < 10 ? '0' : '') + s;
}

// هر کارت آهنگ رو وصل کن
document.querySelectorAll('.song-card').forEach(card => {
  const src = card.dataset.src;
  const playBtn = card.querySelector('.play-btn');
  const progressWrap = card.querySelector('.progress-wrap');
  const progressFill = card.querySelector('.progress-fill');
  const timeDisplay = card.querySelector('.time-display');
  const volumeSlider = card.querySelector('.volume-slider');
  const volumeIcon = card.querySelector('.volume-icon');

  const songAudio = new Audio(src);
  songAudio.preload = 'metadata';

  let isDragging = false;

  // پلی/پاز
  playBtn.addEventListener('click', () => {
    if (songAudio.paused) {
      // بقیه رو pause کن
      document.querySelectorAll('.song-card').forEach(c => {
        if (c === card) return;
        const otherAudio = c._audio;
        const otherBtn = c.querySelector('.play-btn');
        if (otherAudio && !otherAudio.paused) {
          otherAudio.pause();
          otherBtn.classList.remove('playing');
        }
      });
      songAudio.play();
      playBtn.classList.add('playing');
    } else {
      songAudio.pause();
      playBtn.classList.remove('playing');
    }
  });

  // ذخیره audio روی card برای دسترسی از بقیه
  card._audio = songAudio;

  // آپدیت پیشرفت
  songAudio.addEventListener('timeupdate', () => {
    if (!isDragging && songAudio.duration) {
      const pct = (songAudio.currentTime / songAudio.duration) * 100;
      progressFill.style.width = pct + '%';
    }
    timeDisplay.textContent = formatTime(songAudio.currentTime) + ' / ' + formatTime(songAudio.duration);
  });

  songAudio.addEventListener('loadedmetadata', () => {
    timeDisplay.textContent = '0:00 / ' + formatTime(songAudio.duration);
  });

  songAudio.addEventListener('ended', () => {
    playBtn.classList.remove('playing');
    progressFill.style.width = '0%';
    timeDisplay.textContent = '0:00 / ' + formatTime(songAudio.duration);
  });

  // کلیک روی نوار پیشرفت
  function seekFromEvent(e) {
    const rect = progressWrap.getBoundingClientRect();
    let x = (e.clientX || e.touches[0].clientX) - rect.left;
    // چون RTL هست، معکوس می‌کنیم
    const pct = Math.max(0, Math.min(1, x / rect.width));
    if (songAudio.duration) {
      songAudio.currentTime = pct * songAudio.duration;
      progressFill.style.width = (pct * 100) + '%';
    }
  }

  progressWrap.addEventListener('mousedown', (e) => {
    isDragging = true;
    seekFromEvent(e);
  });
  document.addEventListener('mousemove', (e) => {
    if (isDragging) seekFromEvent(e);
  });
  document.addEventListener('mouseup', () => { isDragging = false; });

  progressWrap.addEventListener('touchstart', (e) => {
    isDragging = true;
    seekFromEvent(e);
  }, { passive: true });
  progressWrap.addEventListener('touchmove', (e) => {
    if (isDragging) seekFromEvent(e);
  }, { passive: true });
  progressWrap.addEventListener('touchend', () => { isDragging = false; });

  // ولوم
  volumeSlider.addEventListener('input', () => {
    songAudio.volume = parseFloat(volumeSlider.value);
  });

  // کلیک روی آیکون ولوم = قطع/وصل
  let lastVolume = 1;
  volumeIcon.addEventListener('click', () => {
    if (songAudio.volume > 0) {
      lastVolume = songAudio.volume;
      songAudio.volume = 0;
      volumeSlider.value = 0;
    } else {
      songAudio.volume = lastVolume || 1;
      volumeSlider.value = lastVolume || 1;
    }
  });
});
</script>
</body>
</html>
"""

# ================== لاگین ادمین ==================
ADMIN_LOGIN_HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; font-family: 'Vazirmatn', Tahoma, sans-serif; }
  @media (hover: hover) and (pointer: fine) { * { cursor: none !important; } }
  #cursor-dot {
    position: fixed; width: 10px; height: 10px;
    background: #b366ff; border-radius: 50%;
    pointer-events: none; z-index: 99999;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 15px #b366ff, 0 0 30px #8a2be2;
  }
  #cursor-ring {
    position: fixed; width: 40px; height: 40px;
    border: 2px solid #b366ff; border-radius: 50%;
    pointer-events: none; z-index: 99998;
    transform: translate(-50%, -50%);
    background: rgba(179,102,255,0.08);
    box-shadow: 0 0 20px rgba(179,102,255,0.6);
  }
  @media (hover: none), (pointer: coarse) {
    #cursor-dot, #cursor-ring { display: none !important; }
    * { cursor: auto !important; }
  }
  body {
    background: radial-gradient(circle at 50% 50%, #2a0050, #0a0014);
    min-height: 100vh;
    display: flex; justify-content: center; align-items: center;
    color: #fff; padding: 20px;
  }
  .box {
    background: rgba(138,43,226,0.15);
    border: 2px solid #8a2be2;
    border-radius: 20px; padding: 35px;
    width: 100%; max-width: 400px;
    box-shadow: 0 0 50px rgba(138,43,226,0.5);
    backdrop-filter: blur(10px);
  }
  h2 { text-align: center; margin-bottom: 25px; color: #b366ff; }
  input {
    width: 100%; padding: 14px; margin-bottom: 15px;
    background: rgba(0,0,0,0.3); border: 1px solid #8a2be2;
    border-radius: 10px; color: #fff; font-size: 1rem;
    font-family: 'Vazirmatn', Tahoma, sans-serif;
  }
  input:focus { outline: none; border-color: #b366ff; box-shadow: 0 0 15px #8a2be2; }
  button {
    width: 100%; padding: 14px;
    background: linear-gradient(135deg, #8a2be2, #b366ff);
    border: none; border-radius: 10px;
    color: #fff; font-size: 1.1rem; font-weight: bold;
    cursor: pointer; transition: transform 0.2s;
    font-family: 'Vazirmatn', Tahoma, sans-serif;
  }
  button:hover { transform: scale(1.03); box-shadow: 0 0 25px #b366ff; }
  .err { color: #ff5577; text-align: center; margin-bottom: 15px; }
</style>
</head>
<body>
<div id="cursor-ring"></div>
<div id="cursor-dot"></div>
<div class="box">
  <h2>🔒 ورود</h2>
  {% if error %}<div class="err">{{ error }}</div>{% endif %}
  <form method="POST">
    <input type="text" name="username" placeholder="نام کاربری" required>
    <input type="password" name="password" placeholder="رمز عبور" required>
    <button type="submit">ورود</button>
  </form>
</div>
<script>
const cursorDot = document.getElementById('cursor-dot');
const cursorRing = document.getElementById('cursor-ring');
let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;
if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.addEventListener('mousemove', e => {
    mouseX = e.clientX; mouseY = e.clientY;
    cursorDot.style.left = mouseX + 'px';
    cursorDot.style.top = mouseY + 'px';
  });
  (function anim(){
    ringX += (mouseX - ringX) * 0.18;
    ringY += (mouseY - ringY) * 0.18;
    cursorRing.style.left = ringX + 'px';
    cursorRing.style.top = ringY + 'px';
    requestAnimationFrame(anim);
  })();
}
</script>
</body>
</html>
"""

# ================== پنل ادمین ==================
ADMIN_PANEL_HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>پنل مدیریت</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; font-family: 'Vazirmatn', Tahoma, sans-serif; }
  @media (hover: hover) and (pointer: fine) { * { cursor: none !important; } }
  #cursor-dot {
    position: fixed; width: 10px; height: 10px;
    background: #b366ff; border-radius: 50%;
    pointer-events: none; z-index: 99999;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 15px #b366ff, 0 0 30px #8a2be2;
  }
  #cursor-ring {
    position: fixed; width: 40px; height: 40px;
    border: 2px solid #b366ff; border-radius: 50%;
    pointer-events: none; z-index: 99998;
    transform: translate(-50%, -50%);
    background: rgba(179,102,255,0.08);
    box-shadow: 0 0 20px rgba(179,102,255,0.6);
    transition: width 0.25s, height 0.25s, border-color 0.25s;
  }
  @media (hover: none), (pointer: coarse) {
    #cursor-dot, #cursor-ring { display: none !important; }
    * { cursor: auto !important; }
  }
  body {
    background: radial-gradient(circle at 50% 50%, #2a0050, #0a0014);
    min-height: 100vh; color: #fff; padding: 20px;
  }
  h1 { color: #b366ff; margin-bottom: 20px; text-align: center; font-size: clamp(1.3rem, 5vw, 2rem); }
  .container { max-width: 900px; margin: 0 auto; }
  .card {
    background: rgba(138,43,226,0.15);
    border: 2px solid #8a2be2;
    border-radius: 15px; padding: 20px; margin-bottom: 20px;
    backdrop-filter: blur(10px);
  }
  h2 { color: #b366ff; margin-bottom: 15px; font-size: clamp(1rem, 3vw, 1.3rem); }
  input[type=text], input[type=password], input[type=file] {
    width: 100%; padding: 12px;
    background: rgba(0,0,0,0.3); border: 1px solid #8a2be2;
    border-radius: 10px; color: #fff; margin-bottom: 12px;
    font-size: 1rem; font-family: 'Vazirmatn', Tahoma, sans-serif;
  }
  input:focus { outline: none; border-color: #b366ff; box-shadow: 0 0 15px #8a2be2; }
  button {
    padding: 12px 25px;
    background: linear-gradient(135deg, #8a2be2, #b366ff);
    border: none; border-radius: 10px;
    color: #fff; font-weight: bold;
    cursor: pointer; transition: transform 0.2s;
    font-size: 1rem; font-family: 'Vazirmatn', Tahoma, sans-serif;
  }
  button:hover { transform: scale(1.05); box-shadow: 0 0 20px #b366ff; }
  .song-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 12px; background: rgba(0,0,0,0.3);
    border-radius: 10px; margin-bottom: 10px;
    gap: 10px; flex-wrap: wrap;
  }
  .song-row span { flex: 1; min-width: 150px; word-break: break-all; }
  .del-btn { background: #ff3355; padding: 8px 15px; font-size: 0.9rem; }
  .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; gap: 10px; flex-wrap: wrap; }
  .logout {
    background: transparent; border: 2px solid #b366ff;
    text-decoration: none; color: #b366ff;
    padding: 10px 20px; border-radius: 10px;
    transition: all 0.2s;
  }
  .logout:hover { background: #b366ff; color: #0a0014; }
  .msg-ok {
    background: rgba(102,255,153,0.15);
    border: 1px solid #66ff99;
    color: #66ff99; padding: 12px;
    border-radius: 10px; margin-bottom: 15px; text-align: center;
  }
  .msg-err {
    background: rgba(255,85,119,0.15);
    border: 1px solid #ff5577;
    color: #ff5577; padding: 12px;
    border-radius: 10px; margin-bottom: 15px; text-align: center;
  }
  @media (max-width: 600px) {
    body { padding: 12px; }
    .card { padding: 15px; }
    .song-row { flex-direction: column; align-items: stretch; }
    .song-row button { width: 100%; }
  }
</style>
</head>
<body>
<div id="cursor-ring"></div>
<div id="cursor-dot"></div>

<div class="container">
  <div class="top-bar">
    <h1>🎛️ پنل مدیریت</h1>
    <a href="{{ url_for('admin_logout') }}" class="logout">خروج</a>
  </div>

  {% if msg %}<div class="msg-ok">{{ msg }}</div>{% endif %}
  {% if err %}<div class="msg-err">{{ err }}</div>{% endif %}

  <div class="card">
    <h2>➕ افزودن آهنگ</h2>
    <form method="POST" enctype="multipart/form-data" action="{{ url_for('admin_add') }}">
      <input type="text" name="song_name" placeholder="نام آهنگ" required>
      <input type="file" name="song_file" accept="audio/*" required>
      <button type="submit">آپلود</button>
    </form>
  </div>

  <div class="card">
    <h2>🔑 تغییر نام کاربری و رمز عبور</h2>
    <form method="POST" action="{{ url_for('admin_change_pass') }}">
      <input type="text" name="new_username" placeholder="نام کاربری جدید (خالی = بدون تغییر)">
      <input type="password" name="old_password" placeholder="رمز فعلی" required>
      <input type="password" name="new_password" placeholder="رمز جدید (خالی = بدون تغییر)">
      <input type="password" name="new_password2" placeholder="تکرار رمز جدید">
      <button type="submit">ذخیره تغییرات</button>
    </form>
  </div>

  <div class="card">
    <h2>🎵 آهنگ‌ها ({{ songs|length }})</h2>
    {% if songs %}
      {% for song in songs %}
      <div class="song-row">
        <span>{{ song.name }} — <small style="color:#888">{{ song.file }}</small></span>
        <form method="POST" action="{{ url_for('admin_delete', idx=loop.index0) }}">
          <button type="submit" class="del-btn">حذف</button>
        </form>
      </div>
      {% endfor %}
    {% else %}
      <p style="color:#888">هنوز آهنگی اضافه نشده.</p>
    {% endif %}
  </div>
</div>

<script>
const cursorDot = document.getElementById('cursor-dot');
const cursorRing = document.getElementById('cursor-ring');
let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;
if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.addEventListener('mousemove', e => {
    mouseX = e.clientX; mouseY = e.clientY;
    cursorDot.style.left = mouseX + 'px';
    cursorDot.style.top = mouseY + 'px';
  });
  (function anim(){
    ringX += (mouseX - ringX) * 0.18;
    ringY += (mouseY - ringY) * 0.18;
    cursorRing.style.left = ringX + 'px';
    cursorRing.style.top = ringY + 'px';
    requestAnimationFrame(anim);
  })();
  document.querySelectorAll('input, button, a').forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursorRing.style.width = '60px'; cursorRing.style.height = '60px';
      cursorRing.style.borderColor = '#fff';
    });
    el.addEventListener('mouseleave', () => {
      cursorRing.style.width = '40px'; cursorRing.style.height = '40px';
      cursorRing.style.borderColor = '#b366ff';
    });
  });
}
</script>
</body>
</html>
"""

# ================== روت‌ها ==================
@app.route("/")
def home():
    songs = load_songs()
    return render_template_string(MAIN_HTML, songs=songs)

@app.route(ADMIN_PATH, methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_panel"))
    error = None
    if request.method == "POST":
        cfg = load_config()
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        if u == cfg["username"] and p == cfg["password"]:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        error = "نام کاربری یا رمز اشتباهه"
    return render_template_string(ADMIN_LOGIN_HTML, error=error)

@app.route("/managepanel/")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(ADMIN_PATH)
    songs = load_songs()
    return render_template_string(
        ADMIN_PANEL_HTML,
        songs=songs,
        msg=request.args.get("msg"),
        err=request.args.get("err")
    )

@app.route("/admin-add", methods=["POST"])
def admin_add():
    if not session.get("admin_logged_in"):
        return redirect(ADMIN_PATH)
    name = request.form.get("song_name", "").strip()
    file = request.files.get("song_file")
    if name and file and file.filename:
        safe_name = file.filename.replace(" ", "_")
        file.save(os.path.join(AUDIO_DIR, safe_name))
        songs = load_songs()
        songs.append({"name": name, "file": safe_name})
        save_songs(songs)
        return redirect(url_for("admin_panel", msg="آهنگ اضافه شد ✅"))
    return redirect(url_for("admin_panel", err="اطلاعات ناقصه ❌"))

@app.route("/admin-delete/<int:idx>", methods=["POST"])
def admin_delete(idx):
    if not session.get("admin_logged_in"):
        return redirect(ADMIN_PATH)
    songs = load_songs()
    if 0 <= idx < len(songs):
        fpath = os.path.join(AUDIO_DIR, songs[idx]["file"])
        if os.path.exists(fpath):
            try: os.remove(fpath)
            except: pass
        songs.pop(idx)
        save_songs(songs)
        return redirect(url_for("admin_panel", msg="حذف شد ✅"))
    return redirect(url_for("admin_panel", err="پیدا نشد ❌"))

@app.route("/admin-change-pass", methods=["POST"])
def admin_change_pass():
    if not session.get("admin_logged_in"):
        return redirect(ADMIN_PATH)
    cfg = load_config()
    old = request.form.get("old_password", "")
    new_u = request.form.get("new_username", "").strip()
    new_p = request.form.get("new_password", "")
    new_p2 = request.form.get("new_password2", "")
    if old != cfg["password"]:
        return redirect(url_for("admin_panel", err="رمز فعلی اشتباهه ❌"))
    if new_p and new_p != new_p2:
        return redirect(url_for("admin_panel", err="رمز جدید یکسان نیست ❌"))
    if new_u: cfg["username"] = new_u
    if new_p: cfg["password"] = new_p
    save_config(cfg)
    return redirect(url_for("admin_panel", msg="تغییرات ذخیره شد ✅"))

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(ADMIN_PATH)

# ================== اجرا ==================
if __name__ == "__main__":
    print("=" * 50)
    print("🎧 Funk Land v5.0 در حال اجراست...")
    print("🌐 http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
