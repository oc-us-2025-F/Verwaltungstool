"""
Schüler-Quiz-GUI:
- Auswahl des eigenen Namens (inkl. Surren und Florian)
- Quiz-Auswahl und Sortierung
- Quiz starten
"""

import os
from db_setup import init_db, DB_PATH
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QDialog, QRadioButton, QButtonGroup, QScrollArea, QWidget
from utils.git_utils import git_push
import sqlite3
import sys

REPO_PATH = "."

# Prüfe ob die Datenbank existiert, falls nicht, initialisiere sie
if not os.path.exists(DB_PATH):
    init_db()

# Dialog für die Durchführung eines Quiz
class QuizDialog(QDialog):
    def __init__(self, schueler_name, quiz_id, quiz_titel):
        super().__init__()
        # Fenster-Titel setzen
        self.setWindowTitle(f"Quiz: {quiz_titel}")
        self.schueler_name = schueler_name  # Name des aktuellen Schülers
        self.quiz_id = quiz_id              # ID des aktuellen Quiz
        self.fragen = []                    # Liste der Fragen (frage_id, ButtonGroup)
        self.antwortgruppen = []            # Liste der ButtonGroups für Antworten

        # ScrollArea für viele Fragen, damit alles sichtbar bleibt
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_widget = QWidget()
        self.layout = QVBoxLayout(main_widget)  # Layout für Fragen und Antworten
        scroll.setWidget(main_widget)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll)
        self.setLayout(dialog_layout)

        # Fragen und Antworten aus der Datenbank laden
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, frage_text FROM frage WHERE quiz_id = ?", (quiz_id,))
        fragen = c.fetchall()
        # Jede Frage einzeln abarbeiten
        # SELECT id, antwort_text FROM antwort WHERE frage_id IN (1,2,3,4);
        for frage_id, frage_text in fragen:
            self.layout.addWidget(QLabel(frage_text)) # Frage anzeigen
            c.execute("SELECT id, antwort_text FROM antwort WHERE frage_id = ?", (frage_id,))
            antworten = c.fetchall()
            group = QButtonGroup(self) # ButtonGroup für Antwortoptionen
            # Jede Antwort als Radiobutton anzeigen
            for antwort_id, antwort_text in antworten:
                radio = QRadioButton(antwort_text) # Antwortoption als Radiobutton
                radio.setProperty("antwort_id", antwort_id) # Antwort-ID speichern
                group.addButton(radio)
                self.layout.addWidget(radio)
            self.fragen.append((frage_id, group)) # Frage und zugehörige Antworten speichern
            self.antwortgruppen.append(group)
        conn.close()

        # Button zum Abschicken der Antworten
        self.submit_btn = QPushButton("Abschicken")
        self.submit_btn.clicked.connect(self.submit_quiz)
        self.layout.addWidget(self.submit_btn)

    def submit_quiz(self):
        # Prüfen ob alle Fragen beantwortet wurden
        gegeben_antworten = [] # Liste der gewählten Antworten
        for frage_id, group in self.fragen:
            checked = group.checkedButton()
            if checked is None:
                # Wenn eine Frage nicht beantwortet wurde, abbrechen
                QMessageBox.warning(self, "Fehler", "Bitte alle Fragen beantworten!")
                return
            antwort_id = checked.property("antwort_id")
            gegeben_antworten.append((frage_id, antwort_id))
        # Ergebnis berechnen und speichern
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Schüler-ID aus Datenbank holen
        schueler_id = c.execute("SELECT id FROM schueler WHERE name = ?", (self.schueler_name,)).fetchone()[0]
        richtig = 0 # Zähler für richtige Antworten
        falsch = 0  # Zähler für falsche Antworten
        # Für jede Antwort prüfen ob sie richtig ist
        # SELECT ist_richtig, count(*) FROM antwort WHERE id IN (13,14,15) group by ist_richtig 
        for frage_id, antwort_id in gegeben_antworten:
            ist_richtig = c.execute("SELECT ist_richtig FROM antwort WHERE id = ?", (antwort_id,)).fetchone()[0]
            if ist_richtig:
                richtig += 1
            else:
                falsch += 1
        # Aktuelles Datum/Uhrzeit für das Ergebnis
        import datetime
        datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Ergebnis in die Datenbank schreiben
        c.execute("INSERT INTO ergebnis (schueler_id, quiz_id, datum, richtig, falsch) VALUES (?, ?, ?, ?, ?)",
                  (schueler_id, self.quiz_id, datum, richtig, falsch))
        ergebnis_id = c.lastrowid
        # Gegebene Antworten speichern
        for frage_id, antwort_id in gegeben_antworten:
            c.execute("INSERT INTO gegebene_antwort (ergebnis_id, frage_id, antwort_id) VALUES (?, ?, ?)",
                      (ergebnis_id, frage_id, antwort_id))
        conn.commit()
        conn.close()
        # Ergebnis zu Git pushen, damit Lehrer es sehen kann
        git_push(REPO_PATH)
        # Ergebnis dem Schüler einmalig anzeigen
        QMessageBox.information(self, "Ergebnis", f"Richtig: {richtig}\nFalsch: {falsch}")
        self.accept() # Dialog schließen

# Haupt-GUI für Schüler
class SchuelerQuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz für Schüler")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Dropdown für Schülernamen
        self.schueler_dropdown = QComboBox()
        self.layout.addWidget(QLabel("Wähle deinen Namen:"))
        self.layout.addWidget(self.schueler_dropdown)
        # Filter für Quiz-Sortierung
        filter_layout = QHBoxLayout()
        self.quiz_sort_dropdown = QComboBox()
        self.quiz_sort_dropdown.addItems([
            "Standard",         # Standard-Sortierung
            "Wie oft gemacht",  # Nach Häufigkeit
            "Wann erstellt",    # Nach Erstellungsdatum
            "Noch nie gemacht"  # Noch nicht bearbeitete Quiz
        ]) 
        #TODO: Fehlerhäufigkeiten (falsch - noch nicht richtig - richtig - perfekt)
        filter_layout.addWidget(QLabel("Quiz sortieren nach:"))
        filter_layout.addWidget(self.quiz_sort_dropdown)
        self.layout.addLayout(filter_layout)
        # Liste der verfügbaren Quiz
        self.quiz_list = QListWidget()
        self.layout.addWidget(QLabel("Verfügbare Quiz:"))
        self.layout.addWidget(self.quiz_list)
        # Button zum Starten des Quiz
        self.start_button = QPushButton("Quiz starten")
        self.layout.addWidget(self.start_button)
        # Event-Handler verbinden
        self.start_button.clicked.connect(self.start_quiz)
        self.quiz_sort_dropdown.currentIndexChanged.connect(self.load_quiz)
        self.schueler_dropdown.currentIndexChanged.connect(self.load_quiz)
        # Initiales Laden der Schüler und Quiz
        self.load_schueler()
        self.load_quiz()

    def load_schueler(self):
        # Schülernamen aus DB laden, ggf. "Surren" und "Florian" hinzufügen
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for name in ["Surren", "Florian"]:
            c.execute("SELECT id FROM schueler WHERE name = ?", (name,))
            if not c.fetchone():
                c.execute("INSERT INTO schueler (name) VALUES (?)", (name,))
        conn.commit()
        c.execute("SELECT name FROM schueler")
        schueler = c.fetchall()
        self.schueler_dropdown.clear()
        for s in schueler:
            self.schueler_dropdown.addItem(s[0])
        conn.close()

    def load_quiz(self):
        # Quizliste nach Sortiermodus laden
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        schueler = self.schueler_dropdown.currentText()
        sort_mode = self.quiz_sort_dropdown.currentText()
        # Verschiedene Sortiermodi für Quiz-Auswahl
        query = "SELECT quiz.id, quiz.titel, quiz.rowid, quiz.id FROM quiz"
        if sort_mode == "Wie oft gemacht" and schueler:
            # Quiz nach Häufigkeit sortieren
            query = """
                SELECT quiz.id, quiz.titel, COUNT(ergebnis.id) as gemacht_count
                FROM quiz
                LEFT JOIN ergebnis ON quiz.id = ergebnis.quiz_id AND ergebnis.schueler_id = (SELECT id FROM schueler WHERE name = ?)
                GROUP BY quiz.id
                ORDER BY gemacht_count DESC
            """
            c.execute(query, (schueler,))
            quiz = c.fetchall()
        elif sort_mode == "Wann erstellt":
            # Quiz nach Erstellungsdatum sortieren
            query = "SELECT id, titel FROM quiz ORDER BY id DESC"
            c.execute(query)
            quiz = c.fetchall()
        elif sort_mode == "Noch nie gemacht" and schueler:
            # Quiz, die der Schüler noch nie gemacht hat
            query = """
                SELECT quiz.id, quiz.titel
                FROM quiz
                WHERE quiz.id NOT IN (
                    SELECT quiz_id FROM ergebnis WHERE schueler_id = (SELECT id FROM schueler WHERE name = ?)
                )
            """
            c.execute(query, (schueler,))
            quiz = c.fetchall()
        else:
            # Standard: alle Quiz anzeigen
            query = "SELECT id, titel FROM quiz"
            c.execute(query)
            quiz = c.fetchall()
        self.quiz_list.clear()
        for q in quiz:
            self.quiz_list.addItem(q[1]) # Quiz-Titel zur Liste hinzufügen
        conn.close()

    def start_quiz(self):
        # Quiz starten, QuizDialog öffnen
        schueler = self.schueler_dropdown.currentText()
        quiz_item = self.quiz_list.currentItem()
        if not schueler or not quiz_item:
            QMessageBox.warning(self, "Fehler", "Bitte wähle einen Schüler und ein Quiz aus.")
            return
        # Quiz-ID aus DB holen
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM quiz WHERE titel = ?", (quiz_item.text(),))
        quiz_row = c.fetchone()
        conn.close()
        if not quiz_row:
            QMessageBox.warning(self, "Fehler", "Quiz nicht gefunden.")
            return
        quiz_id = quiz_row[0]
        # QuizDialog anzeigen, Ergebnis wird nach Schließen nicht erneut angezeigt
        dialog = QuizDialog(schueler, quiz_id, quiz_item.text())
        dialog.exec()

# Hauptprogrammstart: Initialisiert die GUI und startet die Anwendung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchuelerQuizApp()
    window.show()
    sys.exit(app.exec())

"""
Lehrer-Quiz-GUI:
- Quiz erstellen (mit Scrollbar für viele Fragen)
- Ergebnisse und Statistiken anzeigen
- Filter nach Schüler und Quiz
- Integration mit Git für Quiz-Änderungen
"""

# GUI- und Datenbank-Importe
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QLineEdit, QTextEdit, QSpinBox, QFormLayout, QScrollArea)
from utils.git_utils import git_push
import sqlite3
import sys
import os
from db_setup import init_db, DB_PATH

REPO_PATH = "."

# Datenbank initialisieren, falls nicht vorhanden
if not os.path.exists(DB_PATH):
    init_db()

class QuizErstellenDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neues Quiz erstellen")
        # ScrollArea für viele Fragen
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_widget = QWidget()
        self.layout = QVBoxLayout(main_widget)
        scroll.setWidget(main_widget)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll)
        self.setLayout(dialog_layout)
        self.titel_input = QLineEdit()
        self.layout.addWidget(QLabel("Quiz-Titel:"))
        self.layout.addWidget(self.titel_input)
        self.fragen = []
        # Fragen und Antwortfelder erzeugen
        for i in range(1, 11):
            frage_group = QVBoxLayout()
            frage_text = QTextEdit()
            frage_text.setPlaceholderText(f"Frage {i}")
            frage_group.addWidget(QLabel(f"Frage {i}:"))
            frage_group.addWidget(frage_text)
            antworten = []
            antwort_layout = QFormLayout()
            num_antworten = QSpinBox()
            num_antworten.setRange(2, 4)
            num_antworten.setValue(2)
            frage_group.addWidget(QLabel("Anzahl Antwortmöglichkeiten (2-4):"))
            frage_group.addWidget(num_antworten)
            # Antwortoptionen für jede Frage
            for j in range(4):
                antwort_text = QLineEdit()
                antwort_text.setPlaceholderText(f"Antwort {j+1}")
                ist_richtig = QComboBox()
                ist_richtig.addItems(["Falsch", "Richtig"])
                antwort_layout.addRow(antwort_text, ist_richtig)
                antworten.append((antwort_text, ist_richtig))
            frage_group.addLayout(antwort_layout)
            self.fragen.append((frage_text, num_antworten, antworten))
            self.layout.addLayout(frage_group)
        self.save_button = QPushButton("Quiz speichern")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_quiz)

    def save_quiz(self):
        # Quiz und Fragen/Antworten speichern
        titel = self.titel_input.text().strip()
        if not titel:
            QMessageBox.warning(self, "Fehler", "Bitte einen Quiz-Titel eingeben.")
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO quiz (titel) VALUES (?)", (titel,))
        quiz_id = c.lastrowid
        for frage_text, num_antworten, antworten in self.fragen:
            frage = frage_text.toPlainText().strip()
            if not frage:
                continue
            c.execute("INSERT INTO frage (quiz_id, frage_text) VALUES (?, ?)", (quiz_id, frage))
            frage_id = c.lastrowid
            antwort_data = []
            for idx in range(num_antworten.value()):
                antwort_txt = antworten[idx][0].text().strip()
                ist_richtig = antworten[idx][1].currentText() == "Richtig"
                if antwort_txt:
                    antwort_data.append((frage_id, antwort_txt, ist_richtig))
            if antwort_data:
                c.executemany("INSERT INTO antwort (frage_id, antwort_text, ist_richtig) VALUES (?, ?, ?)", antwort_data)
        conn.commit()
        conn.close()
        git_push(REPO_PATH) # Änderungen pushen
        QMessageBox.information(self, "Erfolg", "Quiz erfolgreich erstellt und gepusht!")
        self.accept()

class LehrerQuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz-Auswertung für Lehrer")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Filter-Bereich für Schüler und Quiz
        filter_layout = QHBoxLayout()
        self.schueler_dropdown = QComboBox()
        self.quiz_dropdown = QComboBox()
        filter_layout.addWidget(QLabel("Schüler:"))
        filter_layout.addWidget(self.schueler_dropdown)
        filter_layout.addWidget(QLabel("Quiz:"))
        filter_layout.addWidget(self.quiz_dropdown)
        self.layout.addLayout(filter_layout)
        # Ergebnistabelle
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Schüler", "Quiz", "Datum", "Richtig/Falsch"])
        self.layout.addWidget(self.result_table)
        # Buttons für Details und Quiz-Erstellung
        self.detail_button = QPushButton("Details anzeigen")
        self.layout.addWidget(self.detail_button)
        self.detail_button.clicked.connect(self.show_details)
        self.quiz_create_button = QPushButton("Quiz erstellen")
        self.layout.addWidget(self.quiz_create_button)
        self.quiz_create_button.clicked.connect(self.open_quiz_creator)
        # Initiales Laden der Daten
        self.load_schueler()
        self.load_quiz()
        self.load_results()
        # Filter-Events
        self.schueler_dropdown.currentIndexChanged.connect(self.load_results)
        self.quiz_dropdown.currentIndexChanged.connect(self.load_results)

    def load_schueler(self):
        # Schülernamen für Filter laden
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM schueler")
        schueler = c.fetchall()
        self.schueler_dropdown.clear()
        self.schueler_dropdown.addItem("Alle")
        for s in schueler:
            self.schueler_dropdown.addItem(s[0])
        conn.close()

    def load_quiz(self):
        # Quiznamen für Filter laden
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT titel FROM quiz")
        quiz = c.fetchall()
        self.quiz_dropdown.clear()
        self.quiz_dropdown.addItem("Alle")
        for q in quiz:
            self.quiz_dropdown.addItem(q[0])
        conn.close()

    def load_results(self):
        # Ergebnisse für Tabelle laden und filtern
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query = """
            SELECT schueler.name, quiz.titel, ergebnis.datum, ergebnis.richtig, ergebnis.falsch, ergebnis.id
            FROM ergebnis
            JOIN schueler ON ergebnis.schueler_id = schueler.id
            JOIN quiz ON ergebnis.quiz_id = quiz.id
        """
        params = []
        schueler = self.schueler_dropdown.currentText()
        quiz = self.quiz_dropdown.currentText()
        if schueler != "Alle":
            query += " WHERE schueler.name = ?"
            params.append(schueler)
        if quiz != "Alle":
            if params:
                query += " AND quiz.titel = ?"
            else:
                query += " WHERE quiz.titel = ?"
            params.append(quiz)
        query += " ORDER BY ergebnis.datum DESC"
        c.execute(query, params)
        results = c.fetchall()
        self.result_table.setRowCount(len(results))
        for row_idx, (schueler_name, quiz_titel, datum, richtig, falsch, ergebnis_id) in enumerate(results):
            datum_kurz = datum[:16] if datum else "" # Nur Datum, Stunde, Minute
            self.result_table.setItem(row_idx, 0, QTableWidgetItem(schueler_name))
            self.result_table.setItem(row_idx, 1, QTableWidgetItem(quiz_titel))
            self.result_table.setItem(row_idx, 2, QTableWidgetItem(datum_kurz))
            self.result_table.setItem(row_idx, 3, QTableWidgetItem(f"{richtig}/{falsch}"))
            self.result_table.setRowHeight(row_idx, 20)
        conn.close()

    def show_details(self):
        # Detailansicht für ein Ergebnis
        selected = self.result_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Fehler", "Bitte wähle ein Ergebnis aus.")
            return
        ergebnis_id = self.result_table.item(selected, 0)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        schueler = self.result_table.item(selected, 0).text()
        quiz = self.result_table.item(selected, 1).text()
        datum = self.result_table.item(selected, 2).text()
        c.execute("""
            SELECT ergebnis.id FROM ergebnis
            JOIN schueler ON ergebnis.schueler_id = schueler.id
            JOIN quiz ON ergebnis.quiz_id = quiz.id
            WHERE schueler.name = ? AND quiz.titel = ? AND ergebnis.datum LIKE ?
        """, (schueler, quiz, datum + "%"))
        result = c.fetchone()
        conn.close()
        if result:
            dialog = StatistikDialog(result[0])
            dialog.exec()
        else:
            QMessageBox.warning(self, "Fehler", "Statistikdaten konnten nicht geladen werden.")

    def open_quiz_creator(self):
        # Quiz-Erstellungsdialog öffnen
        dialog = QuizErstellenDialog()
        if dialog.exec():
            self.load_quiz()
            self.load_results()

class StatistikDialog(QDialog):
    def __init__(self, ergebnis_id):
        super().__init__()
        self.setWindowTitle("Quiz-Statistik")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Quiz-, Schüler- und Datumsinfo anzeigen
        c.execute("""
            SELECT schueler.name, quiz.titel, ergebnis.datum
            FROM ergebnis
            JOIN schueler ON ergebnis.schueler_id = schueler.id
            JOIN quiz ON ergebnis.quiz_id = quiz.id
            WHERE ergebnis.id = ?
        """, (ergebnis_id,))
        info = c.fetchone()
        if info:
            self.layout.addWidget(QLabel(f"Schüler: {info[0]}"))
            self.layout.addWidget(QLabel(f"Quiz: {info[1]}"))
            self.layout.addWidget(QLabel(f"Datum: {info[2][:16]}"))
        # Fragen und Antworten für das Ergebnis anzeigen
        c.execute("""
            SELECT frage.id, frage.frage_text
            FROM frage
            JOIN ergebnis ON frage.quiz_id = ergebnis.quiz_id
            WHERE ergebnis.id = ?
        """, (ergebnis_id,))
        fragen = c.fetchall()
        for frage_id, frage_text in fragen:
            self.layout.addWidget(QLabel(f"Frage: {frage_text}"))
            c.execute("SELECT id, antwort_text, ist_richtig FROM antwort WHERE frage_id = ?", (frage_id,))
            antworten = c.fetchall()
            c.execute("SELECT antwort_id FROM gegebene_antwort WHERE ergebnis_id = ? AND frage_id = ?", (ergebnis_id, frage_id))
            gegeben = c.fetchone()
            gegeben_id = gegeben[0] if gegeben else None
            for antwort_id, antwort_text, ist_richtig in antworten:
                mark = ""
                if antwort_id == gegeben_id:
                    mark = " (gegeben)"
                if ist_richtig:
                    mark += " [richtig]"
                self.layout.addWidget(QLabel(f"- {antwort_text}{mark}"))
        conn.close()

if __name__ == "__main__":
    # Hauptprogrammstart
    app = QApplication(sys.argv)
    window = LehrerQuizApp()
    window.show()
    sys.exit(app.exec())