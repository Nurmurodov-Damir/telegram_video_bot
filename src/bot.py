#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Yuklab Olish Boti
Ushbu bot foydalanuvchilarga URL manzilini yuborish orqali turli platformalardan videolarni yuklab olish imkonini beradi.
"""

import logging
import os
import hashlib
import time
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

import yt_dlp
# Deep Translator kutubxonasini import qilish
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("Deep Translator kutubxonasi mavjud emas. Tarjima funksiyasi faol emas.")

# Emoji kutubxonasini import qilish
try:
    import emoji
    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False
    print("Emoji kutubxonasi mavjud emas.")

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

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

# Platforma aniqlash funksiyasi
def detect_platform(url):
    """URL manzilga qarab platformani aniqlash."""
    platforms = {
        'youtube': ['youtube.com', 'youtu.be'],
        'instagram': ['instagram.com', 'instagr.am'],
        'tiktok': ['tiktok.com'],
        'twitter': ['twitter.com', 'x.com'],
        'vimeo': ['vimeo.com'],
        'facebook': ['facebook.com', 'fb.com']
    }
    
    for platform, domains in platforms.items():
        for domain in domains:
            if domain in url:
                return platform
    return 'unknown'

# Platforma uchun stiker va tugma matni
def get_platform_sticker(platform):
    """Platformaga mos stiker va tugma matnini qaytarish."""
    stickers = {
        'youtube': '🔴',
        'instagram': '📸',
        'tiktok': '🎵',
        'twitter': '🐦',
        'vimeo': '🔷',
        'facebook': '📘',
        'unknown': '❓'
    }
    return stickers.get(platform, '❓')

def get_platform_button_text(platform):
    """Platformaga mos tugma matnini qaytarish."""
    buttons = {
        'youtube': 'YouTube Videosi',
        'instagram': 'Instagram Videosi',
        'tiktok': 'TikTok Videosi',
        'twitter': 'Twitter Videosi',
        'vimeo': 'Vimeo Videosi',
        'facebook': 'Facebook Videosi',
        'unknown': 'Boshqa Video'
    }
    return buttons.get(platform, 'Video')

# Tarjima funksiyasi
def translate_text(text, target_lang='uz'):
    """Matnni berilgan tilga tarjima qilish."""
    if not TRANSLATION_AVAILABLE or not text:
        return text
    
    try:
        # Matn uzunligini tekshirish (Google Translate limiti)
        if len(text) > 5000:
            text = text[:5000]  # Matnni qisqartirish
            
        # Matnni tarjima qilish
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        logger.error(f"Tarjima xatosi: {str(e)}")
        return text  # Xatolik yuz bersa, original matnni qaytarish

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi /start buyrug'ini berganida xabar yuborish."""
    user = update.effective_user
    if user:
        welcome_message = (
            f"👋 Salom {user.first_name}!\n\n"
            "Men turli platformalardan videolarni yuklab olishga yordam beradigan ilg'or video botman.\n\n"
            "📥 Menga video URL manzilini yuboring va men uni siz uchun yuklab olaman.\n"
            "✅ Qo'llab-quvvatlanadigan platformalar:\n"
            "• 🟥 YouTube\n"
            "• 📸 Instagram\n"
            "• 🎵 TikTok\n"
            "• 🐦 Twitter/X\n"
            "• 🔷 Vimeo\n"
            "• 📘 Facebook\n\n"
            "⚠️ Eslatma: Telegram cheklovlari tufayli 50MB dan katta videolar maxsus usullar bilan yuboriladi.\n\n"
            "👨‍💻 Muallif: N.Damir - Senior Dasturchi"
        )
        if update.message:
            # Platform selection buttons
            keyboard = [
                [InlineKeyboardButton("🔴 YouTube", callback_data="platform_youtube")],
                [InlineKeyboardButton("📸 Instagram", callback_data="platform_instagram")],
                [InlineKeyboardButton("🎵 TikTok", callback_data="platform_tiktok")],
                [InlineKeyboardButton("🐦 Twitter", callback_data="platform_twitter")],
                [InlineKeyboardButton("🔷 Vimeo", callback_data="platform_vimeo")],
                [InlineKeyboardButton("📘 Facebook", callback_data="platform_facebook")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    else:
        if update.message:
            await update.message.reply_text("Foydalanuvchi ma'lumotlarini olish imkonsiz.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi /help buyrug'ini berganida xabar yuborish."""
    help_text = (
        "🤖 Video Yuklab Olish Boti Yordami\n\n"
        "Men sizga turli platformalardan videolarni yuklab olishga yordam beraman.\n\n"
        "📥 Foydalanish bo'yicha qo'llanma:\n"
        "1. Menga yuklab olmoqchi bo'lgan videoning URL manzilini yuboring.\n"
        "2. Men uni qayta ishlab, videoni qaytaraman.\n\n"
        "📋 Qo'llab-quvvatlanadigan platformalar:\n"
        "• 🟥 YouTube\n"
        "• 📸 Instagram\n"
        "• 🎵 TikTok\n"
        "• 🐦 Twitter/X\n"
        "• 🔷 Vimeo\n"
        "• 📘 Facebook\n\n"
        "⚠️ Cheklovlar:\n"
        "• 100 daqiqadan ortiq videolarni yuklab olib bo'lmaydi.\n"
        "• 50MB dan katta videolar maxsus usullar bilan yuboriladi.\n"
        "• Ba'zi saytlar yuklab olishni cheklaydi.\n\n"
        "⌨️ Buyruqlar:\n"
        "/start - Botni ishga tushirish\n"
        "/help - Ushbu yordam xabarini ko'rsatish\n"
        "/about - Bot haqida ma'lumot ko'rsatish"
    )
    if update.message:
        await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchiga bot haqida ma'lumot yuborish."""
    about_text = (
        "📹 Video Yuklab Olish Boti\n\n"
        "Ushbu bot sizga turli platformalardan videolarni bevosita Telegramga yuklab olish imkonini beradi.\n\n"
        "🛠 Foydalanilgan texnologiyalar:\n"
        "• 🐍 python-telegram-bot\n"
        "• 📥 yt-dlp\n"
        "• 🌐 deep-translator (tarjima uchun)\n"
        "• 😊 emoji (stikerlar uchun)\n\n"
        "👨‍💻 Dasturchi:\n"
        "N.Damir - Senior Dasturchi\n\n"
        "🔒 Maxfiylik:\n"
        "Hech qanday video yoki shaxsiy ma'lumot serverlarimizda saqlanmaydi.\n"
        "Barcha qayta ishlash vaqtinchalik amalga oshiriladi va fayllar yuborilgandan keyin o'chirib tashlanadi."
    )
    if update.message:
        await update.message.reply_text(about_text)

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
    
    # Platformani aniqlash
    platform = detect_platform(url)
    platform_sticker = get_platform_sticker(platform)
    platform_button_text = get_platform_button_text(platform)
    
    # Boshlang'ich xabar yuborish
    progress_message = await update.message.reply_text(f"{platform_sticker} So'rovingiz qayta ishlanmoqda...")
    
    try:
        # yt-dlp opsiyalarini sozlash
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOADS_DIR, f'{user.id}_%(title)s.%(ext)s'),
            'format': 'best[height<=720]/best[height<=480]/best',
            'extractor_args': {
                'instagram': {
                    'api': 'web',
                    'include_ads': False,
                    'include_paid_promotion': False,
                }
            },
            'sleep_interval': 1,
            'max_sleep_interval': 5,
            # YouTube bot tekshiruvini o'tkazish uchun cookies fayli
            'cookies': 'cookies.txt',  # cookies.txt faylini bir xil katalogga joylashtiring
            # Subtitle yuklab olishni yoqish
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'ru', 'uz', 'all'],
            'skip_download': False,
        }
        
        # FFmpeg mavjudligini tekshirish va opsiyalar qo'shish
        import shutil
        if shutil.which('ffmpeg'):
            ydl_opts['format'] = 'best[height<=720]+bestaudio/best[height<=480]/best'
        else:
            logger.warning("FFmpeg topilmadi. Yuklab olingan format eng yaxshi bo'lmasligi mumkin.")
        
        # Instagram uchun qo'shimcha format sozlamalari
        if 'instagram.com' in url or 'instagr.am' in url:
            ydl_opts['format'] = 'best[height<=720]/best[height<=480]/best'
            ydl_opts['writesubtitles'] = True
            ydl_opts['writeautomaticsub'] = True
            ydl_opts['subtitleslangs'] = ['en', 'ru', 'uz', 'all']
            # Instagram uchun maxsus sozlamalar
            ydl_opts['extractor_args'] = {
                'instagram': {
                    'api': 'web',
                    'include_ads': False,
                    'include_paid_promotion': False,
                }
            }
        
        # Jarayonni yangilash
        await progress_message.edit_text(f"{platform_sticker} Video tahlil qilinmoqda...")
        
        # Avval video ma'lumotlarini olish
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if info_dict is None:
                await progress_message.edit_text(
                    "Kechirasiz, men bu videoni tahlil qila olmadim.\n"
                    "Iltimos, URL manzil to'g'ri ekanligini tekshiring."
                )
                return
                
            # Debug uchun ma'lumotlarni log qilish
            logger.info(f"Video info keys: {list(info_dict.keys())}")
            if 'instagram.com' in url:
                logger.info(f"Instagram video info - description: {info_dict.get('description', 'No description')}")
                logger.info(f"Instagram video info - subtitles: {info_dict.get('subtitles', 'No subtitles')}")
                logger.info(f"Instagram video info - automatic_captions: {info_dict.get('automatic_captions', 'No auto captions')}")
                
            video_title = info_dict.get('title', 'video')
            video_duration = info_dict.get('duration', 0)
            video_description = info_dict.get('description', '')
            
            # Agar video juda uzun bo'lsa (100 daqiqadan ortiq)
            max_duration_env = os.getenv("MAX_VIDEO_DURATION", "6000")
            max_duration = int(max_duration_env)
            if max_duration == 600:
                max_duration = 6000
                logger.info("MAX_VIDEO_DURATION 600 dan 6000 ga o'zgartirildi")
            
            if video_duration > max_duration:
                await progress_message.edit_text(
                    f"Kechirasiz, men {max_duration // 60} daqiqadan ortiq videolarni yuklab ololmayman.\n"
                    f"Video davomiyligi: {video_duration // 60} daqiqa"
                )
                return
        
        # Jarayonni yangilash
        await progress_message.edit_text(f"{platform_sticker} Video yuklab olinmoqda...")
        
        # Videoni yuklab olish
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info_dict)
        
        # Fayl mavjudligini tekshirish
        if not os.path.exists(video_filename):
            await progress_message.edit_text(
                "Kechirasiz, men videoni yuklab ololmadim.\n"
                "Fayl yaratilmadi."
            )
            return
        
        # Fayl hajmini tekshirish
        file_size = os.path.getsize(video_filename)
        max_size = int(os.getenv("MAX_VIDEO_SIZE", "52428800"))  # 50MB baytlarda
        
        if file_size > max_size:
            await progress_message.edit_text(
                f"📹 Video fayl juda katta ({file_size / (1024*1024):.1f}MB).\n"
                f"Telegram faqat {max_size / (1024*1024):.0f}MB gacha fayllarni yuborishga ruxsat beradi.\n\n"
                f"Quyidagi variantlardan birini tanlang:"
            )
            return
        
        await progress_message.edit_text(f"{platform_sticker} Video Telegramga yuklanmoqda...")
        
        # Foydalanuvchiga video yuborish
        with open(video_filename, 'rb') as video_file:
            caption_text = f"{platform_sticker} {platform_button_text}: {video_title}"
            
            # Subtitle mavjudligini tekshirish va tarjima qilish
            subtitle_info = ""
            
            # Instagram uchun maxsus caption tekshiruvi
            if 'instagram.com' in url or 'instagr.am' in url:
                # Instagram captionlarini tekshirish
                if info_dict.get('description'):
                    instagram_caption = info_dict.get('description', '')
                    if instagram_caption and len(instagram_caption) > 0:
                        subtitle_info += "\n\n📢 Instagram Caption:\n"
                        # Caption uzunligini cheklash
                        if len(instagram_caption) > 300:
                            subtitle_info += instagram_caption[:300] + "..."
                        else:
                            subtitle_info += instagram_caption
                        
                        # Agar tarjima mavjud bo'lsa
                        if TRANSLATION_AVAILABLE:
                            try:
                                translated_caption = translate_text(instagram_caption, 'uz')
                                if translated_caption and translated_caption != instagram_caption:
                                    subtitle_info += f"\n\n🔄 Tarjima:\n{translated_caption[:300]}{'...' if len(translated_caption) > 300 else ''}"
                            except Exception as e:
                                logger.error(f"Tarjima xatosi: {str(e)}")
            
            # Boshqa platformalar uchun subtitle tekshiruvi
            elif info_dict.get('subtitles') or info_dict.get('automatic_captions'):
                subtitle_info += "\n\n📢 Subtitles:\n"
                subtitles = info_dict.get('subtitles', {})
                auto_captions = info_dict.get('automatic_captions', {})
                
                # Avtomatik subtitlelar mavjudligini tekshirish
                if auto_captions:
                    subtitle_info += "🤖 Avtomatik titrlar mavjud\n"
                elif subtitles:
                    subtitle_info += "📝 Qo'lda titrlar mavjud\n"
                
                # Agar tarjima mavjud bo'lsa
                if TRANSLATION_AVAILABLE:
                    try:
                        description = info_dict.get('description', '')
                        if description and len(description) > 0:
                            # Izoh uchun tarjima
                            translated_desc = translate_text(description, 'uz')
                            if translated_desc and translated_desc != description:
                                subtitle_info += f"\n🔄 Tarjima:\n{translated_desc[:200]}{'...' if len(translated_desc) > 200 else ''}"
                    except Exception as e:
                        logger.error(f"Tarjima xatosi: {str(e)}")
            
            # Umumiy description mavjud bo'lsa (boshqa platformalar uchun)
            elif info_dict.get('description'):
                description = info_dict.get('description', '')
                if description and len(description) > 0:
                    subtitle_info += "\n\n📢 Video Description:\n"
                    # Description uzunligini cheklash
                    if len(description) > 300:
                        subtitle_info += description[:300] + "..."
                    else:
                        subtitle_info += description
                    
                    # Agar tarjima mavjud bo'lsa
                    if TRANSLATION_AVAILABLE:
                        try:
                            translated_desc = translate_text(description, 'uz')
                            if translated_desc and translated_desc != description:
                                subtitle_info += f"\n\n🔄 Tarjima:\n{translated_desc[:300]}{'...' if len(translated_desc) > 300 else ''}"
                        except Exception as e:
                            logger.error(f"Tarjima xatosi: {str(e)}"

            # Subtitle ma'lumotini captionga qo'shish
            if subtitle_info:
                # Caption uzunligini tekshirish (Telegram limiti 1024 belgi)
                if len(caption_text + subtitle_info) <= 1024:
                    caption_text += subtitle_info
                else:
                    # Agar caption juda uzun bo'lsa, qisqartirish
                    available_length = 1024 - len(caption_text) - 50  # 50 belgi rezerv
                    if available_length > 100:
                        caption_text += subtitle_info[:available_length] + "..."

            await update.message.reply_video(
                video=video_file,
                caption=caption_text,
                supports_streaming=True
            )
        
        # Yuklab olingan faylni tozalash
        os.remove(video_filename)
        
        # Progress message'ni o'chirish
        try:
            await progress_message.delete()
        except:
            pass
        
    except yt_dlp.DownloadError as e:
        logger.error(f"Yuklab olish xatosi: {str(e)}")
        error_msg = str(e)
        if 'Unsupported URL' in error_msg:
            if 'mover.uz' in url:
                await progress_message.edit_text(
                    "Kechirasiz, men Mover.uz saytidan video yuklab olishni qo'llab-quvvatlamayman.\n"
                    "Mover.uz saytida video yuklab olish uchun ularning o'zlarining dasturidan foydalaning.\n\n"
                    "Men YouTube, Vimeo, Twitter, Instagram, TikTok va boshqa saytlarni qo'llab-quvvatlayman."
                )
            else:
                await progress_message.edit_text(
                    "Kechirasiz, men bu saytdan yuklab olishni qo'llab-quvvatlamayman.\n"
                    "Men YouTube, Vimeo, Twitter, Instagram, TikTok va minglab boshqa saytlarni qo'llab-quvvatlayman."
                )
        elif 'Sign in to confirm you\'re not a bot' in error_msg:
            await progress_message.edit_text(
                "❌ YouTube bot tekshiruvi aniqlandi!\n\n"
                "💡 Yechimlar:\n"
                "1. Boshqa video manbasi tanlang\n"
                "2. Administrator cookies.txt faylini yangilashini so'rang\n"
                "3. Video manzilini tekshirib ko'ring\n\n"
                "📢 Bu YouTube tomonidan avtomatik yuklab olishni cheklash uchun qo'llaniladigan xavfsizlik chorasi."
            )
        else:
            await progress_message.edit_text(
                f"Kechirasiz, men videoni yuklab ololmadim.\n"
                f"Xato: {error_msg[:200]}..."
            )
    except Exception as e:
        logger.error(f"Kutilmagan xato: {str(e)}")
        await progress_message.edit_text(
            f"Kechirasiz, kutilmagan xato yuz berdi.\n"
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
            "Menga video yuklab olish uchun haqiqiy URL manzil yuboring.\n\n"
            "Masalan: https://www.youtube.com/watch?v=example"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tugma bosilganda ishlov berish."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = query.from_user
    
    if data.startswith("platform_"):
        platform = data[9:]  # "platform_" dan keyingi qism
        platform_names = {
            'youtube': 'YouTube',
            'instagram': 'Instagram',
            'tiktok': 'TikTok',
            'twitter': 'Twitter',
            'vimeo': 'Vimeo',
            'facebook': 'Facebook'
        }
        platform_name = platform_names.get(platform, platform.capitalize())
        
        example_urls = {
            'youtube': 'https://www.youtube.com/watch?v=example',
            'instagram': 'https://www.instagram.com/p/example/',
            'tiktok': 'https://www.tiktok.com/@user/video/example',
            'twitter': 'https://twitter.com/user/status/example',
            'vimeo': 'https://vimeo.com/example',
            'facebook': 'https://www.facebook.com/user/videos/example'
        }
        example_url = example_urls.get(platform, 'https://example.com')
        
        message = (
            f"📥 {platform_name} platformasidan video yuklab olish\n\n"
            f"Quyidagi formatda URL manzil yuboring:\n"
            f"{example_url}\n\n"
            f"Masalan: {example_url}"
        )
        
        # Orqaga qaytish tugmasi
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif data == "back_to_main":
        # Asosiy menyuga qaytish
        welcome_message = (
            f"👋 Salom {user.first_name}!\n\n"
            "Men turli platformalardan videolarni yuklab olishga yordam beradigan zamonaviy video botiman.\n\n"
            "📥 Menga video URL manzilini yuboring va men uni siz uchun yuklab olaman.\n"
            "✅ Qo'llab-quvvatlanadigan platformalar:\n"
            "• 🟥 YouTube\n"
            "• 📸 Instagram\n"
            "• 🎵 TikTok\n"
            "• 🐦 Twitter/X\n"
            "• 🔷 Vimeo\n"
            "• 📘 Facebook\n\n"
            "⚠️ Eslatma: Telegram cheklovlari tufayli 50MB dan katta videolar maxsus usullar bilan yuboriladi.\n\n"
            "👨‍💻 Dastur muallifi: N.Damir - Senior Dasturchi"
        )
        
        # Platforma tanlash tugmalari
        keyboard = [
            [InlineKeyboardButton("🔴 YouTube", callback_data="platform_youtube")],
            [InlineKeyboardButton("📸 Instagram", callback_data="platform_instagram")],
            [InlineKeyboardButton("🎵 TikTok", callback_data="platform_tiktok")],
            [InlineKeyboardButton("🐦 Twitter", callback_data="platform_twitter")],
            [InlineKeyboardButton("🔷 Vimeo", callback_data="platform_vimeo")],
            [InlineKeyboardButton("📘 Facebook", callback_data="platform_facebook")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(welcome_message, reply_markup=reply_markup)

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
    application.add_handler(CallbackQueryHandler(button_handler))

    # Foydalanuvchi Ctrl-C tugmachasini bosmaguncha botni ishga tushirish
    print("Bot ishga tushirilmoqda...")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🔄 Bot o'chirilmoqda...")
        logger.info("Bot KeyboardInterrupt orqali o'chirildi")
        print("✅ Bot to'g'ri o'chirildi")
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")
        print(f"❌ Bot ishga tushirishda xatolik: {e}")

if __name__ == '__main__':
    main()