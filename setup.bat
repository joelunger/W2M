@echo off
:: setup.bat – startet setup.ps1 mit Adminrechten

:: PowerShell im Admin-Modus starten
PowerShell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0setup.ps1\"' -Verb RunAs"
