# Telegram Video Bot - Avtomatik deployment skripti (PowerShell)

Write-Host "🚀 Telegram Video Bot - Avtomatik Deployment" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Ishchi katalogni o'zgartirish
Set-Location -Path $PSScriptRoot

# Git o'rnatilganligini tekshirish
Write-Host "🔧 Git o'rnatilganligini tekshirish..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git o'rnatilmagan. Iltimos, avval Gitni o'rnating." -ForegroundColor Red
    exit 1
}

# Git holatini tekshirish
Write-Host "🔍 Git holatini tekshirish..." -ForegroundColor Yellow
try {
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Host "⚠️  O'zgarishlar aniqlandi:" -ForegroundColor Yellow
        Write-Host $gitStatus -ForegroundColor Yellow
    } else {
        Write-Host "✅ O'zgarishlar yo'q" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Git holatini tekshirishda xatolik yuz berdi." -ForegroundColor Red
    exit 1
}

# Barcha fayllarni qo'shish
Write-Host "➕ Barcha fayllarni qo'shish..." -ForegroundColor Yellow
try {
    git add .
    Write-Host "✅ Barcha fayllar qo'shildi" -ForegroundColor Green
} catch {
    Write-Host "❌ Fayllarni qo'shishda xatolik yuz berdi." -ForegroundColor Red
    exit 1
}

# Commit yaratish
Write-Host "📝 Commit yaratish..." -ForegroundColor Yellow
try {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Auto-deploy: $timestamp"
    git commit -m $commitMessage
    Write-Host "✅ Commit yaratildi: $commitMessage" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Commit yaratishda xatolik yuz berdi (ehtimol, o'zgarishlar yo'q)." -ForegroundColor Yellow
}

# Masofaviy repositoriyaga yuklash
Write-Host "🚀 O'zgarishlarni GitHub/GitLab'ga yuklash..." -ForegroundColor Yellow
try {
    # Avval yangilanishlarni olish
    Write-Host "📥 Yangilanishlarni olish..." -ForegroundColor Yellow
    git pull origin main
    
    # O'zgarishlarni yuklash
    git push origin main
    Write-Host "✅ O'zgarishlaringiz GitHub/GitLab'ga yuklandi!" -ForegroundColor Green
} catch {
    Write-Host "❌ O'zgarishlarni yuklashda xatolik yuz berdi." -ForegroundColor Red
    Write-Host "Iltimos, quyidagilarni tekshiring:" -ForegroundColor Yellow
    Write-Host "1. Internet ulanishini" -ForegroundColor Yellow
    Write-Host "2. Git konfiguratsiyasini" -ForegroundColor Yellow
    Write-Host "3. Repository ruxsatnomalarini" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🎉 Deployment muvaffaqiyatli yakunlandi!" -ForegroundColor Green
Write-Host "🌐 O'zgarishlaringiz GitHub/GitLab'ga yuklandi." -ForegroundColor Green