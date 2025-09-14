# Avtomatik Deployment Qo'llanmasi

Ushbu hujjat Telegram Video Bot loyihasini avtomatik tarzda Gitga yuklash bo'yicha to'liq ko'rsatmalarni o'z ichiga oladi.

## Kirish

Telegram Video Bot loyihasi endi to'liq tayyor va avtomatik tarzda Gitga yuklanish uchun tayyor. Ushbu qo'llanma orqali siz loyihani bir necha usullar bilan avtomatik tarzda Gitga yuklashingiz mumkin.

## Mavjud Avtomatik Deployment Usullari

Loyiha quyidagi avtomatik deployment usullarini o'z ichiga oladi:

1. **setup_and_deploy.py** - Python skripti (barcha platformalar uchun)
2. **deploy.ps1** - PowerShell skripti (Windows uchun)
3. **deploy.py** - Oddiy Python deployment skripti (Linux/Mac uchun)
4. **auto_deploy.bat** - Batch fayli (Windows uchun)

## 1. setup_and_deploy.py - To'liq avtomatik yechim

Bu eng to'liq yechim bo'lib, quyidagilarni bajaradi:
- Kerakli dasturiy ta'minotni tekshiradi
- .env faylini yaratadi
- Bog'liqliklarni o'rnatadi
- Git repositoriyasini sozlaydi
- Fayllarni qo'shadi va commit qiladi
- Masofaviy repositoriyani sozlaydi
- O'zgarishlarni yuklaydi

### Ishga tushirish:

```bash
python setup_and_deploy.py
```

## 2. deploy.ps1 - PowerShell skripti (Windows)

Windows foydalanuvchilari uchun mo'ljallangan. Quyidagilarni bajaradi:
- Git o'rnatilganligini tekshiradi
- Fayllarni qo'shadi va commit qiladi
- O'zgarishlarni masofaviy repositoriyaga yuklaydi

### Ishga tushirish:

```powershell
.\deploy.ps1
```

Yoki PowerShell ni administrator huquqlari bilan ochib, quyidagilarni bajaring:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy.ps1
```

## 3. deploy.py - Python skripti (Linux/Mac)

Linux va Mac foydalanuvchilari uchun mo'ljallangan. Quyidagilarni bajaradi:
- Git o'rnatilganligini tekshiradi
- Fayllarni qo'shadi va commit qiladi
- O'zgarishlarni masofaviy repositoriyaga yuklaydi

### Ishga tushirish:

```bash
python deploy.py
```

## 4. auto_deploy.bat - Batch fayli (Windows)

Windows foydalanuvchilari uchun eng oddiy usul. Quyidagilarni bajaradi:
- Git o'rnatilganligini tekshiradi
- Fayllarni qo'shadi va commit qiladi
- O'zgarishlarni masofaviy repositoriyaga yuklaydi

### Ishga tushirish:

Faylni ikki marta bosish yoki command line'da quyidagilarni bajaring:

```cmd
auto_deploy.bat
```

## Batafsil Qadam-qadamlar

### 1. Dastlabki Talablarni Tekshirish

Kerakli dasturiy ta'minot o'rnatilganligini tekshiring:

1. **Python 3.7+**
   ```bash
   python --version
   ```

2. **Git**
   ```bash
   git --version
   ```

3. **pip**
   ```bash
   pip --version
   ```

### 2. .env Faylini Sozlash

Telegram bot tokenini oling:

1. Telegramda @BotFather ga kiring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Foydalanuvchi nomini kiriting
5. Olingan tokeni nusxalang

.env faylini yarating:

```bash
# .env faylga quyidagilarni kiriting
TELEGRAM_BOT_TOKEN=123456789:ABCDEF-ghijklmnopqrstuvwxyz1234567890
MAX_VIDEO_DURATION=600
MAX_VIDEO_SIZE=52428800
DOWNLOAD_DIR=downloads
LOG_LEVEL=INFO
```

### 3. Bog'liqliklarni O'rnatish

```bash
pip install -r requirements.txt
```

### 4. Git Repositoriyasini Sozlash

Agar Git repositoriyasi hali yaratilmagan bo'lsa:

```bash
# Git repositoriyasini ishga tushirish
git init

# Barcha fayllarni qo'shish
git add .

# Dastlabki commit
git commit -m "Initial commit: Telegram Video Bot"
```

### 5. Masofaviy Repositoriyani Ulash

GitHub uchun:
```bash
git remote add origin https://github.com/sizning-foydalanuvchi-nomingiz/telegram-video-bot.git
```

GitLab uchun:
```bash
git remote add origin https://gitlab.com/sizning-foydalanuvchi-nomingiz/telegram-video-bot.git
```

### 6. Branch Nomini O'rnatish

```bash
git branch -M main
```

### 7. O'zgarishlarni Yuklash

```bash
git push -u origin main
```

## Avtomatik Yangilashni Rejalashtirish

### Windows - Task Scheduler

1. Task Scheduler ni oching
2. "Create Basic Task" ni tanlang
3. Vazifa nomini kiriting (masalan: "Telegram Bot Auto Deploy")
4. Trigger tanlang (masalan: har kuni)
5. Action sifatida "Start a program" ni tanlang
6. Program/script maydoniga quyidagini kiriting:
   ```
   C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
   ```
7. Add arguments maydoniga quyidagini kiriting:
   ```
   -ExecutionPolicy Bypass -File "F:\linkyukla\telegram_video_bot\deploy.ps1"
   ```
8. "Finish" tugmasini bosing

### Linux/Mac - Cron

Cron job yaratish:

```bash
# Cron jobni tahrirlash
crontab -e

# Har kuni soat 2:00 (UTC) da yangilanish uchun quyidagi qatorni qo'shing
0 2 * * * cd /path/to/telegram_video_bot && python deploy.py
```

## GitHub Actions orqali CI/CD

Agar siz GitHub ishlatayotgan bo'lsangiz, quyidagi faylni yarating:

`.github/workflows/deploy.yml`

```yaml
name: Deploy Telegram Bot

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Har kuni soat 2:00 (UTC) da

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python test_bot.py
        
    - name: Deploy
      run: |
        echo "Deployment completed successfully"
```

## Xavfsizlik Eslatmasi

1. `.env` faylini hech qachon Gitga yuklamang
2. Bot tokenini xavfsiz saqlang
3. Private repositorylardan foydalaning agar loyiha shaxsiy bo'lsa

## Muammolarni Bartaraf Etiш

### "Permission denied (publickey)" xatosi

SSH kalitini yaratish va GitHub hisobingizga qo'shing:

```bash
# SSH kalitini yaratish
ssh-keygen -t ed25519 -C "sizning_email@example.com"

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

## Qo'shimcha Resurslar

1. [DEPLOYMENT.md](DEPLOYMENT.md) - Batafsil deployment qo'llanmasi
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Loyiha xulosasi
3. [AUTO_DEPLOYMENT_GUIDE.md](AUTO_DEPLOYMENT_GUIDE.md) - Avtomatik deployment qo'llanmasi

## Yakun

Telegram Video Bot loyihasi endi to'liq tayyor va avtomatik tarzda Gitga yuklanish uchun tayyor. Ushbu qo'llanma orqali siz loyihani osongina Gitga yuklashingiz va avtomatik tarzda yangilashingiz mumkin.