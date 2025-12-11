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
## Voraussetzungen:
1. GitHub-Konto: Ein GitHub-Konto wurde mit dem Dozenten eingerichtet.
2. SSH-Schlüssel: Ein SSH-Schlüssel wurde in deinem GitHub-Konto hinterlegt.
3. Terminal-Kenntnisse: Du bist vertraut mit der Nutzung des Terminals/der Kommandozeile.(Falls nicht, wende dich bitte an deinen Dozenten oder Lehrer, um eine Einführung zu erhalten.)
4. Lokale Ordnerstruktur: du verstehst, dass die Namen meiner lokalen Ordner von deinen abweichen können.
5. Selbstständigkeit: DU versuchst, die Aufgabe selbstständig umzusetzen und wendest dich nur bei auftretenden Fehlern an den Dozenten.

---

### schritt 1 
rufe die webseite auf "https://github.com/F-Klose/Verwaltungstool/tree/main"

Klicke auf die grüne Schalt fläche "Code", dann geht ein Fenster auf.
Dies sollte so aussehen:
![](./install_img/001.png)

--- 

### im popup 

Hier siehst du ein Pop-up-Fenster, dieses beinhaltet drei Tabs. Klicke auf SSH.
1. HTTPS
2. SSH <- hier 
3. GITHUB CLI 
![](./install_img/002.png)


--- 

### im SSH tab 

kopiere den link aus dem fenster 
![](./install_img/003.png)

Markiere alles und drücke COMMAND + C oder nutze den Button, um die Zeile in den Zwischenspeicher aufzunehmen.

---
 
 ### terminal 
1. Öffne das Terminal.

2. Nutze den Befehl cd (Change Directory), um in das Verzeichnis zu navigieren, in dem du das Repo (Repository) anlegen willst.
![](./install_img/004.png)

 ---

 ### im Ordner angekommen 

Jetzt, wo du an der Stelle bist, wo du das Repo anlegen willst, musst du den Befehl "git clone" mit der Zeile aus deinem Zwischenspeicher kombinieren.

Das sollte dann so aussehen:
![](./install_img/005.png)
wen das bei dir ao aus sieht drücke enter 

 --- 

### der Download 

Jetzt wird eine Menge in deinem Terminal passieren. Lasse es in Ruhe arbeiten. Wenn es fertig ist, machen wir weiter.

Wenn es in etwa so aussieht, ist der Download abgeschlossen:
![](./install_img/008.png)

---

### öffne VS code 
1. Öffne das jetzt installierte Repo in VS Code.
2. Klicke auf "Öffne neues Terminal" in der oberen rechten ecke .
![](./install_img/007.png)

---

### entwicklungs umgebung anlegen 


Hier gibst du nun folgende Befehle der Reihe nach ein:
```bash
python3 -m venv verwaltungstool
source verwaltungstool/bin/activate
pip install -r requirements.txt
```
wen das jetzt so aus sieht dann hast du alles richti gemacht :
![](./install_img/010.png)

---

### was ist da gerade passiert 

1. Du hast eine Entwicklungsumgebung geschaffen.

2. Du hast bestätigt, dass du innerhalb dieser Umgebung arbeiten willst, und diese aktiviert.

3. Du hast alle benötigten Zusatzpakete, die für das Repo gebraucht werden, installiert.

---

### was jetzt 

Wir sind fertig – du bist startbereit!

Im Hauptverzeichnis kannst du die main.py ausführen. Klicke die Datei an und drücke dann oben auf Start.
![](./install_img/009.png)
Schau dir die README an, wenn du weitere Fragen haben solltest.

Viel Spaß!


