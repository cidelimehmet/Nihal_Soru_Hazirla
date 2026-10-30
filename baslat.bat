@echo off
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
title Tevfik Ileri IHO Soru Hazirlama Sistemi
color 1F

echo ======================================================================
echo    TEVFIK ILERI IMAM HATIP ORTAOKULU
echo    MEB 2026 OYSS SORU HAZIRLAMA VE YAZILI SINAV SISTEMI
echo ======================================================================
echo.

echo [1/3] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Bilgisayarinizda Python kurulu degil veya PATH'e eklenmemis!
    echo Lutfen python.org adresinden Python'i indirip kurunuz.
    echo Kurulum sirasinda 'Add Python to PATH' kutusunu isaretleyiniz.
    echo.
    pause
    exit /b
)

echo [2/3] Sistem kutuphaneleri kontrol ediliyor...
python -c "import fastapi, uvicorn, pymupdf" >nul 2>&1
if errorlevel 1 (
    echo Eksik paketler yukleniyor, lutfen bekleyiniz...
    pip install -r requirements.txt
)

echo [3/3] Soru Hazirlama Sistemi Baslatiliyor...
echo.
echo Sunucu calisiyor, sistem hazir oldugunda tarayiciniz otomatik acilacaktir...
echo (Programi kapatmak istediginizde bu pencereyi kapatabilirsiniz)
echo.

:: FastAPI sunucusunu baslat (sunucu hazir oldugu an tarayiciyi kendisi acar)
python main.py

echo.
echo Sunucu kapandi.
pause
