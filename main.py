import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pdf_generator import create_invoice_pdf
import json
import os
from datetime import date
from utils import get_next_rechnungsnummer
from kunden_db import (
    init_db, get_alle_kunden, get_kunde_by_id,
    add_kunde, update_kunde
)
from artikel_db import (
    init_artikel_db, get_alle_artikel, get_artikel_by_id,
    add_artikel, update_artikel, delete_artikel
)

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_data(data, rechnungsnummer):
    fname = f"{DATA_DIR}/rechnung_{rechnungsnummer}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def refresh_kundenliste():
    global kunden_liste, kunden_dict
    kunden_liste = get_alle_kunden()
    kunden_dict = {f"{k[1]} ({k[2]}, {k[3]})": k[0] for k in kunden_liste}
    filter_kundenliste()  # Filter anwenden, falls ein Suchbegriff besteht

def filter_kundenliste(event=None):
    search = entry_suche.get().lower()
    filtered = [
        f"{k[1]} ({k[2]}, {k[3]})"
        for k in kunden_liste
        if search in k[1].lower() or search in (k[2] or "").lower() or search in (k[3] or "").lower()
    ]
    combo_kunden['values'] = filtered
    if not search and filtered:
        combo_kunden.current(0)
    else:
        combo_kunden.set('')

def kunde_ausgewaehlt(event=None):
    key = kunden_var.get()
    if key and key in kunden_dict:
        kunden_id = kunden_dict[key]
        daten = get_kunde_by_id(kunden_id)
        if daten:
            entry_name.delete(0, tk.END)
            entry_name.insert(0, daten[0])
            entry_strasse.delete(0, tk.END)
            entry_strasse.insert(0, daten[1])
            entry_plzort.delete(0, tk.END)
            entry_plzort.insert(0, daten[2])
            entry_geb.delete(0, tk.END)
            entry_geb.insert(0, daten[3])
            global akt_kunden_id
            akt_kunden_id = kunden_id
        else:
            akt_kunden_id = None
    else:
        akt_kunden_id = None

def kunde_hinzufuegen():
    name = simpledialog.askstring("Kunde hinzufügen", "Name:")
    if not name:
        return
    strasse = simpledialog.askstring("Kunde hinzufügen", "Straße + Nr:")
    plzort = simpledialog.askstring("Kunde hinzufügen", "PLZ + Ort:")
    geburtstag = simpledialog.askstring("Kunde hinzufügen", "Geburtsdatum:")
    add_kunde(name, strasse, plzort, geburtstag)
    refresh_kundenliste()
    messagebox.showinfo("Kunde hinzugefügt", f"Kunde '{name}' wurde hinzugefügt.")

def kunde_bearbeiten():
    key = kunden_var.get()
    if not key or key not in kunden_dict:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie zuerst einen Kunden aus.")
        return
    kunden_id = kunden_dict[key]
    daten = get_kunde_by_id(kunden_id)
    if not daten:
        messagebox.showerror("Fehler", "Kunde nicht gefunden!")
        return
    name = simpledialog.askstring("Kunde bearbeiten", "Name:", initialvalue=daten[0])
    if not name:
        return
    strasse = simpledialog.askstring("Kunde bearbeiten", "Straße + Nr:", initialvalue=daten[1])
    plzort = simpledialog.askstring("Kunde bearbeiten", "PLZ + Ort:", initialvalue=daten[2])
    geburtstag = simpledialog.askstring("Kunde bearbeiten", "Geburtsdatum:", initialvalue=daten[3])
    update_kunde(kunden_id, name, strasse, plzort, geburtstag)
    refresh_kundenliste()
    messagebox.showinfo("Kunde aktualisiert", f"Kunde '{name}' wurde bearbeitet.")
    if kunden_var.get() == key:
        kunde_ausgewaehlt()

# --- Artikelfunktionen ---

def refresh_artikelliste():
    global artikel_liste, artikel_dict
    artikel_liste = get_alle_artikel()
    artikel_dict = {f"{a[1]} ({a[2]}€, {a[3]}%)": a[0] for a in artikel_liste}
    combo_artikel['values'] = list(artikel_dict.keys())

def artikel_ausgewaehlt(event=None):
    key = artikel_var.get()
    if key and key in artikel_dict:
        artikel_id = artikel_dict[key]
        daten = get_artikel_by_id(artikel_id)
        if daten:
            entry_artikelpreis.delete(0, tk.END)
            entry_artikelpreis.insert(0, str(daten[1]))
            entry_artikelmwst.delete(0, tk.END)
            entry_artikelmwst.insert(0, str(daten[2]))
        else:
            entry_artikelpreis.delete(0, tk.END)
            entry_artikelmwst.delete(0, tk.END)
    else:
        entry_artikelpreis.delete(0, tk.END)
        entry_artikelmwst.delete(0, tk.END)

def artikel_hinzufuegen():
    name = simpledialog.askstring("Artikel hinzufügen", "Name:")
    if not name:
        return
    preis = simpledialog.askfloat("Artikel hinzufügen", "Preis (€):")
    if preis is None:
        return
    mwst = simpledialog.askfloat("Artikel hinzufügen", "MwSt (%):")
    if mwst is None:
        return
    add_artikel(name, preis, mwst)
    refresh_artikelliste()
    messagebox.showinfo("Artikel hinzugefügt", f"Artikel '{name}' wurde hinzugefügt.")

def artikel_bearbeiten():
    key = artikel_var.get()
    if not key or key not in artikel_dict:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie zuerst einen Artikel aus.")
        return
    artikel_id = artikel_dict[key]
    daten = get_artikel_by_id(artikel_id)
    if not daten:
        messagebox.showerror("Fehler", "Artikel nicht gefunden!")
        return
    name = simpledialog.askstring("Artikel bearbeiten", "Name:", initialvalue=daten[0])
    if not name:
        return
    preis = simpledialog.askfloat("Artikel bearbeiten", "Preis (€):", initialvalue=daten[1])
    if preis is None:
        return
    mwst = simpledialog.askfloat("Artikel bearbeiten", "MwSt (%):", initialvalue=daten[2])
    if mwst is None:
        return
    update_artikel(artikel_id, name, preis, mwst)
    refresh_artikelliste()
    messagebox.showinfo("Artikel aktualisiert", f"Artikel '{name}' wurde bearbeitet.")

def artikel_loeschen():
    key = artikel_var.get()
    if not key or key not in artikel_dict:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie zuerst einen Artikel aus.")
        return
    artikel_id = artikel_dict[key]
    if messagebox.askyesno("Artikel löschen", "Wirklich löschen?"):
        delete_artikel(artikel_id)
        refresh_artikelliste()
        messagebox.showinfo("Artikel gelöscht", "Artikel wurde gelöscht.")

def artikel_zu_tabelle_hinzufuegen():
    key = artikel_var.get()
    if not key or key not in artikel_dict:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie zuerst einen Artikel aus.")
        return
    artikel_id = artikel_dict[key]
    name = key.split(' (')[0]
    try:
        preis = float(entry_artikelpreis.get())
        mwst = float(entry_artikelmwst.get())
        # Neue Methode: Leistungsdaten als Liste (ein Datum pro Zeile)
        leistungsdaten = [d.strip() for d in entry_leistungsdatum.get("1.0", tk.END).splitlines() if d.strip()]
        anzahl = len(leistungsdaten)
        if anzahl == 0:
            raise ValueError
    except Exception:
        messagebox.showerror("Fehler", "Bitte gültige Werte für Preis, MwSt und mindestens ein Leistungsdatum angeben.")
        return
    artikel = {
        "artikel_id": artikel_id,
        "name": name,
        "preis": preis,
        "mwst": mwst,
        "anzahl": anzahl,
        "leistungsdaten": leistungsdaten
    }
    artikel_liste_rechnung.append(artikel)
    datum_anzeige = ", ".join(leistungsdaten) if anzahl <= 3 else f"{leistungsdaten[0]}, ..."
    artikel_tabelle.insert("", "end", values=(name, datum_anzeige, preis, mwst, anzahl))
    entry_anzahl.delete(0, tk.END)
    entry_anzahl.insert(0, "1")
    entry_leistungsdatum.delete("1.0", tk.END)

def artikel_von_tabelle_entfernen():
    selected = artikel_tabelle.selection()
    if not selected:
        return
    idx = artikel_tabelle.index(selected[0])
    artikel_tabelle.delete(selected)
    del artikel_liste_rechnung[idx]

def on_submit():
    rechnungsnummer = get_next_rechnungsnummer()
    data = {
        "rechnungsnummer": rechnungsnummer,
        "kunde_name": entry_name.get(),
        "kunde_strasse": entry_strasse.get(),
        "kunde_plzort": entry_plzort.get(),
        "kunde_geburtstag": entry_geb.get(),
        "artikel_liste": artikel_liste_rechnung,
        "privatrezept": var_privatrezept.get(),
        "verordnungsdatum": entry_verordnung.get(),
        "diagnose": entry_diagnose.get(),
        "bezahlt": var_bezahlt.get()
    }
    # Pflichtfelder prüfen
    if not data['kunde_name'] or not artikel_liste_rechnung:
        messagebox.showerror("Fehler", "Bitte füllen Sie alle Pflichtfelder aus und fügen Sie mindestens einen Artikel hinzu!")
        return
    save_data(data, rechnungsnummer)
    pdf_path = create_invoice_pdf(data, rechnungsnummer)
    messagebox.showinfo("Erfolg", f"Rechnung erstellt: {pdf_path}")

# ---- Init DBs ----
init_db()
init_artikel_db()

root = tk.Tk()
root.title("Rechnungssoftware")

frame = ttk.Frame(root, padding=15)
frame.grid()

row = 0

# Kundendaten-Überschrift
ttk.Label(frame, text="Kundendaten", font=("Arial", 12, "bold")).grid(column=0, row=row, columnspan=6, pady=5)
row += 1

# Kunde suchen
ttk.Label(frame, text="Kunde suchen:").grid(column=0, row=row, sticky="e")
entry_suche = ttk.Entry(frame, width=30)
entry_suche.grid(column=1, row=row, sticky="w")
row += 1

# Kunde auswählen und Buttons in einer Zeile
ttk.Label(frame, text="Kunde auswählen:").grid(column=0, row=row, sticky="e")
kunden_liste = get_alle_kunden()
kunden_dict = {f"{k[1]} ({k[2]}, {k[3]})": k[0] for k in kunden_liste}
kunden_var = tk.StringVar()
combo_kunden = ttk.Combobox(frame, textvariable=kunden_var, values=list(kunden_dict.keys()), state="readonly", width=30)
combo_kunden.grid(column=1, row=row, sticky="w")
combo_kunden.bind("<<ComboboxSelected>>", kunde_ausgewaehlt)
row += 1
ttk.Button(frame, text="Neu", command=kunde_hinzufuegen).grid(column=1, row=row, sticky="w", padx=(2, 0))
ttk.Button(frame, text="Bearbeiten", command=kunde_bearbeiten).grid(column=1, row=row, sticky="", padx=(2, 0))
row += 1

# Kundendaten Felder
ttk.Label(frame, text="Name:").grid(column=0, row=row, sticky="e")
entry_name = ttk.Entry(frame, width=30)
entry_name.grid(column=1, row=row, sticky="w")
row += 1

ttk.Label(frame, text="Straße + Nr:").grid(column=0, row=row, sticky="e")
entry_strasse = ttk.Entry(frame, width=30)
entry_strasse.grid(column=1, row=row, sticky="w")
row += 1

ttk.Label(frame, text="PLZ + Ort:").grid(column=0, row=row, sticky="e")
entry_plzort = ttk.Entry(frame, width=30)
entry_plzort.grid(column=1, row=row, sticky="w")
row += 1

ttk.Label(frame, text="Geburtsdatum:").grid(column=0, row=row, sticky="e")
entry_geb = ttk.Entry(frame, width=30)
entry_geb.grid(column=1, row=row, sticky="w")
row += 2

# Artikeldaten-Überschrift
ttk.Label(frame, text="Artikeldaten", font=("Arial", 12, "bold")).grid(column=0, row=row, columnspan=6, pady=5)
row += 1

# Artikel auswählen und Buttons in einer Zeile
ttk.Label(frame, text="Artikel auswählen:").grid(column=0, row=row, sticky="e")
artikel_liste = get_alle_artikel()
artikel_dict = {f"{a[1]} ({a[2]}€, {a[3]}%)": a[0] for a in artikel_liste}
artikel_var = tk.StringVar()
combo_artikel = ttk.Combobox(frame, textvariable=artikel_var, values=list(artikel_dict.keys()), state="readonly", width=30)
combo_artikel.grid(column=1, row=row, sticky="w")
combo_artikel.bind("<<ComboboxSelected>>", artikel_ausgewaehlt)
row += 1
ttk.Button(frame, text="Neu", command=artikel_hinzufuegen).grid(column=1, row=row, sticky="w", padx=(2, 0))
ttk.Button(frame, text="Löschen", command=artikel_loeschen).grid(column=1, row=row, sticky="e",  padx=(2, 0))
ttk.Button(frame, text="Bearbeiten", command=artikel_bearbeiten).grid(column=1, row=row, sticky="", padx=(2, 0))

row += 1

# Artikeldaten Felder
ttk.Label(frame, text="Preis (€):").grid(column=0, row=row, sticky="e")
entry_artikelpreis = ttk.Entry(frame, width=10)
entry_artikelpreis.grid(column=1, row=row, sticky="w")
row += 1
ttk.Label(frame, text="MwSt (%):").grid(column=0, row=row, sticky="e")
entry_artikelmwst = ttk.Entry(frame, width=10)
entry_artikelmwst.grid(column=1, row=row, sticky="w")
row += 1
ttk.Label(frame, text="Anzahl:").grid(column=0, row=row, sticky="e")
entry_anzahl = ttk.Entry(frame, width=5)
entry_anzahl.insert(0, "1")
entry_anzahl.grid(column=1, row=row, sticky="w")
row += 1

ttk.Label(frame, text="Leistungsdaten (ein Datum pro Zeile):").grid(column=0, row=row, sticky="e")
entry_leistungsdatum = tk.Text(frame, width=20, height=3)
entry_leistungsdatum.grid(column=1, row=row, sticky="w")
row += 1
ttk.Button(frame, text="Artikel hinzufügen", command=artikel_zu_tabelle_hinzufuegen).grid(column=1, row=row, columnspan=4, pady=5, sticky="w")
ttk.Button(frame, text="Entfernen", command=artikel_von_tabelle_entfernen).grid(column=1, row=row, columnspan=4, pady=5, sticky="")
row += 1

# Tabelle für Artikel in Rechnung
artikel_tabelle = ttk.Treeview(frame, columns=("Name", "Leistungsdatum", "Preis", "MwSt", "Anzahl"), show="headings", height=5)
artikel_tabelle.grid(column=0, row=row, columnspan=5, pady=3, sticky="w")
for col in ("Name", "Leistungsdatum", "Preis", "MwSt", "Anzahl"):
    artikel_tabelle.heading(col, text=col)
    artikel_tabelle.column("Name", width=150)
    artikel_tabelle.column("Leistungsdatum", width=150)
    artikel_tabelle.column("Preis", width=80)
    artikel_tabelle.column("MwSt", width=60)
    artikel_tabelle.column("Anzahl", width=60)
row += 2

artikel_liste_rechnung = []

# Rezeptdaten-Überschrift
ttk.Label(frame, text="Rezeptdaten", font=("Arial", 12, "bold")).grid(column=0, row=row, columnspan=6, pady=5)
row += 1

# Privatrezept-Checkbox
var_privatrezept = tk.BooleanVar()
ttk.Checkbutton(frame, text="Privatrezept", variable=var_privatrezept).grid(column=1, row=row, columnspan=2, sticky="w")
row += 1

ttk.Label(frame, text="Verordnungsdatum:").grid(column=0, row=row, sticky="e")
entry_verordnung = ttk.Entry(frame, width=30)
entry_verordnung.grid(column=1, row=row, sticky="w")
row += 1

ttk.Label(frame, text="Diagnose:").grid(column=0, row=row, sticky="e")
entry_diagnose = ttk.Entry(frame, width=30)
entry_diagnose.grid(column=1, row=row, sticky="w")
row += 2

var_bezahlt = tk.BooleanVar()
ttk.Checkbutton(frame, text="Bereits bezahlt?", variable=var_bezahlt).grid(column=1, row=row, columnspan=2, sticky="w")
row += 2

ttk.Button(frame, text="Rechnung erstellen", command=on_submit).grid(column=0, row=row, columnspan=6, pady=10)

# Events binden
entry_suche.bind("<KeyRelease>", filter_kundenliste)

refresh_kundenliste()
refresh_artikelliste()

root.mainloop()