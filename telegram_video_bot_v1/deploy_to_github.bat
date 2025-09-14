@echo off
REM Telegram Video Bot - Avtomatik GitHub yuklash skripti
REM Muallif: N.Damir - Senior Dasturchi

echo ==================================================
echo Telegram Video Bot - GitHub Yuklash
echo ==================================================

REM Git holatini tekshirish
echo Git holatini tekshirish...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo Xato: Git repositoriyasi topilmadi!
    echo Iltimos, avval 'git init' buyrug'ini ishlating.
    pause
    exit /b 1
)

REM Barcha fayllarni qo'shish
echo Barcha fayllarni qo'shish...
git add .
if %errorlevel% neq 0 (
    echo Xato: Fayllarni qo'shishda muammo!
    pause
    exit /b 1
)

REM Commit yaratish
echo Commit yaratish...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Update: %timestamp%"
if %errorlevel% neq 0 (
    echo Ogohlantirish: Hech qanday o'zgarish yo'q yoki commit xatosi.
)

REM Remote repositoriyani tekshirish
echo Remote repositoriyani tekshirish...
git remote -v | findstr "origin" >nul 2>&1
if %errorlevel% neq 0 (
    echo Xato: Remote repositoriya topilmadi!
    echo Iltimos, quyidagi buyruqni ishlating:
    echo git remote add origin YOUR_REPOSITORY_URL
    pause
    exit /b 1
)

REM GitHub'ga yuklash
echo GitHub'ga yuklash...
git push origin main
if %errorlevel% neq 0 (
    echo Xato: GitHub'ga yuklashda muammo!
    echo Iltimos, internet ulanishini va repository ruxsatnomalarini tekshiring.
    pause
    exit /b 1
)

echo.
echo ==================================================
echo Muvaffaqiyatli yakunlandi!
echo ==================================================
echo Kod GitHub'ga yuklandi: %timestamp%
echo.
echo Keyingi qadamlar:
echo 1. GitHub repositoriyasini tekshiring
echo 2. README.md faylini yangilang
echo 3. Issues yoki Pull Requests oching
echo.
pause
