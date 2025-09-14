# GitHub'ga Loyiha Yuklash Yo'riqnomasi

## 📋 **Kerakli Fayllar va Papkalar**

### ✅ **Asosiy Fayllar (Majburiy)**
```
telegram_video_bot/
├── src/
│   └── bot.py                 # Asosiy bot kodi
├── requirements.txt           # Python kutubxonalari
├── README.md                  # Loyiha haqida ma'lumot
├── .gitignore                 # Git uchun ignore qoidalari
├── LICENSE                    # Litsenziya fayli
└── run_bot.py                 # Botni ishga tushirish skripti
```

### 📁 **Qo'shimcha Fayllar (Ixtiyoriy)**
```
telegram_video_bot/
├── setup.py                   # Python paket sozlamalari
├── setup_bot.py               # Bot sozlash skripti
├── test_bot.py                # Test skripti
├── .env.example               # Muhit o'zgaruvchilari namunasi
└── docs/                      # Hujjatlar papkasi
    ├── INSTALLATION.md
    ├── USAGE.md
    └── TROUBLESHOOTING.md
```

## 🚀 **GitHub'ga Yuklash Qadamlari**

### 1️⃣ **Git Repositoriyasini Ishga Tushirish**
```bash
# Loyiha papkasiga o'ting
cd telegram_video_bot

# Git repositoriyasini ishga tushiring
git init

# Barcha fayllarni qo'shing
git add .

# Birinchi commit yarating
git commit -m "Initial commit: Telegram Video Bot"
```

### 2️⃣ **GitHub Repositoriyasini Yaratish**
1. **GitHub.com** ga kiring
2. **"New repository"** tugmasini bosing
3. **Repository nomi:** `telegram_video_bot`
4. **Description:** "Telegram bot for downloading videos from various platforms"
5. **Public** yoki **Private** tanlang
6. **"Create repository"** tugmasini bosing

### 3️⃣ **Remote Repositoriyani Qo'shish**
```bash
# Remote repositoriyani qo'shing (HTTPS)
git remote add origin https://github.com/USERNAME/telegram_video_bot.git

# Yoki SSH (agar SSH kalit sozlagan bo'lsangiz)
git remote add origin git@github.com:USERNAME/telegram_video_bot.git
```

### 4️⃣ **Kodni GitHub'ga Yuklash**
```bash
# Main branch nomini o'rnating
git branch -M main

# Kodni GitHub'ga yuklang
git push -u origin main
```

## 📝 **README.md Fayli Tarkibi**

### **Majburiy Bo'limlar:**
```markdown
# Telegram Video Download Bot

**Muallif:** N.Damir - Senior Dasturchi

## Tavsif
Bot turli platformalardan videolarni yuklab oladi.

## O'rnatish
1. Python 3.9+ o'rnating
2. `pip install -r requirements.txt`
3. `.env` faylini yarating

## Ishlatish
```bash
python run_bot.py
```

## Qo'llab-quvvatlanadigan platformalar
- YouTube, Instagram, TikTok, va boshqalar

## Litsenziya
MIT
```

## 🔧 **.gitignore Fayli Tarkibi**

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/

# Environment
.env
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Bot specific
downloads/
*.mp4
*.avi
*.mkv
logs/
```

## 📋 **requirements.txt Tarkibi**

```txt
python-telegram-bot>=22.0
yt-dlp>=2025.0.0
python-dotenv>=1.0.0
```

## 🔐 **.env.example Fayli**

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Video Download Settings
MAX_VIDEO_DURATION=600
MAX_VIDEO_SIZE=52428800
DOWNLOAD_DIR=downloads

# Logging Settings
LOG_LEVEL=INFO
```

## ⚠️ **Muhim Eslatmalar**

### **Hech qachon GitHub'ga yuklamang:**
- ❌ `.env` fayli (bot tokeni)
- ❌ `downloads/` papkasi
- ❌ `__pycache__/` papkalari
- ❌ Shaxsiy ma'lumotlar
- ❌ Katta media fayllar

### **Majburiy Tekshiruvlar:**
1. ✅ Bot tokeni `.env` faylida
2. ✅ Barcha kerakli kutubxonalar `requirements.txt` da
3. ✅ README.md to'liq va tushunarli
4. ✅ .gitignore to'g'ri sozlangan
5. ✅ Kod ishlaydi va test qilingan

## 🎯 **Yakuniy Checklist**

- [ ] Git repositoriyasi ishga tushirilgan
- [ ] Barcha kerakli fayllar mavjud
- [ ] README.md to'liq yozilgan
- [ ] .gitignore sozlangan
- [ ] requirements.txt to'g'ri
- [ ] .env.example yaratilgan
- [ ] Kod test qilingan
- [ ] GitHub repositoriyasi yaratilgan
- [ ] Remote qo'shilgan
- [ ] Kod yuklangan

## 🚀 **Avtomatik Yuklash Skripti**

Windows uchun:
```batch
@echo off
git add .
git commit -m "Update: %date% %time%"
git push origin main
echo Kod GitHub'ga yuklandi!
pause
```

Linux/Mac uchun:
```bash
#!/bin/bash
git add .
git commit -m "Update: $(date)"
git push origin main
echo "Kod GitHub'ga yuklandi!"
```

## 📞 **Yordam**

Agar muammo yuz bersa:
1. Git holatini tekshiring: `git status`
2. Remote repositoriyani tekshiring: `git remote -v`
3. Loglarni ko'ring: `git log --oneline`
4. GitHub'da Issues oching

---
**Muallif:** N.Damir - Senior Dasturchi  
**Sana:** 2025-yil  
**Versiya:** 1.0.0
