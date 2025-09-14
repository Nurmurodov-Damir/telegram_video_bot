#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Bot - Avtomatik deployment skripti
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command):
    """Buyruqni ishga tushirish va natijani qaytarish."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Xato: {e.stderr}")
        return None

def check_git_status():
    """Git holatini tekshirish."""
    print("🔍 Git holatini tekshirish...")
    status = run_command("git status --porcelain")
    if status is None:
        return False
    
    if status:
        print("⚠️  O'zgarishlar aniqlandi:")
        print(status)
    else:
        print("✅ O'zgarishlar yo'q")
    
    return True

def add_and_commit():
    """Barcha fayllarni qo'shish va commit qilish."""
    print("➕ Barcha fayllarni qo'shish...")
    if run_command("git add .") is None:
        return False
    
    # Hozirgi vaqtni olish
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Auto-deploy: {timestamp}"
    
    print(f"📝 Commit xabari: {commit_message}")
    if run_command(f'git commit -m "{commit_message}"') is None:
        # Agar hech narsa commit qilinmasa, bu xato emas
        pass
    
    return True

def push_to_remote():
    """O'zgarishlarni masofaviy repositoriyaga yuklash."""
    print("🚀 O'zgarishlarni GitHub/GitLab'ga yuklash...")
    
    # Avval yangilanishlarni olish
    print("📥 Yangilanishlarni olish...")
    run_command("git pull origin main")
    
    # O'zgarishlarni yuklash
    if run_command("git push origin main") is None:
        return False
    
    return True

def main():
    """Asosiy funksiya."""
    print("🚀 Telegram Video Bot - Avtomatik Deployment")
    print("=" * 50)
    
    # Ishchi katalogni o'zgartirish
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Git o'rnatilganligini tekshirish
    print("🔧 Git o'rnatilganligini tekshirish...")
    if run_command("git --version") is None:
        print("❌ Git o'rnatilmagan. Iltimos, avval Gitni o'rnating.")
        return False
    
    # Git holatini tekshirish
    if not check_git_status():
        return False
    
    # Fayllarni qo'shish va commit qilish
    if not add_and_commit():
        return False
    
    # Masofaviy repositoriyaga yuklash
    if not push_to_remote():
        return False
    
    print("\n✅ Deployment muvaffaqiyatli yakunlandi!")
    print("🌐 O'zgarishlaringiz GitHub/GitLab'ga yuklandi.")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)