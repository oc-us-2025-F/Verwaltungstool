import os 
#hauptfunktion
ziele = [0.45, 0.50, 0.55] #ziele in prozent 0.45 = 45%
gesamt_werktage_schulungzeitraum = 503# austauschen gegegen zeitraum der schulung
basis_ordner = "Documents/Schulungs_Material" #pfad anpassen?
doppelte_berichte = []
counter_doppellberichte = 0
anzahl_h = 0
anzahl_k = 0 
for wurzel, verzeichnisse, dateien in os.walk(basis_ordner):
    for datei in dateien:
        print(datei)
        name_lower = datei.lower()
        if "tagesbericht_h" in name_lower:
            anzahl_h += 1
            print(anzahl_h)
        elif "tagesbericht_k" in name_lower:
            anzahl_k += 1
            print(anzahl_k)
gesamt = anzahl_h + anzahl_k# gesammt zahl der tagesberichte 
#
#hier werden die prozente ermittelt 1. punkt in der gui 
if gesamt > 0:
    prozent_h = ((anzahl_h -1) / gesamt) * 100
    prozent_k = ((anzahl_k -1 ) / gesamt) * 100
else:# falls nichts da ist wird null zur neuem varablen inhalt festgelegt damit der code auch im lehr zustand durchlaufen kann  
    prozent_h = 0
    prozent_k = 0
print(f"Anzahl Tagesberichte H:  {anzahl_h}    K:,{anzahl_k}")
print(f"Gesamtanzahl Tagesberichte: {gesamt}")
print(f"Prozentualer Anteil H: {prozent_h:.2f}% ")
print(f"Prozentualer Anteil K: {prozent_k:.2f}%")
#prüfung der nach doppel berichten noch nicht fertig //gleiche berichte muessten auch im selben verzeichnis sein um entdeckt zu werden
#aus wahl punkt 3 in der gui 
for wurzel, basis_ordner, dateien in os.walk(basis_ordner):
    for datei in dateien:
        if "tagesbericht" in datei.lower():
            pfad = os.path.join(wurzel, datei)
            if pfad not in doppelte_berichte:
                doppelte_berichte.append(pfad)
            else:
                counter_doppellberichte += 1
print(f"Anzahl doppelter Berichte: {counter_doppellberichte}")

gesamt = anzahl_h + anzahl_k
gesamt2 = anzahl_h + anzahl_k



#auswahlpunkt 2 in der gui 
#ermitteln nach spiel raum auf grund lage der werktage inerhalb der schulung(berücksichtig gesetzliche feiertage badenwürtemberg 
# zwischen 10.03.25 und 10.03.27 muss warschleinlich noch angepasst werden) und der bereits erstellten berichte 
print("Gesamtanzahl der Berichte: ", gesamt)
for ziel in ziele:
    ziel_prozent = int(ziel * 100)
    aktueller_k = anzahl_k / gesamt if gesamt > 0 else 0 

    print(f"Ziel: {ziel_prozent}% K")

    if aktueller_k < ziel:
        fehlende_k =(ziel * gesamt -anzahl_k) / (1 - ziel)
        fehlende_k = int(fehlende_k) + 1 if fehlende_k % 1 != 0 else int(fehlende_k)
        print(f"es fehlen {fehlende_k} berichte_K um {ziel_prozent}% zu erreichen ")
    else:
        print(f"schon min {ziel_prozent}% K erreicht")
    
    max_h_weg = int((anzahl_k / ziel) - gesamt)
    if max_h_weg > 0:
        print(f"Maximale Anzahl H Berichte, die gemacht werden können, um {ziel_prozent}% K noch zu erreichen: {max_h_weg}")
    else:
        print(f"kein spielraum mehr für H Berichte, um {ziel_prozent}% K zu erreichen")

print("tage der schulung: ", gesamt_werktage_schulungzeitraum)
print("tage der schulung prozentual: ", (gesamt / gesamt_werktage_schulungzeitraum) * 100)
print("---->",gesamt_werktage_schulungzeitraum - gesamt2, "<---- tage übrig")
print((gesamt_werktage_schulungzeitraum/2)-gesamt2,"halbzeit")
#alle brichte ausgeben die erstellt wurden und sortiert nach datum
#andere datei 
#wird später alles neu sortiert jetzt laufen die prototypen erstmal

#TODO: Urlaubsrechnung einbauen
#TODO: Feiertagsrechnung einbauen
#TODO: Ende der Schulung bearbeiten
#TODO: Legende überlegen (KA/HO/K/F/P/U)
#TODO: richtig anzalh der schulungs tage ermiiteln über schulungbeginn von bis ende (bundesland feiertage berücksichtigen)(mit eingaben)
#TODO: rest urlaub ermitteln 
#TODO: prints entfernenreturn an die gui 