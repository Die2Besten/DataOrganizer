import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

fenster = tk.Tk()
fenster.title("Data Organizer")
fenster.geometry("300x300")
aktion_var = tk.StringVar(value="verschieben")

kopiere_radiobutton = tk.Radiobutton(fenster, text="Kopieren", variable=aktion_var, value="kopieren")
verschiebe_radiobutton = tk.Radiobutton(fenster, text="Verschieben", variable=aktion_var, value="verschieben")

kopiere_radiobutton.pack()
verschiebe_radiobutton.pack()

unterordner_var = tk.BooleanVar()

unterordner_check = tk.Checkbutton(
    fenster,
    text="Auch Unterordner sortieren",
    variable=unterordner_var
)
unterordner_check.pack()

struktur_var = tk.BooleanVar()

struktur_check = tk.Checkbutton(
    fenster,
    text="Ordnerstruktur erhalten",
    variable=struktur_var
)
struktur_check.pack()



def ordner_sort():
    pfad = filedialog.askdirectory()
    print("Ordner:", pfad)
    if not pfad:
        return
    
    dateien = [d for d in os.listdir(pfad) if os.path.isfile(os.path.join(pfad, d))]
    anzahl = len(dateien)

    progress["maximum"] = anzahl

    for datei in os.listdir(pfad):
        dateipfad = os.path.join(pfad, datei)
        dateiname = os.path.basename(dateipfad)

        if "." in dateiname and not dateiname.startswith("."):
         endung = dateiname.split('.')[-1].lower()
        else:
         endung = "andere"

        basisziel = os.path.join(pfad, f"{endung}_dateien")

        # Ordnerstruktur erhalten?
        if unterordner_var.get() and struktur_var.get():
         relativ_pfad = os.path.relpath(os.path.dirname(dateipfad), pfad)
         zielordner = os.path.join(basisziel, relativ_pfad)
        else:
         zielordner = basisziel

        # Ordner anlegen
        os.makedirs(zielordner, exist_ok=True)

        zielpfad = os.path.join(zielordner, dateiname)

        if unterordner_var.get():
           dateien = []
           for wurzel, _, dateinamen in os.walk(pfad):
            for d in dateinamen:
               dateipfad = os.path.join(wurzel, d)
               if os.path.isfile(dateipfad):
                  dateien.append(dateipfad)
               else:
                 dateien = [os.path.join(pfad, d) for d in os.listdir(pfad) if os.path.isfile(os.path.join(pfad, d))]


        if os.path.isfile(dateipfad) and "." in datei and not datei.startswith("."):
           dateiendung = datei.split('.')[-1].lower()

           zielordner = os.path.join(pfad, f"{dateiendung}_dateien")

        if not os.path.exists(zielordner):
            os.makedirs(zielordner)

        neuer_pfad = os.path.join(zielordner, datei)

        try:
            shutil.move(dateipfad, neuer_pfad)
            print(f"Verschoben: {datei} → {zielordner}")
        except Exception as e:
            print(f"Fehler beim Verschieben von {datei}: {e}")
        else:
           print(f"Übersprungen (keine Datei mit Endung): {datei}")

        if "." in datei and not datei.startswith("."):
          dateiendung = datei.split('.')[-1].lower()
        else:
            dateiendung = "andere"

        zielordner = os.path.join(pfad, f"{dateiendung}_dateien")
        if not os.path.exists(zielordner):
           os.makedirs(zielordner)

        zielpfad = os.path.join(zielordner, datei)

        try:
           if aktion_var.get() == "kopieren":
             shutil.copy2(dateipfad, zielpfad)
           else:
              shutil.move(dateipfad, zielpfad)
              print(f"{aktion_var.get().capitalize()}: {datei} → {zielordner}")

           progress["value"] += 1
           prozent = int((progress["value"] / anzahl) * 100)
           progress_label.config(text=f"{prozent}% abgeschlossen")
           fenster.update_idletasks()

        except Exception as e:
          print(f"Fehler bei {datei}: {e}")
 
        progress["value"] = 0
        progress_label.config(text="")

        print("Sortierung abgeschlossen")
        messagebox.showinfo("Fertig!", "Die Dateien wurden erfolgreich sortiert.")
        fenster.destroy()


button = tk.Button(fenster, text="Change Directory", command=ordner_sort)
button.pack(pady=20)

progress = ttk.Progressbar(fenster, orient="horizontal", length=200, mode="determinate")
progress.pack(pady=5)

progress = ttk.Progressbar(
    fenster,
    orient="horizontal",
    length=200,
    mode="determinate",
)
progress.pack(pady=5)


progress_label = tk.Label(fenster, text="")
progress_label.pack()

def zurücksetzen():
    aktion_var.set("verschieben")

reset_button = tk.Button(fenster, text="Zurücksetzen", command=zurücksetzen)
reset_button.pack(pady=5)


fenster.mainloop()