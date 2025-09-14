# Telegram Video Download Bot

Ushbu Telegram bot foydalanuvchilarga URL manzilini yuborish orqali turli platformalardan videolarni yuklab olish imkonini beradi.

## Xususiyatlari

- YouTube, Vimeo, Twitter, Instagram, TikTok va minglab boshqa saytlardan video yuklab olish
- Telegram orqali video yuborish
- Video davomiyligi va hajmi cheklovlari
- Foydalanuvchi uchun qulay interfeys
- Mover.uz kabi saytlar uchun maxsus xatolar

## Talablarni o'rnatish

1. Python 3.9 yoki yuqori versiyasini o'rnating
2. Kerakli kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```

## Sozlash

1. `.env` faylini yarating va quyidagi o'zgaruvchilarni sozlang:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   MAX_VIDEO_DURATION=600
   MAX_VIDEO_SIZE=52428800
   DOWNLOAD_DIR=downloads
   LOG_LEVEL=INFO
   ```

2. `your_telegram_bot_token_here` ni haqiqiy Telegram bot tokeni bilan almashtiring.

## Botni ishga tushirish

```bash
python run_bot.py
```

Yoki bevosita:

```bash
python src/bot.py
```

## Avtomatik Gitga Yuklash

Loyihani avtomatik tarzda Gitga yuklash uchun quyidagi usullardan birini ishlating:

### Windows uchun

1. `deploy.ps1` skriptini ishga tushiring:
   ```powershell
   .\deploy.ps1
   ```

2. Yoki `auto_deploy.bat` faylini ikki marta bosing

### Linux/Mac uchun

1. `deploy.py` skriptini ishga tushiring:
   ```bash
   python deploy.py
   ```

2. Yoki `setup_and_deploy.py` skriptini ishga tushiring:
   ```bash
   python setup_and_deploy.py
   ```

## Qo'llab-quvvatlanadigan platformalar

- YouTube
- Vimeo
- Twitter
- Instagram
- TikTok
- Va minglab boshqa saytlar

## Cheklovlar

- Telegram cheklovlari tufayli faqat 50MB gacha bo'lgan videolar yuboriladi
- 10 daqiqadan ortiq videolar yuklab olinmaydi

## Xatoliklarni tuzatish

### "ModuleNotFoundError"

Talablarni o'rnating:
```bash
pip install -r requirements.txt
```

### "TELEGRAM_BOT_TOKEN not found"

`.env` faylining mavjudligini va to'g'ri sozlanganligini tekshiring.

## Litsenziya

MIT Litsenziya