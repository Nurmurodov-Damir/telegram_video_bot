#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Bot - Sozlash skripti
"""

import os
import sys

def check_python_version():
    """Python versiyasini tekshirish."""
    if sys.version_info < (3, 9):
        print("❌ Xato: Python 3.9 yoki yuqori versiyasi talab qilinadi!")
        print(f"Sizning Python versiyangiz: {sys.version}")
        return False
    return True

def create_env_file():
    """.env faylini yaratish yoki tekshirish."""
    env_path = '.env'
    
    if os.path.exists(env_path):
        print("✓ .env fayli mavjud")
        # Faylni o'qib, token mavjudligini tekshirish
        with open(env_path, 'r') as f:
            content = f.read()
            
        if 'YOUR_BOT_TOKEN_HERE' in content:
            print("⚠️  Eslatma: .env faylida hali bot tokeni sozlanmagan")
            print("   Iltimos, TELEGRAM_BOT_TOKEN qiymatini haqiqiy token bilan almashtiring")
        else:
            print("✓ .env faylida bot tokeni mavjud")
        return True
    
    # .env faylini yaratish
    env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Video Download Settings
MAX_VIDEO_DURATION=600
MAX_VIDEO_SIZE=52428800
DOWNLOAD_DIR=downloads

# Logging Settings
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✓ .env fayli yaratildi")
        print("⚠️  Eslatma: TELEGRAM_BOT_TOKEN qiymatini haqiqiy token bilan almashtiring")
        return True
    except Exception as e:
        print(f"❌ .env faylini yaratishda xatolik: {e}")
        return False

def check_requirements():
    """requirements.txt faylini tekshirish."""
    req_path = 'requirements.txt'
    
    if not os.path.exists(req_path):
        print("❌ requirements.txt fayli topilmadi!")
        return False
    
    try:
        with open(req_path, 'r') as f:
            content = f.read()
            
        required_packages = ['python-telegram-bot', 'yt-dlp', 'python-dotenv']
        missing_packages = []
        
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
                
        if missing_packages:
            print(f"⚠️  Quyidagi paketlar requirements.txt da topilmadi: {', '.join(missing_packages)}")
        else:
            print("✓ Barcha kerakli paketlar requirements.txt da mavjud")
        return True
    except Exception as e:
        print(f"❌ requirements.txt faylini o'qishda xatolik: {e}")
        return False

def show_setup_instructions():
    """Sozlash ko'rsatmalarini ko'rsatish."""
    print("\n🔧 Sozlash ko'rsatmalari:")
    print("=" * 40)
    print("1. Telegramda @BotFather ga kiring")
    print("2. Yangi bot yarating (/newbot buyrug'i)")
    print("3. BotFather dan bot tokenini oling")
    print("4. .env faylini oching")
    print("5. YOUR_BOT_TOKEN_HERE ni haqiqiy token bilan almashtiring")
    print("6. Botni ishga tushiring: python run_bot.py")

def main():
    """Asosiy funksiya."""
    print("🚀 Telegram Video Yuklab Olish Botini Sozlash")
    print("=" * 50)
    
    # Ishchi katalogni o'zgartirish
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Tekshiruvlarni bajarish
    checks = [
        ("Python versiyasi", check_python_version),
        (".env fayli", create_env_file),
        ("Talablarni tekshirish", check_requirements)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name} tekshirilmoqda...")
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n✅ Barcha tekshiruvlar muvaffaqiyatli o'tdi!")
        show_setup_instructions()
        print("\n💡 Botni ishga tushirish uchun: python run_bot.py")
    else:
        print("\n❌ Ba'zi tekshiruvlardan o'tmadi!")
        print("Yuqoridagi xatoliklarni tuzating va qayta urinib ko'ring.")

if __name__ == '__main__':
    main()