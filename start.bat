@echo off
title VoiceMimic - Sistema de Clonagem de Voz

REM Verifica se o ambiente virtual existe
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Instala as dependências se necessário
pip list | findstr /i "TTS" > nul
if %errorlevel% neq 0 (
    echo Instalando dependências...
    pip install -r requirements.txt
)

REM Inicia o servidor
echo Iniciando servidor...
uvicorn main:app --reload --port 8085

REM Mantém a janela aberta se ocorrer um erro
if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro. Pressione qualquer tecla para sair...
    pause > nul
)