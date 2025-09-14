# Telegram Video Yuklab Olish Boti Arxitekturasi

## 1. Umumiy ko'rinish

Bot foydalanuvchilardan kelgan xabarlarni tinglab turadi, xabarda video manzili (URL) aniqlansa, `yt-dlp` yordamida videoni yuklab oladi va foydalanuvchiga yuboradi.

## 2. Asosiy komponentlar

### 2.1. Telegram Bot API bilan o'zaro ta'sir

- **Kutubxona**: `python-telegram-bot`
- **Funksiyalar**:
    - `Updater`: Telegramdan yangi xabarlarni doimiy ravishda olish uchun.
    - `Dispatcher`: Turli xil yangiliklarni mos handlers'larga yo'naltirish uchun.
    - `CommandHandler`: `/start` kabi buyruqlarni bajarish uchun.
    - `MessageHandler`: Oddiy matnli xabarlarni (xususan, URL manzillarni) qayta ishlash uchun.

### 2.2. Video yuklab olish moduli

- **Kutubxona**: `yt-dlp` (Python moduli sifatida)
- **Funksiyalar**:
    - `YoutubeDL`: Yuklab olishni sozlash va bajarish uchun asosiy klass.
    - **Xatolarni qayta ishlash**: URL manzil qo'llab-quvvatlanmasa yoki yuklab olishda muammo yuzaga kelsa, ularga eleganza bilan javob berish.

### 2.3. Fayllar bilan ishlash

- **Saqlash**: Foydalanuvchiga yuborishdan oldin videolarni vaqtincha saqlash.
- **Tozalash**: Videoni foydalanuvchiga yuborganidan keyin vaqtincha fayllarni o'chirib tashlash, xotiradan joy tejash maqsadida.

## 3. Ish oqimi

1. Foydalanuvchi botga `/start` buyrug'ini yoki video URL manzilini yuboradi.
2. Bot xabarni `Updater` va `Dispatcher` yordamida qabul qiladi.
3. Agar bu `/start` buyrug'i bo'lsa, bot foydalanuvchiga xush kelibsiz xabarini yuboradi.
4. Agar bu URL manzil bo'lsa, `MessageHandler` URL manzilni ajratib oladi.
5. `yt-dlp` moduli video yuklab olish uchun chaqiriladi.
6. Yuklab olingandan so'ng, bot video faylni foydalanuvchiga yuboradi.
7. Vaqtincha video fayl serverdan o'chirib tashlanadi.

## 4. Xatolarni qayta ishlash

- Agar berilgan URL manzil noto'g'ri yoki qo'llab-quvvatlanmasa, foydalanuvchiga xabar berish.
- Agar yuklab olish jarayonida muammo yuzaga kelsa, foydalanuvchiga xabar berish.
- Agar video fayl Telegram orqali yuborish uchun juda katta bo'lsa, foydalanuvchiga xabar berish (Telegram fayl hajmi cheklovi mavjud).