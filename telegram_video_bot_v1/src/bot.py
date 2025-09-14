#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Yuklab Olish Boti
Ushbu bot foydalanuvchilarga URL manzilini yuborish orqali turli platformalardan videolarni yuklab olish imkonini beradi.
"""

import logging
import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

import yt_dlp

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Jurnalni yoqish
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Agar yuklab olish katalogi mavjud bo'lmasa, yaratish
DOWNLOADS_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

# Foydalanuvchi so'rovlarini saqlash (kelajakda ishlatish uchun)
# user_requests = {}

# Buyruq handlerlarini belgilash
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi /start buyrug'ini yuborganida xabar yuborish."""
    user = update.effective_user
    if user:
        welcome_message = (
            f"[+] Salom {user.first_name}!\n\n"
            "Men turli platformalardan videolarni yuklab olishga yordam beradigan video yuklab olish botiman.\n\n"
            "[*] Menga video URL manzilini yuboring va men uni siz uchun yuklab olaman.\n"
            "[*] Qo'llab-quvvatlanadigan platformalar: YouTube, Vimeo, Twitter, Instagram, TikTok va minglab boshqalar!\n\n"
            "[!] Eslatma: Telegram cheklovlari tufayli men faqat 50MB gacha bo'lgan videolarni yuklab olaman.\n\n"
            "_Dastur muallifi: N.Damir - Senior Dasturchi_"
        )
        if update.message:
            await update.message.reply_text(welcome_message, parse_mode='Markdown')
    else:
        if update.message:
            await update.message.reply_text("Foydalanuvchi ma'lumotlarini olish imkonsiz.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi /help buyrug'ini yuborganida xabar yuborish."""
    help_text = (
        "[*] Video Yuklab Olish Boti Yordami\n\n"
        "Men turli platformalardan videolarni yuklab olishga yordam beraman.\n\n"
        "[*] Foydalanish tartibi:\n"
        "1. Menga yuklab olmoqchi bo'lgan videoning URL manzilini yuboring\n"
        "2. Men qayta ishlash va videoni yuborishimni kuting\n\n"
        "[*] Qo'llab-quvvatlanadigan platformalar:\n"
        "• YouTube\n"
        "• Vimeo\n"
        "• Twitter\n"
        "• Instagram\n"
        "• TikTok\n"
        "• Va minglab boshqalar!\n\n"
        "[!] Cheklovlar:\n"
        "• 50MB dan ortiq videolar Telegram orqali yuborilmaydi\n"
        "• Ba'zi saytlar yuklab olishni cheklaydi\n\n"
        "[*] Buyruqlar:\n"
        "/start - Botni ishga tushirish\n"
        "/help - Ushbu yordam xabarini ko'rsatish\n"
        "/about - Bot haqida ma'lumot"
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot haqida ma'lumot yuborish."""
    about_text = (
        "[*] Video Yuklab Olish Boti\n\n"
        "Ushbu bot turli platformalardan videolarni bevosita Telegramga yuklab olish imkonini beradi.\n\n"
        "[*] Yaratilgan texnologiyalar:\n"
        "• python-telegram-bot\n"
        "• yt-dlp\n\n"
        "[*] Ishlab chiquvchi:\n"
        "N.Damir - Senior Dasturchi\n\n"
        "[*] Maxfiylik:\n"
        "Hech qanday video yoki shaxsiy ma'lumot serverlarimizda saqlanmaydi.\n"
        "Barcha qayta ishlash vaqtinchalik amalga oshiriladi va fayllar yuborilgandan so'ng o'chirib tashlanadi."
    )
    if update.message:
        await update.message.reply_text(about_text, parse_mode='Markdown')

# ProgressLogger sinfi olib tashlandi - ishlatilmayapti

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """URL manzildan video yuklab olish va foydalanuvchiga yuborish."""
    if not update.message or not update.message.text:
        return
        
    url = update.message.text
    user = update.effective_user
    
    if not user:
        await update.message.reply_text("Foydalanuvchi ma'lumotlarini olish imkonsiz.")
        return
        
    logger.info(f"Foydalanuvchi {user.first_name} ({user.id}) quyidagi uchun yuklab olishni so'radi: {url}")
    
    # Boshlang'ich xabar yuborish
    progress_message = await update.message.reply_text("[*] So'rovingiz qayta ishlanmoqda...")
    
    try:
        # yt-dlp opsiyalarini sozlash
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOADS_DIR, f'{user.id}_%(title)s.%(ext)s'),
            'format': 'best[height<=720][filesize<50M]/best[filesize<50M]/best',  # More flexible format selection
            # Instagram uchun maxsus sozlamalar
            'extractor_args': {
                'instagram': {
                    'api': 'web',
                    'include_ads': False,
                    'include_paid_promotion': False,
                }
            },
            # Instagram uchun qo'shimcha sozlamalar
            # 'cookiesfrombrowser': ['chrome', 'firefox', 'edge'],  # Browser cookies o'chirildi - keyring muammosi tufayli
            'sleep_interval': 1,  # So'rovlar orasida 1 soniya kutish
            'max_sleep_interval': 5,  # Maksimal kutish vaqti
        }
        
        # FFmpeg mavjudligini tekshirish va opsiyalar qo'shish
        import shutil
        if shutil.which('ffmpeg'):
            ydl_opts['format'] = 'best[height<=720][filesize<50M]+bestaudio/best[filesize<50M]/best'
        else:
            logger.warning("FFmpeg not found. The downloaded format may not be the best available.")
        
        # Instagram uchun qo'shimcha format sozlamalari
        if 'instagram.com' in url or 'instagr.am' in url:
            ydl_opts['format'] = 'best[height<=720]/best[height<=480]/best'
            ydl_opts['writesubtitles'] = False
            ydl_opts['writeautomaticsub'] = False
            # Browser cookies o'chirildi - keyring muammosi tufayli
            # ydl_opts['cookiesfrombrowser'] = ['chrome', 'firefox', 'edge']
        
        # Jarayonni yangilash
        await progress_message.edit_text("[*] Video tahlil qilinmoqda...")
        
        # Avval video ma'lumotlarini olish
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            # info_dict None bo'lishi mumkin, shu sababli tekshirish kerak
            if info_dict is None:
                await progress_message.edit_text(
                    "[!] Kechirasiz, men bu videoni tahlil qila olmadim.\n"
                    "Iltimos, URL manzil to'g'ri ekanligini tekshiring."
                )
                return
                
            video_title = info_dict.get('title', 'video')
            video_duration = info_dict.get('duration', 0)
            
            # Agar video juda uzun bo'lsa (10 daqiqadan ortiq)
            max_duration = int(os.getenv("MAX_VIDEO_DURATION", "600"))  # 10 daqiqa soniyalarda
            if video_duration > max_duration:
                await progress_message.edit_text(
                    f"[!] Kechirasiz, men {max_duration // 60} daqiqadan ortiq videolarni yuklab ololmayman.\n"
                    f"Video davomiyligi: {video_duration // 60} daqiqa"
                )
                return
        
        # Jarayonni yangilash
        await progress_message.edit_text("[*] Video yuklab olinmoqda...")
        
        # Videoni yuklab olish
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info_dict)
        
        # Fayl mavjudligini tekshirish
        if not os.path.exists(video_filename):
            await progress_message.edit_text(
                "[!] Kechirasiz, men videoni yuklab ololmadim.\n"
                "Fayl yaratilmadi."
            )
            return
        
        # Fayl hajmini tekshirish
        file_size = os.path.getsize(video_filename)
        max_size = int(os.getenv("MAX_VIDEO_SIZE", "52428800"))  # 50MB baytlarda
        if file_size > max_size:
            os.remove(video_filename)  # Tozalash
            await progress_message.edit_text(
                f"[!] Kechirasiz, video fayl juda katta ({file_size / (1024*1024):.1f}MB).\n"
                f"Telegram faqat {max_size / (1024*1024):.0f}MB gacha fayllarni yuborishga ruxsat beradi."
            )
            return
        
        await progress_message.edit_text("[*] Video Telegramga yuklanmoqda...")
        
        # Foydalanuvchiga video yuborish
        with open(video_filename, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"[+] {video_title}",
                supports_streaming=True
            )
        
        # Yuklab olingan faylni tozalash
        os.remove(video_filename)
        
        await progress_message.edit_text("[*] Video muvaffaqiyatli yuborildi!")
        
    except yt_dlp.DownloadError as e:
        logger.error(f"Yuklab olish xatosi: {str(e)}")
        error_msg = str(e)
        if 'Unsupported URL' in error_msg:
            # Maxsus xabar Mover.uz uchun
            if 'mover.uz' in url:
                await progress_message.edit_text(
                    "[!] Kechirasiz, men Mover.uz saytidan video yuklab olishni qo'llab-quvvatlamayman.\n"
                    "Mover.uz saytida video yuklab olish uchun ularning o'zlarining dasturidan foydalaning.\n\n"
                    "Men YouTube, Vimeo, Twitter, Instagram, TikTok va boshqa saytlarni qo'llab-quvvatlayman."
                )
            else:
                await progress_message.edit_text(
                    "[!] Kechirasiz, men bu saytdan yuklab olishni qo'llab-quvvatlamayman.\n"
                    "Men YouTube, Vimeo, Twitter, Instagram, TikTok va minglab boshqa saytlarni qo'llab-quvvatlayman."
                )
        elif 'HTTP Error 403' in error_msg:
            if 'instagram.com' in url or 'instagr.am' in url:
                await progress_message.edit_text(
                    "[!] Instagram video yuklab olishda kirish rad etildi.\n"
                    "Bu Instagram'ning xavfsizlik siyosati tufayli bo'lishi mumkin.\n"
                    "Iltimos, quyidagilarni sinab ko'ring:\n"
                    "• Video ochiq ekanligini tekshiring\n"
                    "• Video egasi tomonidan cheklangan bo'lishi mumkin\n"
                    "• Bir necha daqiqa kutib, qayta urinib ko'ring"
                )
            else:
                await progress_message.edit_text(
                    "[!] Ushbu videoga kirish rad etildi. U shaxsiy yoki mintaqaviy cheklangan bo'lishi mumkin."
                )
        elif 'Requested format is not available' in error_msg:
            # Instagram uchun maxsus xabar
            if 'instagram.com' in url or 'instagr.am' in url:
                await progress_message.edit_text(
                    "[!] Instagram video yuklab olishda muammo yuz berdi.\n"
                    "Bu Instagram'ning cheklovlari tufayli bo'lishi mumkin.\n"
                    "Iltimos, quyidagilarni sinab ko'ring:\n"
                    "• Video ochiq ekanligini tekshiring\n"
                    "• Bir necha daqiqa kutib, qayta urinib ko'ring\n"
                    "• Boshqa Instagram video manzilini sinab ko'ring"
                )
            else:
                await progress_message.edit_text(
                    "[!] Ushbu video uchun so'ralgan format mavjud emas.\n"
                    "Bu ba'zi ijtimoiy tarmoq platformalarida yuzaga keladi.\n"
                    "Iltimos, boshqa video manzilini yuboring."
                )
        elif 'unsupported keyring' in error_msg:
            # Browser keyring xatosi uchun maxsus xabar
            await progress_message.edit_text(
                "[!] Browser cookies bilan bog'liq muammo yuz berdi.\n"
                "Bu Windows tizimida browser keyring qo'llab-quvvatlanmasligi tufayli.\n\n"
                "[*] Yechim:\n"
                "• Cookies sozlamalari o'chirildi\n"
                "• Video ochiq ekanligini tekshiring\n"
                "• Bir necha daqiqa kutib, qayta urinib ko'ring\n"
                "• Boshqa video manzilini sinab ko'ring"
            )
        elif 'instagram.com' in url or 'instagr.am' in url:
            # Instagram uchun umumiy xato xabari
            await progress_message.edit_text(
                "[!] Instagram video yuklab olishda muammo yuz berdi.\n"
                "Bu Instagram'ning cheklovlari tufayli bo'lishi mumkin.\n\n"
                "[*] Yechimlar:\n"
                "• Video ochiq ekanligini tekshiring\n"
                "• Video egasi tomonidan cheklangan bo'lishi mumkin\n"
                "• Bir necha daqiqa kutib, qayta urinib ko'ring\n"
                "• Boshqa Instagram video manzilini sinab ko'ring\n"
                "• Instagram Stories uchun maxsus cheklovlar mavjud"
            )
        else:
            await progress_message.edit_text(
                f"[!] Kechirasiz, men videoni yuklab ololmadim.\n"
                f"Xato: {error_msg[:200]}..."  # Uzoq xato xabarlarini qisqartirish
            )
    except Exception as e:
        logger.error(f"Kutilmagan xato: {str(e)}")
        await progress_message.edit_text(
            f"[!] Kechirasiz, kutilmagan xato yuz berdi.\n"
            f"Xato: {str(e)}"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kiruvchi xabarlarni qayta ishlash."""
    if not update.message or not update.message.text:
        return
        
    text = update.message.text
    user = update.effective_user
    
    user_name = user.first_name if user else "Noma'lum"
    logger.info(f"Foydalanuvchi {user_name} yubordi: {text}")
    
    # Agar xabar URL manzil bo'lsa
    if text.startswith('http'):
        await download_video(update, context)
    else:
        await update.message.reply_text(
            "[!] Menga video yuklab olish uchun haqiqiy URL manzil yuboring.\n\n"
            "Masalan: https://www.youtube.com/watch?v=example"
        )

def main() -> None:
    """Botni ishga tushirish."""
    # .env fayldan bot tokenini olish
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Xato: TELEGRAM_BOT_TOKEN .env faylida sozlanmagan!")
        print("Iltimos, .env faylini tahrirlang va haqiqiy bot tokenini kiriting.")
        return
    
    # Application yaratish va bot tokeningizni o'tkazish.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Foydalanuvchi Ctrl-C tugmachasini bosmaguncha botni ishga tushirish
    print("Bot ishga tushirilmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()