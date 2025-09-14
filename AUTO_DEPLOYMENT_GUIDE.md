# Avtomatik Gitga Yuklash Qo'llanmasi

Ushbu hujjat Telegram Video Bot loyihasini Git repositoriyasiga avtomatik tarzda yuklash bo'yicha to'liq ko'rsatmalarni o'z ichiga oladi.

## Kirish

Telegram Video Bot loyihasi endi to'liq tayyor va Gitga yuklanishga tayyor. Ushbu qo'llanma orqali siz loyihani avtomatik tarzda Git repositoriyasiga yuklashingiz mumkin.

## Talablarni Tekshirish

1. Git o'rnatilganligini tekshiring:
   ```bash
   git --version
   ```

2. Internet ulanishi mavjudligini tekshiring

## Avtomatik Deployment Qadam-qadamlar

### 1. Yangi GitHub/GitLab Repositoriyasini Yaratish

1. GitHub yoki GitLab saytiga kiring
2. "New repository" tugmasini bosing
3. Repositoriya nomini kiriting (masalan: `telegram-video-bot`)
4. Ommaviy (public) yoki shaxsiy (private) tanlang
5. "Create repository" tugmasini bosing

### 2. Mahalliy Repositoriyani Sozlash

Terminalni oching va quyidagi buyruqlarni bajaring:

```bash
# Loyiha katalogiga o'ting
cd F:\linkyukla\telegram_video_bot

# Git repositoriyasini ishga tushiring (agar hali bajarilmagan bo'lsa)
git init

# Barcha fayllarni qo'shing
git add .

# Dastlabki commitni yarating
git commit -m "Initial commit: Complete Telegram Video Bot"
```

### 3. Masofaviy Repositoriyani Ulash

GitHub uchun:
```bash
git remote add origin https://github.com/sizning-foydalanuvchi-nomingiz/telegram-video-bot.git
```

GitLab uchun:
```bash
git remote add origin https://gitlab.com/sizning-foydalanuvchi-nomingiz/telegram-video-bot.git
```

### 4. Kodni Yuklash

```bash
# Asosiy shaxani (main) yaratish (agar kerak bo'lsa)
git branch -M main

# Kodni masofaviy repositoriyaga yuklash
git push -u origin main
```

## Windows uchun Avtomatik Deployment

Loyiha katalogida joylashgan `deploy.ps1` skriptidan foydalaning:

1. PowerShell ni administrator huquqlari bilan oching
2. Quyidagi buyruqni bajaring:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. `deploy.ps1` skriptini ishga tushiring:
   ```powershell
   .\deploy.ps1
   ```

## Linux/Mac uchun Avtomatik Deployment

Loyiha katalogida joylashgan `deploy.py` skriptidan foydalaning:

```bash
python deploy.py
```

## Task Scheduler orqali Avtomatik Yangilash (Windows)

1. Task Scheduler ni oching
2. "Create Basic Task" ni tanlang
3. Vazifa nomini kiriting (masalan: "Telegram Bot Auto Deploy")
4. Trigger tanlang (masalan: har kuni)
5. Action sifatida "Start a program" ni tanlang
6. Program/script maydoniga PowerShell manzilini kiriting
7. Add arguments maydoniga quyidagini kiriting:
   ```
   -ExecutionPolicy Bypass -File "F:\linkyukla\telegram_video_bot\deploy.ps1"
   ```
8. "Finish" tugmasini bosing

## Cron orqali Avtomatik Yangilash (Linux/Mac)

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

## Muhim Fayllar Ro'yxati

Quyidagi fayllar Git repositoriyasiga kiritilishi kerak:

- `src/bot.py` - Asosiy bot kodi
- `run_bot.py` - Botni ishga tushirish skripti
- `requirements.txt` - Python bog'liqliklari
- `README.md` - Loyiha tavsifi
- `DEPLOYMENT.md` - Deployment qo'llanmasi
- `PROJECT_SUMMARY.md` - Loyiha xulosasi
- `.env.example` - Konfiguratsiya fayli namunasi
- `.gitignore` - Git tomonidan e'tiborga olinmaydigan fayllar
- `deploy.py` - Python deployment skripti
- `deploy.ps1` - PowerShell deployment skripti

Quyidagi fayllar Git repositoriyasiga kiritilmasligi kerak:

- `.env` - Maxfiy sozlamalar (agar mavjud bo'lsa)
- `downloads/` - Yuklab olingan fayllar
- `__pycache__/` - Python bytecode keshi
- `*.pyc` - Python bytecode fayllari

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

## Yakun

Telegram Video Bot loyihasi endi to'liq tayyor va Gitga yuklanishga tayyor. Ushbu qo'llanma orqali siz loyihani osongina Git repositoriyasiga yuklashingiz va avtomatik tarzda yangilashingiz mumkin.

Agar qo'shimcha savollaringiz bo'lsa, [DEPLOYMENT.md](DEPLOYMENT.md) fayliga murojaat qiling.