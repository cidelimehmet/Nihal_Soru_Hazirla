@echo off
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
title Tevfik Ileri IHO Soru Hazirlama Sistemi
color 1F

echo ======================================================================
echo    TEVFIK ILERI IMAM HATIP ORTAOKULU
echo    MEB 2026 OYSS SORU HAZIRLAMA VE YAZILI SINAV SISTEMI
echo ======================================================================
echo.

:: 1. Klasor icindeki tasinabilir (Portable) Python kontrolu (Python kurulu olmayan PC'ler icin)
if exist "%~dp0python_embed\python.exe" (
    set "PY_EXE=%~dp0python_embed\python.exe"
    echo [1/2] Klasor ici Tasinabilir Python (python_embed^) bulundu. Kurulum gerekmiyor!
    goto :RUN_SERVER
)

:: 2. Yedek: Sistemde kurulu Python kontrolu
echo [1/2] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] python_embed klasoru veya sistem Python'u bulunamadi!
    pause
    exit /b
)
set "PY_EXE=python"

"%PY_EXE%" -c "import fastapi, uvicorn, pymupdf, docx" >nul 2>&1
if errorlevel 1 (
    echo Eksik paketler yukleniyor, lutfen bekleyiniz...
    "%PY_EXE%" -m pip install -r requirements.txt
)

:RUN_SERVER
echo [2/2] Soru Hazirlama Sistemi Baslatiliyor...
echo.
echo Sunucu calisiyor, sistem hazir oldugunda tarayiciniz otomatik acilacaktir...
echo (Programi kapatmak istediginizde bu pencereyi kapatabilirsiniz)
echo.

"%PY_EXE%" main.py

echo.
echo Sunucu kapandi.
pause
