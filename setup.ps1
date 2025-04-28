# setup.ps1 – Projektabhängigkeiten für WAV-to-MP3-Konverter installieren

# === Python Installation ===
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python wird installiert..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe" -OutFile "$env:TEMP\python-installer.exe"
    Start-Process -Wait "$env:TEMP\python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0"
    Remove-Item "$env:TEMP\python-installer.exe"
} else {
    Write-Host "✅ Python ist bereits installiert."
}

# === Virtuelle Umgebung & Pakete ===
python -m ensurepip --upgrade

if (-not (Test-Path ".venv")) {
    Write-Host "Virtuelle Umgebung wird erstellt..."
    python -m venv .venv
}
. .venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install pydub mutagen

# === FFmpeg Installation ===
$ffmpegZip = "$env:TEMP\ffmpeg.zip"
$ffmpegDir = "$PWD\ffmpeg"

if (-not (Test-Path $ffmpegDir)) {
    Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $ffmpegZip
    Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegDir
    Remove-Item $ffmpegZip
    Write-Host "FFmpeg wurde installiert."
} else {
    Write-Host "FFmpeg ist bereits vorhanden."
}

$realBinPath = Get-ChildItem "$ffmpegDir\ffmpeg-*-essentials_build\bin" | Select-Object -First 1
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$($realBinPath.FullName)", [EnvironmentVariableTarget]::User)

# === Ordner verschieben ===
$sourceFolder = Split-Path -Parent $MyInvocation.MyCommand.Path
$folderName = Split-Path -Leaf $sourceFolder
$destinationFolder = "C:\Program Files\$folderName"

Write-Host "Projekt wird verschoben nach 'C:\Program Files'..."
if (-not (Test-Path $destinationFolder)) {
    Move-Item -Path $sourceFolder -Destination "C:\Program Files"
    Write-Host "✅ Projekt verschoben."
} else {
    Write-Host "⚠️ Zielordner existiert bereits. Überspringe Verschieben."
}

# === Desktop-Verknüpfung erstellen ===
$desktopPath = [Environment]::GetFolderPath("Desktop")
$linkPath = Join-Path $desktopPath "fcco.pyw.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($linkPath)
$shortcut.TargetPath = "C:\Program Files\$folderName\main.pyw"
$shortcut.WorkingDirectory = "C:\Program Files\$folderName"
$shortcut.Save()

Write-Host "`n✅ Einrichtung abgeschlossen. Verknüpfung wurde erstellt!"
pause
