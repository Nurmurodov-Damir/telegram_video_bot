# Telegram Video Bot - Deployment Guide

Ushbu hujjat Telegram Video Bot loyihasini Git repositoriyasiga avtomatik tarzda yuklash bo'yicha to'liq ko'rsatmalarni o'z ichiga oladi.

## Dastlabki talablarni tekshirish

1. Git o'rnatilganligini tekshiring:
   ```bash
   git --version
   ```

2. Python 3.9+ o'rnatilganligini tekshiring:
   ```bash
   python --version
   ```

## Loyihani Gitga yuklash

### 1. Git repositoriyasini yaratish

GitHub, GitLab yoki boshqa Git xosting servisida yangi repositoriya yarating.

### 2. Mahalliy repositoriyani sozlash

```bash
# Loyiha katalogiga o'ting
cd telegram_video_bot

# Git repositoriyasini ishga tushiring (agar hali bajarilmagan bo'lsa)
git init

# Barcha fayllarni qo'shing
git add .

# Dastlabki commitni yarating
git commit -m "Initial commit: Complete Telegram Video Bot implementation"
```

### 3. Masofaviy repositoriyani qo'shish

```bash
# GitHub uchun (sizning foydalanuvchi nomingiz va repositoriya nomingiz bilan almashtiring)
git remote add origin https://github.com/yourusername/telegram-video-bot.git

# Yoki GitLab uchun
git remote add origin https://gitlab.com/yourusername/telegram-video-bot.git
```

### 4. Kodni masofaviy repositoriyaga yuklash

```bash
# Asosiy shaxani (main) yaratish (agar kerak bo'lsa)
git branch -M main

# Kodni GitHub/GitLab'ga yuklash
git push -u origin main
```

## Avtomatik deployment uchun cron job yaratish (Linux/Mac)

Loyihani avtomatik tarzda yangilash uchun cron job yaratishingiz mumkin:

```bash
# Cron jobni tahrirlash
crontab -e

# Har kuni soat 2:00 (UTC) da yangilanish uchun quyidagi qatorni qo'shing
0 2 * * * cd /path/to/telegram_video_bot && git add . && git commit -m "Daily auto-update" && git push origin main
```

## Windows uchun avtomatik deployment

Windowsda quyidagi PowerShell skriptidan foydalanishingiz mumkin:

```powershell
# deploy.ps1
cd "F:\linkyukla\telegram_video_bot"
git add .
git commit -m "Auto-deploy $(Get-Date)"
git push origin main
```

Task Scheduler yordamida bu skriptni rejalashtirishingiz mumkin.

## CI/CD uchun GitHub Actions (agar GitHub ishlatilsa)

`.github/workflows/deploy.yml` faylini yarating:

```yaml
name: Deploy Telegram Bot

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python test_bot.py
        
    - name: Deploy to server
      run: |
        # Deploy komandalari bu yerga
        echo "Deploying to server..."
```

## Muammolarni bartaraf etish

### "Permission denied (publickey)" xatosi

SSH kalitini yaratish va GitHub hisobingizga qo'shish kerak:

```bash
# SSH kalitini yaratish
ssh-keygen -t ed25519 -C "your_email@example.com"

# Kalitni ssh-agent ga qo'shish
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# GitHub hisobingizga kalitni qo'shing (https://github.com/settings/keys)
```

### "Updates were rejected" xatosi

Masofaviy o'zgarishlar mahalliy o'zgarishlardan oldin bo'lsa:

```bash
# O'zgarishlarni sinxronizatsiya qilish
git pull origin main

# Konfliktlarni hal qilish

# O'zgarishlarni qayta yuklash
git add .
git commit -m "Resolve conflicts"
git push origin main
```

## Muhim fayllar

Quyidagi fayllar Git repositoriyasiga kiritilishi kerak:

- `src/bot.py` - Asosiy bot kodi
- `run_bot.py` - Botni ishga tushirish skripti
- `requirements.txt` - Python bog'liqliklari
- `README.md` - Loyiha tavsifi
- `.env.example` - Konfiguratsiya fayli namunasi
- `.gitignore` - Git tomonidan e'tiborga olinmaydigan fayllar

Quyidagi fayllar Git repositoriyasiga kiritilmasligi kerak:

- `.env` - Maxfiy sozlamalar
- `downloads/` - Yuklab olingan fayllar
- `__pycache__/` - Python bytecode keshi
- `*.pyc` - Python bytecode fayllari

## Yangilanishlarni kuzatish

Loyiha yangilanishlarini kuzatish uchun quyidagi buyruqlardan foydalaning:

```bash
# Oxirgi o'zgarishlarni ko'rish
git log --oneline -n 10

# O'zgarishlarni ko'rish
git diff HEAD~1

# Branch holatini tekshirish
git status
```