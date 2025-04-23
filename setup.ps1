# setup.ps1 – Projektabhängigkeiten für WAV-to-MP3-Konverter installieren

# Python installieren, falls nicht vorhanden
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python wird installiert..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe" -OutFile "$env:TEMP\python-installer.exe"
    Start-Process -Wait "$env:TEMP\python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0"
    Remove-Item "$env:TEMP\python-installer.exe"
} else {
    Write-Host "✅ Python ist bereits installiert."
}

# Sicherstellen, dass pip funktioniert
python -m ensurepip --upgrade

# Virtuelle Umgebung erstellen
if (-not (Test-Path ".venv")) {
    Write-Host "Virtuelle Umgebung wird erstellt..."
    python -m venv .venv
}
. .venv\Scripts\Activate.ps1

# Benötigte Pakete installieren
pip install --upgrade pip
pip install pydub mutagen

# ffmpeg installieren
$ffmpegZip = "$env:TEMP\ffmpeg.zip"
$ffmpegDir = "$PWD\ffmpeg"
$binPath = "$ffmpegDir\ffmpeg-*-essentials_build\bin"

if (-not (Test-Path $ffmpegDir)) {
    Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $ffmpegZip
    Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegDir
    Remove-Item $ffmpegZip
    Write-Host "FFmpeg wurde installiert."
} else {
    Write-Host "FFmpeg ist bereits vorhanden."
}

# Pfad zum ffmpeg/bin dauerhaft hinzufügen (User-spezifisch)
$realBinPath = Get-ChildItem "$ffmpegDir\ffmpeg-*-essentials_build\bin" | Select-Object -First 1
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$($realBinPath.FullName)", [EnvironmentVariableTarget]::User)

Write-Host "`n✅ Einrichtung abgeschlossen. Starte jetzt dein Python-Programm!"
pause
