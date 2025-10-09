import os
import re
from datetime import datetime

def pruefer_tool(rtf_path):
    eintraege = []
    with open(rtf_path, 'r', encoding='utf-8') as f:
        text = f.read()
        # RTF-Steuerzeichen entfernen (grob)
        text = re.sub(r'{\\.*?}|\\[a-z]+\d*|{|}', '', text)
        for match in re.findall(r"(\d{2}\.\d{2}\.\d{2})\s+(KA|HO)", text):
            datum_str, typ = match
            datum_obj = datetime.strptime(datum_str, "%d.%m.%y")
            datum_format = datum_obj.strftime("%Y_%m_%d")  # Für Dateinamen 2- x weiter kürzel ausdenken
            if typ == "KA":
                typ = "K"
            elif typ == "HO":
                typ = "H"
            eintraege.append((datum_format, typ))
    return eintraege

def abgleichung(rtf_path, pruefer_path):
    eintraege_pdf = pruefer_tool(rtf_path)
    pdf_dict = {d: t for d, t in eintraege_pdf}
    
    # Alle .rtf-Dateien in allen Unterordnern finden, aber nur mit "tagesbericht" im Namen
    dateien_ordner = []
    for root, dirs, files in os.walk(pruefer_path):
        for f in files:
            if f.lower().endswith(".rtf") and "tagesbericht" in f.lower():
                dateien_ordner.append(os.path.join(root, f))

    fehlend = []
    uberzaelig = []
    falsch = []
    for datum, typ in eintraege_pdf:
        suchmuster = f"{datum}_tagesbericht_{typ}".lower()
        passende = [d for d in dateien_ordner if suchmuster in os.path.basename(d).lower()]
        if not passende:
            fehlend.append(f"{datum} {typ}")
        else:
            if not any(suchmuster in os.path.basename(d).lower() for d in passende):
                falsch.append(f"{datum}: erwartet {typ}, gefunden {[os.path.basename(p) for p in passende]}")
    
    pdf_keys = [f"{d}_tagesbericht_{t}".lower() for d, t in eintraege_pdf]
    for datei in dateien_ordner:
        name = os.path.basename(datei).lower().replace(".rtf", "")
        if all(name != p for p in pdf_keys):
            uberzaelig.append(datei)
    return fehlend, uberzaelig, falsch

if __name__ == "__main__":
    rtf_pfad = "test.rtf"      # RTF-Datei im aktuellen Verzeichnis
    ordner = "Schulungs_Material"           # Hauptordner

    if not os.path.exists(rtf_pfad):
        print(f"RTF-Datei nicht gefunden: {rtf_pfad}")
    elif not os.path.exists(ordner):
        print(f"Ordner nicht gefunden: {ordner}")
    else:
        fehlend, uberzaelig, falsch = abgleichung(rtf_pfad, ordner)
        print("Prüfung abgeschlossen.")
        print("Fehlende Einträge:")
        if fehlend:
            for f in fehlend:
                print("  -", f)
        else:
            print("  Keine")

        print("Überzählige Dateien:")
        if uberzaelig:
            for u in uberzaelig:
                print("  -", u)
        else:
            print("  Keine")

        print("Falsche Einträge:")
        if falsch:
            for fa in falsch:
                print("  -", fa)
        else:
            print("  Keine")

#TODO: Urlaubsrechnung einbauen
#TODO: Feiertagsrechnung einbauen
#TODO: Ende der Schulung bearbeiten
#TODO: Legende überlegen (KA/HO/K/F/P/U)
#TODO: alternative zu bennenung "tagesbericht" überlegen
#TODO: prints entfernen return an gui