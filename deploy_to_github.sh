#!/bin/bash
# Telegram Video Bot - Avtomatik GitHub yuklash skripti
# Muallif: N.Damir - Senior Dasturchi

echo "=================================================="
echo "Telegram Video Bot - GitHub Yuklash"
echo "=================================================="

# Git holatini tekshirish
echo "Git holatini tekshirish..."
if ! git status >/dev/null 2>&1; then
    echo "Xato: Git repositoriyasi topilmadi!"
    echo "Iltimos, avval 'git init' buyrug'ini ishlating."
    exit 1
fi

# Barcha fayllarni qo'shish
echo "Barcha fayllarni qo'shish..."
git add .
if [ $? -ne 0 ]; then
    echo "Xato: Fayllarni qo'shishda muammo!"
    exit 1
fi

# Commit yaratish
echo "Commit yaratish..."
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Update: $timestamp"
if [ $? -ne 0 ]; then
    echo "Ogohlantirish: Hech qanday o'zgarish yo'q yoki commit xatosi."
fi

# Remote repositoriyani tekshirish
echo "Remote repositoriyani tekshirish..."
if ! git remote -v | grep -q "origin"; then
    echo "Xato: Remote repositoriya topilmadi!"
    echo "Iltimos, quyidagi buyruqni ishlating:"
    echo "git remote add origin YOUR_REPOSITORY_URL"
    exit 1
fi

# GitHub'ga yuklash
echo "GitHub'ga yuklash..."
git push origin main
if [ $? -ne 0 ]; then
    echo "Xato: GitHub'ga yuklashda muammo!"
    echo "Iltimos, internet ulanishini va repository ruxsatnomalarini tekshiring."
    exit 1
fi

echo ""
echo "=================================================="
echo "Muvaffaqiyatli yakunlandi!"
echo "=================================================="
echo "Kod GitHub'ga yuklandi: $timestamp"
echo ""
echo "Keyingi qadamlar:"
echo "1. GitHub repositoriyasini tekshiring"
echo "2. README.md faylini yangilang"
echo "3. Issues yoki Pull Requests oching"
echo ""
