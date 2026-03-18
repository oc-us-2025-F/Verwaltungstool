from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QInputDialog, QLineEdit, QFrame
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
import sys
from news.news_main import get_news, delete_old_news, add_news_item
# Quotes-Import
from quotes.quotes_main import get_quotes, add_quotes as add_quote_item
from counter.counter_main import CounterDialog
from password.password_main import PasswordWindow
from quiz.quiz_main import QuizMainWindow
from utils.git_utils import git_pull, git_push, git_merge
# Module für Netzplan-Übung verfügbar machen
import sys, os
# Pfad zum Netzplan-Verzeichnis hinzufügen, damit Imports funktionieren
netzplan_dir = os.path.join(os.path.dirname(__file__), "netzplan_gui_version")
if netzplan_dir not in sys.path:
    sys.path.insert(0, netzplan_dir)

from attendance_calendar.date_attendance_main import AttendanceCalendar
from Elekrotechnick.gui import ElektroGUI
from utils.markdown_viewer import MarkdownViewerDialog

# AP2 Lernkarten Quiz
try:
    from lernkarten_ap2.quiz_launcher import AP2QuizLauncher
except ImportError:
    AP2QuizLauncher = None

# Netzplan-Komponenten (falls verfügbar)
try:
    from netzplan_gui_version.netzplan_uebung import NetzplanUebungWindow
except ImportError:
    NetzplanUebungWindow = None
# Zahlensysteme-Funktionen (nur Quiz-Funktionen verwenden, GUI nicht verändern)
from zahlensysteme.main.fuctions import (
    binaer_zu_dezi,
    dezi_zu_binaer,
    dezi_zu_hexadezi,
    hexadezi_zu_dezi,
)


class NewsFenster(QWidget):
    def __init__(self):
        super().__init__()
        self.news_list = get_news()
        
        # Fallback für leere Liste
        if not self.news_list:
            self.news_list = ["Keine News vorhanden. Klicke 'Neu' um eine zu erstellen."]
        
        self.current_index = 0
        
        layout = QVBoxLayout()
        self.label = QLabel(self.news_list[self.current_index])
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        btn_prev = QPushButton("Zurück")
        btn_prev.clicked.connect(self.show_prev)
        btn_new = QPushButton("Neu")
        btn_new.clicked.connect(self.add_news)
        btn_next = QPushButton("Nächste")
        btn_next.clicked.connect(self.show_next_immediately)
        button_layout.addWidget(btn_prev)
        button_layout.addWidget(btn_new)
        button_layout.addWidget(btn_next)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next)
        self.timer.start(45000)  # 45 Sekunden

    def show_next(self):
        if len(self.news_list) <= 1:
            return  # Kein Weiterschalten wenn nur 1 Eintrag
        self.current_index = (self.current_index + 1) % len(self.news_list)
        self.label.setText(self.news_list[self.current_index])

    def show_prev(self):
        if len(self.news_list) <= 1:
            return  # Kein Zurückschalten wenn nur 1 Eintrag
        self.current_index = (self.current_index - 1) % len(self.news_list)
        self.label.setText(self.news_list[self.current_index])

    def show_next_immediately(self):
        self.timer.stop()
        self.show_next()
        self.timer.start(45000)

    def reload_news(self):
        self.news_list = get_news()
        
        # Fallback für leere Liste
        if not self.news_list:
            self.news_list = ["Keine News vorhanden."]
        
        # Index zurücksetzen wenn außerhalb der neuen Liste
        if self.current_index >= len(self.news_list):
            self.current_index = 0
        
        self.label.setText(self.news_list[self.current_index])

    def add_news(self):
        text, ok = QInputDialog.getText(self, "Neue News", "News-Text eingeben:", QLineEdit.Normal)
        if ok and text.strip():
            try:
                from datetime import datetime
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                add_news_item(text, "news/news.db", created_at)
                self.reload_news()
            except Exception as e:
                print(f"Fehler beim Hinzufügen: {e}")
                self.label.setText(f"Fehler: {e}")

class QuotesFenster(QWidget):
    def __init__(self):
        super().__init__()
        self.quotes_list = get_quotes()
        self.current_index = 0

        layout = QVBoxLayout()
        self.label = QLabel(self.quotes_list[self.current_index])
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        btn_prev = QPushButton("Zurück")
        btn_prev.clicked.connect(self.show_prev)
        btn_new = QPushButton("Neu")
        btn_new.clicked.connect(self.add_quote)
        btn_next = QPushButton("Nächste")
        btn_next.clicked.connect(self.show_next_immediately)
        button_layout.addWidget(btn_prev)
        button_layout.addWidget(btn_new)
        button_layout.addWidget(btn_next)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next)
        self.timer.start(45000)  # 45 Sekunden

    def show_prev(self):
        self.current_index = (self.current_index - 1) % len(self.quotes_list)
        self.label.setText(self.quotes_list[self.current_index])

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.quotes_list)
        self.label.setText(self.quotes_list[self.current_index])

    def show_next_immediately(self):
        self.timer.stop()
        self.show_next()
        self.timer.start(45000)

    def reload_quotes(self):
        self.quotes_list = get_quotes()
        self.label.setText(self.quotes_list[self.current_index])

    def add_quote(self):
        text, ok = QInputDialog.getText(self, "Neues Zitat", "Zitat-Text eingeben:", QLineEdit.Normal)
        if ok and text.strip():
            add_quote_item(text, "quotes/quotes.db")
            git_push()
            self.reload_quotes()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verwaltungstool")

        # --- Git- und News-Initialisierung beim Start ---
        git_pull()
        git_merge()
        delete_old_news("news/news.db")
        git_push()

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Obere Buttons
        top_layout = QHBoxLayout()

        btn_anwesenheit = QPushButton("Anwesenheitskalender")
        btn_anwesenheit.clicked.connect(self.oeffne_anwesenheit)
        top_layout.addWidget(btn_anwesenheit)

        btn_counter = QPushButton("Störungs Counter")
        btn_counter.clicked.connect(self.oeffne_counter)
        top_layout.addWidget(btn_counter)

        btn_quizscore = QPushButton("Quiz starten")
        btn_quizscore.clicked.connect(self.oeffne_quizscore)
        top_layout.addWidget(btn_quizscore)

        btn_ap2_quiz = QPushButton("AP2 Lernkarten Quiz")
        btn_ap2_quiz.clicked.connect(self.oeffne_ap2_quiz)
        top_layout.addWidget(btn_ap2_quiz)

        # Neuer teil zahlen bis netzplan
        btn_zahlensysteme = QPushButton("Zahlensysteme")
        btn_zahlensysteme.clicked.connect(self.oeffne_zahlensysteme)
        top_layout.addWidget(btn_zahlensysteme)

        btn_elektro = QPushButton("Elektrotechnik")
        btn_elektro.clicked.connect(self.oeffne_elektrotechnik)
        top_layout.addWidget(btn_elektro)

        btn_netzplan = QPushButton("Netzplan")
        btn_netzplan.clicked.connect(self.oeffne_netzplan)
        top_layout.addWidget(btn_netzplan)

        btn_password = QPushButton("Passwortgenerator")
        btn_password.clicked.connect(self.oeffne_password)
        top_layout.addWidget(btn_password)
        
        main_layout.addLayout(top_layout)

        # Mittlere Info-Fenster
        middle_layout = QHBoxLayout()
        self.news_fenster = NewsFenster()
        self.quotes_fenster = QuotesFenster()
        middle_layout.addWidget(self.news_fenster)
        middle_layout.addWidget(self.quotes_fenster)
        main_layout.addLayout(middle_layout)

        # Untere Buttons
        bottom_layout = QHBoxLayout()
        # Branding-Box unten links
        branding_layout = QHBoxLayout()
        branding_frame = QFrame()
        branding_frame.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        branding_inner = QHBoxLayout()
        logo = QLabel()
        logo.setFixedSize(15, 15)
        
        # Versuche icon.png zu laden, ansonsten Fallback-Farbe
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            # Skaliere auf exakt 15x15 Pixel
            pixmap = pixmap.scaledToWidth(15, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        else:
            # Fallback: Grauer Platzhalter, wenn icon.png nicht existiert
            logo.setStyleSheet("background-color: #bbb; border: 1px solid #888;")
        
        branding_inner.addWidget(logo)
        branding_text = QLabel("MAKE BY UMSCHULUNGS GRUPPEN: 03.2025-03.2027")
        branding_inner.addWidget(branding_text)
        branding_frame.setLayout(branding_inner)
        branding_layout.addWidget(branding_frame)
        branding_layout.addStretch()
        bottom_layout.addLayout(branding_layout)

        bottom_layout.addStretch()
        btn_beenden = QPushButton("Beenden")
        btn_beenden.clicked.connect(self.beenden)
        bottom_layout.addWidget(btn_beenden)
        btn_aktualisieren = QPushButton("Aktualisieren")
        btn_aktualisieren.clicked.connect(self.git_update)
        bottom_layout.addWidget(btn_aktualisieren)
        main_layout.addLayout(bottom_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Timer für automatisches Git Pull alle 60 Sekunden
        self.git_timer = QTimer(self)
        self.git_timer.timeout.connect(self.git_auto_pull)
        self.git_timer.start(60000)  #TODO: wieder auf 60 Sekunden ändern
    
    def oeffne_anwesenheit(self):
        self.anwesenheit_window = AttendanceCalendar()
        self.anwesenheit_window.show()

    def oeffne_counter(self):
        dialog = CounterDialog(self)
        dialog.exec()

    def oeffne_anwesenheit(self):
        self.anwesenheit_window = AttendanceCalendar()
        self.anwesenheit_window.show()

    def oeffne_password(self):
        self.password_window = PasswordWindow()
        self.password_window.show()

    def oeffne_quizscore(self):
        self.quiz_window = QuizMainWindow()
        self.quiz_window.show()

    def oeffne_ap2_quiz(self):
        if AP2QuizLauncher is None:
            QMessageBox.warning(self, "Fehler", "AP2 Lernkarten Quiz-Modul nicht verfügbar.")
            return
        
        try:
            from pathlib import Path
            quiz_exe = Path(__file__).parent / "lernkarten_ap2" / "main.exe"
            
            if not quiz_exe.exists():
                # Zeige Setup-Anleitung wenn Exe fehlt
                setup_md = Path(__file__).parent / "lernkarten_ap2" / "SETUP_ANLEITUNG.md"
                if setup_md.exists():
                    dialog = MarkdownViewerDialog(
                        str(setup_md),
                        "AP2 Lernkarten Quiz - Einrichtung erforderlich",
                        self
                    )
                    dialog.exec()
                else:
                    QMessageBox.warning(
                        self, 
                        "Fehler", 
                        f"Quiz-Programm nicht gefunden:\n{quiz_exe}\n\nBitte main.cs kompilieren."
                    )
                return
            
            launcher = AP2QuizLauncher(str(quiz_exe))
            if launcher.start_quiz():
                QMessageBox.information(self, "Erfolg", "AP2 Lernkarten Quiz wurde gestartet!")
            else:
                QMessageBox.critical(self, "Fehler", "Quiz konnte nicht gestartet werden.")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Starten des Quiz: {e}")

    def oeffne_elektrotechnik(self):
        self.elektro_window = ElektroGUI()
        self.elektro_window.show()

    def oeffne_netzplan(self):
        if NetzplanUebungWindow is None:
            QMessageBox.warning(self, "Fehler", "Netzplan-Modul fehlt oder konnte nicht geladen werden.")
            return
        self.netzplan_window = NetzplanUebungWindow()
        self.netzplan_window.show()

    def git_update(self):
        git_pull()
        git_merge()
        self.news_fenster.reload_news()

    def git_auto_pull(self):
        git_pull()
        self.news_fenster.reload_news()

    def beenden(self):
        git_push()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


    #TODO: funktionen auslagern in eigene dateien