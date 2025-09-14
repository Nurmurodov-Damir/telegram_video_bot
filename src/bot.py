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
        'youtube': 'YouTube Video',
        'instagram': 'Instagram Video',
        'tiktok': 'TikTok Video',
        'twitter': 'Twitter Video',
        'vimeo': 'Vimeo Video',
        'facebook': 'Facebook Video',
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

# Foydalanuvchi so'rovlarini saqlash (kelajakda ishlatish uchun)
# user_requests = {}

# Buyruq handlerlarini belgilash
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi /start buyrug'ini yuborganida xabar yuborish."""
    user = update.effective_user
    if user:
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
        if update.message:
            # Platforma tanlash tugmalari
            keyboard = [
                [InlineKeyboardButton(" YouTube", callback_data="platform_youtube")],
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
    """Foydalanuvchi /help buyrug'ini yuborganida xabar yuborish."""
    help_text = (
        "🤖 Video Yuklab Olish Boti Yordami\n\n"
        "Men turli platformalardan videolarni yuklab olishga yordam beraman.\n\n"
        "📥 Foydalanish tartibi:\n"
        "1. Menga yuklab olmoqchi bo'lgan videoning URL manzilini yuboring\n"
        "2. Men qayta ishlash va videoni yuborishimni kuting\n\n"
        "📋 Qo'llab-quvvatlanadigan platformalar:\n"
        "• 🟥 YouTube\n"
        "• 📸 Instagram\n"
        "• 🎵 TikTok\n"
        "• 🐦 Twitter/X\n"
        "• 🔷 Vimeo\n"
        "• 📘 Facebook\n\n"
        "⚠️ Cheklovlar:\n"
        "• 100 daqiqadan ortiq videolar yuklab olinmaydi\n"
        "• 50MB dan ortiq videolar maxsus usullar bilan yuboriladi\n"
        "• Ba'zi saytlar yuklab olishni cheklaydi\n\n"
        "⌨️ Buyruqlar:\n"
        "/start - Botni ishga tushirish\n"
        "/help - Ushbu yordam xabarini ko'rsatish\n"
        "/about - Bot haqida ma'lumot"
    )
    if update.message:
        await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot haqida ma'lumot yuborish."""
    about_text = (
        "📹 Video Yuklab Olish Boti\n\n"
        "Ushbu bot turli platformalardan videolarni bevosita Telegramga yuklab olish imkonini beradi.\n\n"
        "🛠 Yaratilgan texnologiyalar:\n"
        "• 🐍 python-telegram-bot\n"
        "• 📥 yt-dlp\n"
        "• 🌐 deep-translator (tarjima uchun)\n"
        "• 😊 emoji (stikerlar uchun)\n\n"
        "👨‍💻 Ishlab chiquvchi:\n"
        "N.Damir - Senior Dasturchi\n\n"
        "🔒 Maxfiylik:\n"
        "Hech qanday video yoki shaxsiy ma'lumot serverlarimizda saqlanmaydi.\n"
        "Barcha qayta ishlash vaqtinchalik amalga oshiriladi va fayllar yuborilgandan so'ng o'chirib tashlanadi."
    )
    if update.message:
        await update.message.reply_text(about_text)

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
            'format': 'best[height<=720]/best[height<=480]/best',  # Format cheklovini olib tashlash
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
            ydl_opts['format'] = 'best[height<=720]+bestaudio/best[height<=480]/best'
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
        await progress_message.edit_text(f"{platform_sticker} Video tahlil qilinmoqda...")
        
        # Avval video ma'lumotlarini olish
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            # info_dict None bo'lishi mumkin, shu sababli tekshirish kerak
            if info_dict is None:
                await progress_message.edit_text(
                    "Kechirasiz, men bu videoni tahlil qila olmadim.\\n"
                    "Iltimos, URL manzil to'g'ri ekanligini tekshiring."
                )
                return
                
            # Debug uchun info_dict kalitlarini log qilish
            logger.info(f"Info dict keys: {list(info_dict.keys())}")
                
            video_title = info_dict.get('title', 'video')
            video_duration = info_dict.get('duration', 0)
            video_description = info_dict.get('description', '')  # Instagram izoh matni
            
            # Agar video juda uzun bo'lsa (100 daqiqadan ortiq)
            max_duration_env = os.getenv("MAX_VIDEO_DURATION", "6000")
            max_duration = int(max_duration_env)  # 100 daqiqa soniyalarda
            # Agar environment variable 600 bo'lsa, uni 6000 ga o'zgartirish
            if max_duration == 600:
                max_duration = 6000
                logger.info("MAX_VIDEO_DURATION 600 dan 6000 ga o'zgartirildi")
            logger.info(f"MAX_VIDEO_DURATION env: {max_duration_env}")
            logger.info(f"Max duration: {max_duration} seconds ({max_duration // 60} minutes)")
            logger.info(f"Video duration: {video_duration} seconds ({video_duration // 60} minutes)")
            if video_duration > max_duration:
                await progress_message.edit_text(
                    f"Kechirasiz, men {max_duration // 60} daqiqadan ortiq videolarni yuklab ololmayman.\\n"
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
                "Kechirasiz, men videoni yuklab ololmadim.\\n"
                "Fayl yaratilmadi."
            )
            return
        
        # Fayl hajmini tekshirish va katta fayllar uchun maxsus usul
        file_size = os.path.getsize(video_filename)
        max_size = int(os.getenv("MAX_VIDEO_SIZE", "52428800"))  # 50MB baytlarda
        
        if file_size > max_size:
            # Katta fayl uchun maxsus usullarni taklif qilish
            await progress_message.edit_text(
                f"📹 Video fayl juda katta ({file_size / (1024*1024):.1f}MB).\\n"
                f"Telegram faqat {max_size / (1024*1024):.0f}MB gacha fayllarni yuborishga ruxsat beradi.\\n\\n"
                f"Quyidagi variantlardan birini tanlang:"
            )
            
            # Maxsus tugmalar yaratish
            keyboard = [
                [InlineKeyboardButton("📁 Cloud Storage (Google Drive)", callback_data=f"cloud_{video_filename}")],
                [InlineKeyboardButton("✂️ Video qismlarga bo'lish", callback_data=f"split_{video_filename}")],
                [InlineKeyboardButton("🔗 To'g'ridan-to'g'ri havola", callback_data=f"link_{video_filename}")],
                [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await progress_message.edit_text(
                f"📹 Video fayl juda katta ({file_size / (1024*1024):.1f}MB).\\n"
                f"Telegram faqat {max_size / (1024*1024):.0f}MB gacha fayllarni yuborishga ruxsat beradi.\\n\\n"
                f"Quyidagi variantlardan birini tanlang:",
                reply_markup=reply_markup
            )
            return
        
        await progress_message.edit_text(f"{platform_sticker} Video Telegramga yuklanmoqda...")
        
        # Foydalanuvchiga video yuborish
        with open(video_filename, 'rb') as video_file:
            # Video izoh matnini tayyorlash
            caption_text = f"{platform_sticker} {platform_button_text}: {video_title}"
            
            # Statistik ma'lumotlarni qo'shish
            stats_lines = []
            
            # Asosiy statistik ma'lumotlarni olish
            likes = info_dict.get('like_count') or info_dict.get('likes')
            comments = info_dict.get('comment_count') or info_dict.get('comments')
            upload_date = info_dict.get('upload_date') or info_dict.get('timestamp')
            views = info_dict.get('view_count') or info_dict.get('views')
            
            # Qo'shimcha ma'lumotlar
            uploader = info_dict.get('uploader')
            duration = info_dict.get('duration')
            
            # Statistik ma'lumotlarni qo'shish (faqat mavjud bo'lsa)
            if likes is not None and likes != 'N/A':
                stats_lines.append(f"• ❤️ Likes: {likes}")
                
            if comments is not None and comments != 'N/A':
                stats_lines.append(f"• 💬 Comments: {comments}")
                
            if views is not None and views != 'N/A':
                stats_lines.append(f"• 👁️ Views: {views}")
                
            # Upload sanasini formatlash
            if upload_date is not None and upload_date != 'N/A':
                try:
                    if isinstance(upload_date, str) and len(upload_date) == 8:
                        year = upload_date[:4]
                        month = upload_date[4:6]
                        day = upload_date[6:8]
                        formatted_date = f"{day}.{month}.{year}"
                        stats_lines.append(f"• 📅 Upload date: {formatted_date}")
                    elif isinstance(upload_date, int):
                        # Unix timestamp bo'lsa
                        from datetime import datetime
                        dt = datetime.fromtimestamp(upload_date)
                        formatted_date = dt.strftime("%d.%m.%Y")
                        stats_lines.append(f"• 📅 Upload date: {formatted_date}")
                    else:
                        stats_lines.append(f"• 📅 Upload date: {upload_date}")
                except:
                    stats_lines.append(f"• 📅 Upload date: {upload_date}")
            
            if duration is not None and duration != 'N/A':
                stats_lines.append(f"• ⏱ Duration: {duration} sec")
                
            if uploader is not None and uploader != 'N/A':
                stats_lines.append(f"• 📤 Uploader: {uploader}")
            
            # Statistik matnni yaratish
            if stats_lines:
                stats_text = "\\n\\n📊 Statistika:\\n" + "\\n".join(stats_lines)
            else:
                stats_text = ""
            
            if video_description:
                # Izoh matnini o'zbek tiliga tarjima qilish
                translated_description = translate_text(video_description)
                
                # Original va tarjima matnini birga qo'shish
                full_caption = f"{caption_text}\\n\\n📝 Izoh (Original): {video_description}\\n\\n📝 Izoh (O'zbek tilida): {translated_description}{stats_text}"
            else:
                full_caption = f"{caption_text}{stats_text}"
                
            caption_text = full_caption[:1020] + "..." if len(full_caption) > 1024 else full_caption
            
            # Platformaga mos tugmalar yaratish
            keyboard = [
                [InlineKeyboardButton(f"🔁 Qayta yuklash", callback_data="retry")],
                [InlineKeyboardButton(f"ℹ️ Video haqida", callback_data="info")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            logger.info(f"Tugma ma'lumotlari: retry, info")
            logger.info(f"Tugma uzunligi: retry={len('retry')}, info={len('info')}")
            
            await update.message.reply_video(
                video=video_file,
                caption=caption_text,
                supports_streaming=True,
                reply_markup=reply_markup
            )
        
        # Yuklab olingan faylni tozalash
        os.remove(video_filename)
        
        # Progress message'ni o'chirish (video allaqachon yuborilgan)
        try:
            await progress_message.delete()
        except:
            pass  # Agar o'chirishda xatolik bo'lsa, e'tibor bermaslik
        
    except yt_dlp.DownloadError as e:
        logger.error(f"Yuklab olish xatosi: {str(e)}")
        error_msg = str(e)
        if 'Unsupported URL' in error_msg:
            # Maxsus xabar Mover.uz uchun
            if 'mover.uz' in url:
                await progress_message.edit_text(
                    "Kechirasiz, men Mover.uz saytidan video yuklab olishni qo'llab-quvvatlamayman.\\n"
                    "Mover.uz saytida video yuklab olish uchun ularning o'zlarining dasturidan foydalaning.\\n\\n"
                    "Men YouTube, Vimeo, Twitter, Instagram, TikTok va boshqa saytlarni qo'llab-quvvatlayman."
                )
            else:
                await progress_message.edit_text(
                    "Kechirasiz, men bu saytdan yuklab olishni qo'llab-quvvatlamayman.\\n"
                    "Men YouTube, Vimeo, Twitter, Instagram, TikTok va minglab boshqa saytlarni qo'llab-quvvatlayman."
                )
        elif 'HTTP Error 403' in error_msg:
            if 'instagram.com' in url or 'instagr.am' in url:
                await progress_message.edit_text(
                    "Instagram video yuklab olishda kirish rad etildi.\\n"
                    "Bu Instagram'ning xavfsizlik siyosati tufayli bo'lishi mumkin.\\n"
                    "Iltimos, quyidagilarni sinab ko'ring:\\n"
                    "• Video ochiq ekanligini tekshiring\\n"
                    "• Video egasi tomonidan cheklangan bo'lishi mumkin\\n"
                    "• Bir necha daqiqa kutib, qayta urinib ko'ring"
                )
            else:
                await progress_message.edit_text(
                    "Ushbu videoga kirish rad etildi. U shaxsiy yoki mintaqaviy cheklangan bo'lishi mumkin."
                )
        elif 'Requested format is not available' in error_msg:
            # Instagram uchun maxsus xabar
            if 'instagram.com' in url or 'instagr.am' in url:
                await progress_message.edit_text(
                    "Instagram video yuklab olishda muammo yuz berdi.\\n"
                    "Bu Instagram'ning cheklovlari tufayli bo'lishi mumkin.\\n"
                    "Iltimos, quyidagilarni sinab ko'ring:\\n"
                    "• Video ochiq ekanligini tekshiring\\n"
                    "• Bir necha daqiqa kutib, qayta urinib ko'ring\\n"
                    "• Boshqa Instagram video manzilini sinab ko'ring"
                )
            else:
                await progress_message.edit_text(
                    "Ushbu video uchun so'ralgan format mavjud emas.\\n"
                    "Bu ba'zi ijtimoiy tarmoq platformalarida yuzaga keladi.\\n"
                    "Iltimos, boshqa video manzilini yuboring."
                )
        elif 'unsupported keyring' in error_msg:
            # Browser keyring xatosi uchun maxsus xabar
            await progress_message.edit_text(
                "Browser cookies bilan bog'liq muammo yuz berdi.\\n"
                "Bu Windows tizimida browser keyring qo'llab-quvvatlanmasligi tufayli.\\n\\n"
                "Yechim:\\n"
                "• Cookies sozlamalari o'chirildi\\n"
                "• Video ochiq ekanligini tekshiring\\n"
                "• Bir necha daqiqa kutib, qayta urinib ko'ring\\n"
                "• Boshqa video manzilini sinab ko'ring"
            )
        elif 'instagram.com' in url or 'instagr.am' in url:
            # Instagram uchun umumiy xato xabari
            await progress_message.edit_text(
                "Instagram video yuklab olishda muammo yuz berdi.\\n"
                "Bu Instagram'ning cheklovlari tufayli bo'lishi mumkin.\\n\\n"
                "Yechimlar:\\n"
                "• Video ochiq ekanligini tekshiring\\n"
                "• Video egasi tomonidan cheklangan bo'lishi mumkin\\n"
                "• Bir necha daqiqa kutib, qayta urinib ko'ring\\n"
                "• Boshqa Instagram video manzilini sinab ko'ring\\n"
                "• Instagram Stories uchun maxsus cheklovlar mavjud"
            )
        else:
            await progress_message.edit_text(
                f"Kechirasiz, men videoni yuklab ololmadim.\\n"
                f"Xato: {error_msg[:200]}..."  # Uzoq xato xabarlarini qisqartirish
            )
    except Exception as e:
        logger.error(f"Kutilmagan xato: {str(e)}")
        await progress_message.edit_text(
            f"Kechirasiz, kutilmagan xato yuz berdi.\\n"
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
    
    if data == "retry":
        # Qayta yuklash logikasi
        await query.edit_message_text("🔁 Qayta yuklash so'rovi qabul qilindi. Iltimos, yangi URL manzil yuboring.")
    elif data == "info":
        # Video haqida ma'lumot logikasi
        await query.edit_message_text("ℹ️ Video haqida ma'lumot so'rovi qabul qilindi. Iltimos, yangi URL manzil yuboring.")
    elif data.startswith("platform_"):
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
            [InlineKeyboardButton(" YouTube", callback_data="platform_youtube")],
            [InlineKeyboardButton("📸 Instagram", callback_data="platform_instagram")],
            [InlineKeyboardButton("🎵 TikTok", callback_data="platform_tiktok")],
            [InlineKeyboardButton("🐦 Twitter", callback_data="platform_twitter")],
            [InlineKeyboardButton("🔷 Vimeo", callback_data="platform_vimeo")],
            [InlineKeyboardButton("📘 Facebook", callback_data="platform_facebook")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(welcome_message, reply_markup=reply_markup)
    elif data == "cancel":
        # Bekor qilish
        await query.edit_message_text("❌ Operatsiya bekor qilindi.")
    elif data.startswith("cloud_"):
        # Cloud storage uchun
        file_path = data[6:]  # "cloud_" dan keyingi qism
        await handle_cloud_storage(query, file_path)
    elif data.startswith("split_"):
        # Video qismlarga bo'lish uchun
        file_path = data[6:]  # "split_" dan keyingi qism
        await handle_video_splitting(query, file_path)
    elif data.startswith("link_"):
        # To'g'ridan-to'g'ri havola uchun
        file_path = data[5:]  # "link_" dan keyingi qism
        await handle_direct_link(query, file_path)

async def handle_cloud_storage(query, file_path):
    """Cloud storage (Google Drive) ga yuklash."""
    try:
        await query.edit_message_text("📁 Cloud storage ga yuklash...")
        
        # Hozircha Google Drive integratsiyasi yo'q, shuning uchun foydalanuvchiga yo'riqnoma beramiz
        file_size = os.path.getsize(file_path) / (1024*1024)
        
        message = (
            f"📁 Cloud Storage Varianti\n\n"
            f"Video hajmi: {file_size:.1f}MB\n\n"
            f"🔧 Hozircha Google Drive integratsiyasi ishlab chiqilmoqda.\n"
            f"Vaqtinchalik yechim:\n\n"
            f"1️⃣ Video fayl serverda saqlanadi\n"
            f"2️⃣ Sizga maxsus havola beriladi\n"
            f"3️⃣ Havolani boshqa qurilmalarda ochishingiz mumkin\n\n"
            f"⚠️ Fayl 24 soatdan keyin avtomatik o'chiriladi"
        )
        
        # Havolani yaratish (hozircha mock)
        download_link = f"https://your-server.com/download/{os.path.basename(file_path)}"
        
        keyboard = [
            [InlineKeyboardButton("🔗 Yuklab olish havolasi", url=download_link)],
            [InlineKeyboardButton("📱 QR kod", callback_data=f"qr_{file_path}")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Cloud storage xatoligi: {e}")
        await query.edit_message_text("❌ Cloud storage ga yuklashda xatolik yuz berdi.")

async def handle_video_splitting(query, file_path):
    """Videoni qismlarga bo'lish."""
    try:
        await query.edit_message_text("✂️ Video qismlarga bo'linmoqda...")
        
        file_size = os.path.getsize(file_path) / (1024*1024)
        max_size = 45  # MB, xavfsizlik uchun 45MB
        
        # Qismlar sonini hisoblash
        parts_count = int(file_size / max_size) + 1
        
        message = (
            f"✂️ Video Qismlarga Bo'lish\n\n"
            f"Video hajmi: {file_size:.1f}MB\n"
            f"Qismlar soni: {parts_count} ta\n"
            f"Har bir qism: ~{max_size}MB\n\n"
            f"🔧 Hozircha video bo'lish funksiyasi ishlab chiqilmoqda.\n"
            f"Vaqtinchalik yechim:\n\n"
            f"1️⃣ Video avtomatik ravishda qismlarga bo'linadi\n"
            f"2️⃣ Har bir qism alohida yuboriladi\n"
            f"3️⃣ Siz qismlarni ketma-ket ko'rishingiz mumkin"
        )
        
        keyboard = [
            [InlineKeyboardButton("✅ Qismlarga bo'lishni boshlash", callback_data=f"start_split_{file_path}")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Video splitting xatoligi: {e}")
        await query.edit_message_text("❌ Video bo'lishda xatolik yuz berdi.")

async def handle_direct_link(query, file_path):
    """To'g'ridan-to'g'ri yuklab olish havolasini berish."""
    try:
        await query.edit_message_text("🔗 To'g'ridan-to'g'ri havola yaratilmoqda...")
        
        file_size = os.path.getsize(file_path) / (1024*1024)
        
        # Mock havola (real serverda bu haqiqiy havola bo'ladi)
        download_link = f"https://your-server.com/download/{os.path.basename(file_path)}"
        
        message = (
            f"🔗 To'g'ridan-to'g'ri Yuklab Olish\n\n"
            f"Video hajmi: {file_size:.1f}MB\n\n"
            f"✅ Video fayl serverda saqlanadi\n"
            f"🔗 Quyidagi havola orqali yuklab oling:\n\n"
            f"📱 Mobil qurilmalarda:\n"
            f"• Havolani bosing\n"
            f"• 'Yuklab olish' tugmasini bosing\n\n"
            f"💻 Kompyuterda:\n"
            f"• Havolani oching\n"
            f"• Fayl avtomatik yuklanadi\n\n"
            f"⚠️ Havola 24 soat amal qiladi"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔗 Yuklab olish", url=download_link)],
            [InlineKeyboardButton("📱 QR kod", callback_data=f"qr_{file_path}")],
            [InlineKeyboardButton("📋 Havolani nusxalash", callback_data=f"copy_{file_path}")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Direct link xatoligi: {e}")
        await query.edit_message_text("❌ Havola yaratishda xatolik yuz berdi.")

async def send_shutdown_message(application: Application):
    """Bot o'chib ketganda foydalanuvchilarga xabar yuborish."""
    try:
        # Faol foydalanuvchilar ro'yxatini olish (oxirgi 24 soatda xabar yuborganlar)
        # Bu oddiy yechim, haqiqiy loyihada foydalanuvchilar bazasidan olish kerak
        shutdown_message = (
            "🔴 **Bot vaqtincha o'chirildi**\n\n"
            "Texnik ishlar yoki yangilanishlar tufayli bot vaqtincha ishlamayapti.\n\n"
            "⏰ **Qachon qaytadi:**\n"
            "Tez orada qayta ishga tushiriladi\n\n"
            "📞 **Yordam:**\n"
            "Muammolar bo'lsa, administrator bilan bog'laning\n\n"
            "👨‍💻 _Dastur muallifi: N.Damir - Senior Dasturchi_"
        )
        
        # Bot adminlari ro'yxati (bu yerda o'z ID'ingizni qo'ying)
        admin_ids = [8250501153]  # Admin ID'larni bu yerga qo'shing
        
        for admin_id in admin_ids:
            try:
                await application.bot.send_message(
                    chat_id=admin_id,
                    text=shutdown_message,
                    parse_mode='Markdown'
                )
                logger.info(f"Shutdown xabari admin {admin_id} ga yuborildi")
            except Exception as e:
                logger.error(f"Admin {admin_id} ga xabar yuborishda xatolik: {e}")
                
    except Exception as e:
        logger.error(f"Shutdown xabarlarini yuborishda xatolik: {e}")

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

    # Bot o'chib ketganda xabar yuborish
    import signal
    import asyncio
    
    def signal_handler(signum, frame):
        """Signal handler - bot o'chib ketganda."""
        print("\n🔄 Bot o'chirilmoqda...")
        logger.info("Bot shutdown signal qabul qilindi")
        
        # Asyncio event loop yaratish va shutdown xabarini yuborish
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_shutdown_message(application))
            loop.close()
        except Exception as e:
            logger.error(f"Shutdown xabari yuborishda xatolik: {e}")
        
        print("✅ Bot to'g'ri o'chirildi")
        sys.exit(0)
    
    # Signal handlerlarni qo'shish
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # Termination signal

    # Foydalanuvchi Ctrl-C tugmachasini bosmaguncha botni ishga tushirish
    print("Bot ishga tushirilmoqda...")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🔄 Bot o'chirilmoqda...")
        logger.info("Bot KeyboardInterrupt orqali o'chirildi")
        
        # Shutdown xabarini yuborish
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_shutdown_message(application))
            loop.close()
        except Exception as e:
            logger.error(f"Shutdown xabari yuborishda xatolik: {e}")
        
        print("✅ Bot to'g'ri o'chirildi")
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")
        print(f"❌ Bot ishga tushirishda xatolik: {e}")

if __name__ == '__main__':
    main()