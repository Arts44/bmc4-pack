@echo off
rem migrer-bmc4.bat - BMC-93 : lance bmc4-migration\migrer-bmc4.ps1 (Windows PowerShell 5.1)
rem AVANT le premier lancement de la nouvelle instance. Journal : migration-bmc4.log
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0bmc4-migration\migrer-bmc4.ps1"
