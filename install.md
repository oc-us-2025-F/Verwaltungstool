---
marp: true
title: Projektmanagement — Qualität & Ziele
author: Dein Name
theme: default
paginate: true
style: |
  section {
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    color: #222;
    background: linear-gradient(180deg, #d1cbcbff 0%, #a1b4c7ff 100%);
    padding: 2.0rem;
    /* Blauer Rand für bessere Optik */
    border: 18px solid #0b57a4;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(11,87,164,0.12);
  }
  h1, h2, h3 { color: #0b57a4; margin-bottom: 0.6rem; }
  .title-slide { background: linear-gradient(135deg,#0b57a4,#3db2ff); color: #fff; }
  .small { font-size: 0.85em; color: #666; }
  .center { text-align: center; }
  .lead { font-size: 1.15em; color: #333; }
  footer { font-size: 0.8em; color: #888; text-align: right; padding-right: 1em; }
  /* Zwei-Spalten Layout für Diagramme neben Text */
  .two-col { display: flex; gap: 2rem; align-items: center; justify-content: center; }
  .two-col .text { flex: 1 1 50%; min-width: 220px; }
  .two-col .visual { flex: 1 1 40%; display: flex; justify-content: center; }
  .two-col svg { max-width: 420px; width: 100%; height: auto; }
  .a {color:#008080;}
  @media (max-width: 900px) {
    .two-col { flex-direction: column; }
    section { padding: 1.2rem; }
  }

---

### Istallation des Verwaltungs tools 

## voraus setzungen:
1. Mit Dozenten eingerichter Github Accunt 
2. ssh schlüssel im acc hinterlegt 
3. du kennst das terminal (wenn nicht wende dich an deinen dozenten oder leher)
4. du musst verstehen das meine lokalen ornder andersheißen können als deine lokalen ordner 
5. du versuchst es alleine umzsetzen und wendes dich nur bei fehlern an die Dozenten 

wen das bei dir so weit passt können wir weiter machen 

---

### schritt 1 
rufe die webseite auf "https://github.com/F-Klose/Verwaltungstool/tree/main"

klicke auf die grüne schalt fläcche "code" dann geht ein fenster auf 
das sollte so aus sehen :
paltzhalter bild 001 

--- 

### im popup 

hier sihst du ein pop up fesner dieses beinhaltet drei Tabs klicke auf SSH
1. HTTPS
2. SSH <- hier 
3. GITHUB CLI 
platzhalter bild 2 

--- 

### im SSH tab 

kopiere den link aus dem fenster 
platzhaltter bild 003 
makiere alles und drücke COMMAND + C oder nutze den button um die zeile in den zwischenspeicher aufzunehmen 

---
 
 ### terminal 
 öffne das terminal 
 nutze den befehl "cd" und in das verzeichnis zu navigieren in dem du das repro anlegen willst 
 das sollte in etwa so aus sehen :
 platzhalter bild 004 

 ---

 ### im ordner angekommen 

 jetzt wo du an der stelle bist wo du das repro an legen willst
 musst du den befehl " git clone" mit der zeile aus deinem zwischenspeicher kombinieren 
 das sollte dann so aus sehen :
 platzhalter bild 005 
wen das bei dir ao aus siht wie bei mir drücke enter 

 --- 

### der Download 

jetzt wird eine menge in deinem terminal passieren lasse es in ruhe arbeiten wen es fertig ist machen wir weiter 
wen es in etwa so aus sieht ist der download abgeschlossen 

bild 006 

---

### öffne VS code 

öffne das jetzt instalierte repro 

klicke auf öffne neues terminal :
bild 007 

---

### entwicklungs umgebung anlegen 


hier gibst du nun folgende befehle ein :
```bash
python3 -m venv verwaltungstool
source verwaltungstool/bin/activate
pip install -r requirements.txt
```
wen das jetzt so aus sieht dann hast du alles richti gemacht :
bild 008 

---

### 

