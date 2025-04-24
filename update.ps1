# URL zur neuesten Version
$DownloadURL = "https://fcco.netlify.app/update/main.pyw"

# Zielpfade
$DestinationFolder = "$PSScriptRoot\App"
$DestinationFile = "$DestinationFolder\main.pyw"
$BackupFile = "$DestinationFolder\main_backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').pyw"

# Schritt 1: Zielordner prüfen und erstellen
Write-Host "Prüfe den Zielordner..."
if (-not (Test-Path $DestinationFolder)) {
    New-Item -ItemType Directory -Path $DestinationFolder -Force
    Write-Host "Zielordner wurde erstellt: $DestinationFolder" -ForegroundColor Green
} else {
    Write-Host "Zielordner existiert bereits: $DestinationFolder" -ForegroundColor Cyan
}

# Schritt 2: Sicherung der alten Datei
Write-Host "Prüfe vorhandene Datei für Backup..."
if (Test-Path $DestinationFile) {
    Rename-Item -Path $DestinationFile -NewName $BackupFile -Force
    Write-Host "Alte Datei wurde gesichert als: $BackupFile" -ForegroundColor Yellow
} else {
    Write-Host "Keine bestehende Datei gefunden. Kein Backup erforderlich." -ForegroundColor Cyan
}

# Schritt 3: Neue Version herunterladen
Write-Host "Lade die neue Version herunter..."
try {
    Invoke-WebRequest -Uri $DownloadURL -OutFile $DestinationFile -UseBasicParsing
    Write-Host "Neue Version erfolgreich heruntergeladen: $DestinationFile" -ForegroundColor Green
} catch {
    Write-Host "Fehler beim Herunterladen: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Bitte überprüfe die URL oder den Zielpfad." -ForegroundColor Yellow
    Pause
    exit 1
}

# Schritt 4: Abschlussmeldung und Pause
Write-Host "Update abgeschlossen! Die neue Version wurde erfolgreich installiert." -ForegroundColor Green
Write-Host "Drücken Sie eine beliebige Taste, um das Fenster zu schließen..."
Pause
