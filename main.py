import os
import json
import threading
from datetime import datetime
from tkinter import filedialog, messagebox, simpledialog
from tkinter import *
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from tkinter.ttk import Progressbar

SETTINGS_FILE = "settings.json"

WEEKDAY_SHORT_DE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

DEFAULT_EXPORT_PATHS = {
    "Gottesdienst": "gottesdienste",
    "Hochzeit": "hochzeiten",
    "Weissagung": "weissagungen"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"export_paths": DEFAULT_EXPORT_PATHS.copy()}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

settings = load_settings()

root = Tk()
root.title("WAV zu MP3 Konverter")
root.geometry("500x600")

Label(root, text="Wähle WAV-Dateien aus:").pack(pady=5)
file_listbox = Listbox(root, width=60)
file_listbox.pack(pady=5)

progress = Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
progress.pack(pady=10)

file_paths = []

def choose_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("WAV-Dateien", "*.wav")])
    file_listbox.delete(0, END)
    for path in file_paths:
        file_listbox.insert(END, os.path.basename(path))

Button(root, text="Dateien auswählen", command=choose_files).pack(pady=5)

def generate_album_name(content_type):
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    return f"{date_str} [{content_type}]"

def generate_folder_name(content_type):
    now = datetime.now()
    weekday = WEEKDAY_SHORT_DE[now.weekday()]
    base = now.strftime("%y%m%d") + weekday
    return f"{base} [{content_type}]" if content_type != "Sonstiges" else base

def open_settings_window():
    win = Toplevel(root)
    win.title("Einstellungen")
    win.geometry("500x400")

    Label(win, text="Künstlername:").pack()
    artist_entry = Entry(win)
    artist_entry.pack()
    artist_entry.insert(0, settings.get("metadata", {}).get("artist", ""))

    Label(win, text="Genre:").pack()
    genre_entry = Entry(win)
    genre_entry.pack()
    genre_entry.insert(0, settings.get("metadata", {}).get("genre", ""))

    Label(win, text="Kommentar:").pack()
    comment_entry = Entry(win)
    comment_entry.pack()
    comment_entry.insert(0, settings.get("metadata", {}).get("comment", ""))

    Label(win, text="Cover Pfad:").pack()
    cover_entry = Entry(win)
    cover_entry.pack()
    cover_entry.insert(0, settings.get("metadata", {}).get("cover", ""))

    Label(win, text="Standardverzeichnisse für Exporte:").pack(pady=10)

    entries = {}
    for key in DEFAULT_EXPORT_PATHS:
        Label(win, text=key).pack()
        entry = Entry(win)
        entry.pack()
        entry.insert(0, settings.get("export_paths", {}).get(key, DEFAULT_EXPORT_PATHS[key]))
        entries[key] = entry

    def save_all():
        settings["metadata"] = {
            "artist": artist_entry.get(),
            "genre": genre_entry.get(),
            "comment": comment_entry.get(),
            "cover": cover_entry.get()
        }
        settings["export_paths"] = {k: v.get() for k, v in entries.items()}
        save_settings(settings)
        messagebox.showinfo("Gespeichert", "Einstellungen wurden gespeichert.")
        win.destroy()

    Button(win, text="Speichern", command=save_all).pack(pady=10)

Button(root, text="Einstellungen öffnen", command=open_settings_window).pack(pady=5)

def confirm_metadata(content_type):
    meta = settings.get("metadata", {}).copy()
    meta["album"] = generate_album_name(content_type)
    meta["year"] = str(datetime.now().year)

    win = Toplevel(root)
    win.title("Metadaten bestätigen oder anpassen")
    win.geometry("400x500")

    Label(win, text="Künstlername:").pack()
    artist_entry = Entry(win)
    artist_entry.pack()
    artist_entry.insert(0, meta.get("artist", ""))

    Label(win, text="Albumname:").pack()
    album_entry = Entry(win)
    album_entry.pack()
    album_entry.insert(0, meta.get("album", ""))

    Label(win, text="Genre:").pack()
    genre_entry = Entry(win)
    genre_entry.pack()
    genre_entry.insert(0, meta.get("genre", ""))

    Label(win, text="Jahr:").pack()
    year_entry = Entry(win)
    year_entry.pack()
    year_entry.insert(0, meta.get("year", ""))

    Label(win, text="Kommentar:").pack()
    comment_entry = Entry(win)
    comment_entry.pack()
    comment_entry.insert(0, meta.get("comment", ""))

    Label(win, text="Cover-Pfad:").pack()
    cover_entry = Entry(win)
    cover_entry.pack()
    cover_entry.insert(0, meta.get("cover", ""))

    confirmed_data = {}

    def confirm():
        confirmed_data["artist"] = artist_entry.get()
        confirmed_data["album"] = album_entry.get()
        confirmed_data["genre"] = genre_entry.get()
        confirmed_data["year"] = year_entry.get()
        confirmed_data["comment"] = comment_entry.get()
        confirmed_data["cover"] = cover_entry.get()
        win.destroy()

    Button(win, text="Bestätigen", command=confirm).pack(pady=10)
    win.grab_set()
    root.wait_window(win)

    return confirmed_data if confirmed_data else None

def ask_content_type():
    win = Toplevel(root)
    win.title("Art des Inhaltes wählen")
    win.geometry("300x250")

    selected = StringVar(value="Gottesdienst")

    Label(win, text="Wähle Art des Inhalts:").pack(pady=10)
    for option in ["Gottesdienst", "Hochzeit", "Weissagung", "Sonstiges"]:
        Radiobutton(win, text=option, variable=selected, value=option).pack(anchor=W)

    confirmed = {}

    def confirm():
        confirmed["type"] = selected.get()
        win.destroy()

    Button(win, text="Bestätigen", command=confirm).pack(pady=10)
    win.grab_set()
    root.wait_window(win)

    return confirmed.get("type")

def convert():
    if not file_paths:
        messagebox.showerror("Fehler", "Keine Dateien ausgewählt.")
        return

    content_type = ask_content_type()
    if not content_type:
        return

    meta = confirm_metadata(content_type)
    if not meta:
        return

    if content_type in settings.get("export_paths", {}):
        base_dir = settings["export_paths"][content_type]
        os.makedirs(base_dir, exist_ok=True)
        folder_name = generate_folder_name(content_type)
        export_dir = os.path.join(base_dir, folder_name)
        os.makedirs(export_dir, exist_ok=True)
    else:
        export_dir = filedialog.askdirectory(title="Export-Ordner wählen")
        if not export_dir:
            return

    settings["last_export_dir"] = export_dir
    save_settings(settings)

    sorted_files = sorted(file_paths, key=lambda x: os.path.basename(x).lower())
    total = len(sorted_files)

    def run_conversion():
        for i, file in enumerate(sorted_files):
            try:
                audio = AudioSegment.from_wav(file)
                title = os.path.splitext(os.path.basename(file))[0]
                mp3_path = os.path.join(export_dir, f"{title}.mp3")
                audio.export(mp3_path, format="mp3")

                audiofile = EasyID3(mp3_path)
                audiofile["title"] = title
                audiofile["artist"] = meta["artist"]
                audiofile["album"] = meta["album"]
                audiofile["tracknumber"] = str(i + 1)
                audiofile["genre"] = meta.get("genre", "")
                audiofile["date"] = meta.get("year", "")
                audiofile["comment"] = meta.get("comment", "")
                audiofile.save()

                audiofile = ID3(mp3_path)
                with open(meta["cover"], "rb") as img:
                    audiofile.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc=u'Cover',
                        data=img.read()
                    ))
                audiofile.save()

                progress["value"] = (i + 1) / total * 100
                root.update_idletasks()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler bei Datei '{file}': {str(e)}")
                continue

        messagebox.showinfo("Fertig", "Konvertierung abgeschlossen!")

    threading.Thread(target=run_conversion).start()

Button(root, text="Konvertieren", command=convert).pack(pady=10)

root.mainloop()
