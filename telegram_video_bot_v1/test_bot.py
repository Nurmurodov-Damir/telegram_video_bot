#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Yuklab Olish Boti uchun test skripti
"""

import sys
import os

# src katalogini yo'lga qo'shing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Barcha kerakli modullar import qilinishini tekshirish."""
    try:
        import telegram
        print("✓ Telegram moduli muvaffaqiyatli import qilindi")
    except ImportError as e:
        print(f"✗ Telegram import qilishda xatolik: {e}")
        return False
    
    try:
        import yt_dlp
        print("✓ yt_dlp moduli muvaffaqiyatli import qilindi")
    except ImportError as e:
        print(f"✗ yt_dlp import qilishda xatolik: {e}")
        return False
    
    return True

def test_directory_structure():
    """Katalog strukturasining to'g'riligini tekshirish."""
    required_files = [
        'src/bot.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} mavjud")
        else:
            print(f"✗ {file_path} topilmadi")
            return False
    
    return True

def test_requirements():
    """Talablarni tekshirish faylida to'g'ri tarkib borligini tekshirish."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    try:
        with open(requirements_path, 'r') as f:
            content = f.read()
            
        if 'python-telegram-bot' in content:
            print("✓ python-telegram-bot talablarda topildi")
        else:
            print("✗ python-telegram-bot talablarda topilmadi")
            return False
            
        if 'yt-dlp' in content:
            print("✓ yt-dlp talablarda topildi")
        else:
            print("✗ yt-dlp talablarda topilmadi")
            return False
            
    except Exception as e:
        print(f"✗ requirements.txt faylini o'qishda xatolik: {e}")
        return False
    
    return True

def main():
    """Barcha testlarni ishga tushirish."""
    print("Telegram Video Yuklab Olish Boti uchun testlarni ishga tushirish...\n")
    
    tests = [
        ("Import Testlari", test_imports),
        ("Katalog Struktura Testlari", test_directory_structure),
        ("Talablar Testlari", test_requirements)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        if not test_func():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 Barcha testlar o'tdi!")
        print("\nTelegram Video Yuklab Olish Botingiz foydalanishga tayyor.")
        print("Ishga tushirish uchun:")
        print("1. Talablarni o'rnating: pip install -r requirements.txt")
        print("2. @BotFather orqali bot tokenini oling")
        print("3. Bot tokenini src/bot.py faylida yangilang")
        print("4. Botni ishga tushiring: python src/bot.py")
    else:
        print("❌ Ba'zi testlar o'tmadi. Yuqoridagi xatoliklarni tekshiring.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)