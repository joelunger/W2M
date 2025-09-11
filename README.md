# 🎵 WAV zu MP3 Konverter

Ein einfaches, benutzerfreundliches Python-Tool mit grafischer Oberfläche (Tkinter), das WAV-Dateien in MP3-Dateien konvertiert. Es unterstützt automatische Metadaten-Erstellung (Künstler, Album, Titel, Tracknummer) und fügt sogar ein Cover-Bild ein. Alle Dateien werden automatisch alphabetisch sortiert.

---

## ✅ Features

- 📂 Mehrere WAV-Dateien auswählen
- 📝 Standard-Metadaten definieren (Künstler, Album, Cover)
- 🧠 Vorschau & Bearbeitung der Metadaten vor der Konvertierung
- 🔄 Automatische Sortierung nach Dateinamen
- 🖼️ Cover-Bild einfügen
- 💾 Einstellungen werden gespeichert (Metadaten & letzter Export-Ordner)
- 📊 Fortschrittsbalken während der Konvertierung

---

## 🛠️ Setup

# Automatisches Setup starten
Windows-Nutzer können einfach ````setup.bat```` ausführen – es installiert:
-	Python (falls nicht vorhanden)
-	Virtuelle Umgebung
-	Alle benötigten Python-Pakete (pydub, mutagen)
-	FFmpeg (wird automatisch heruntergeladen & eingebunden)

# Alternativ: Manuell installieren
1. Stelle sicher, dass Python 3.11 oder neuer installiert ist.
2. Virtuelle Umgebung erstellen und aktivieren:
````python -m venv .venv````
````.venv\Scripts\activate````

3. Abhängigkeiten installieren:
````pip install pydub mutagen````

4. FFmpeg herunterladen und den bin-Ordner zur PATH-Umgebungsvariable hinzufügen.

# 🚀 Anwendung starten
1. main.py ausführen:
````.venv\Scripts\python.exe main.py````

2. WAV-Dateien auswählen und konvertieren.


#📁 Projektstruktur
````
📦 wav-to-mp3-converter
├── setup.bat              # Batch-Datei zum Starten der Installation
├── setup.ps1              # PowerShell-Setupscript
├── settings.json          # Gespeicherte Einstellungen (automatisch erzeugt)
├── main.py                # Hauptprogramm mit GUI
└── README.md              # Diese Datei
````
#ℹ️ Hinweise
Nur .wav-Dateien werden akzeptiert.

Cover muss eine .jpg- oder .jpeg-Datei sein.

Export erfolgt im .mp3-Format, benannt nach dem Originaldateinamen.

Metadaten können vor jeder Konvertierung überprüft und angepasst werden.
