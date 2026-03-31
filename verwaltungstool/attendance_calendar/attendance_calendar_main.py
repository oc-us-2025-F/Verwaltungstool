import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QComboBox, 
                               QLabel, QCalendarWidget, QDialog, QDialogButtonBox)
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QColor
from collections import Counter
from datetime import datetime, timedelta

from verwaltungstool.config import settings


CLASS_JSON_FILE = settings.CALENDAR_JSON

class StartDateDialog(QDialog):
    """Dialog zum Festlegen des Schulungs-Startdatums."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Startdatum wählen")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        info_label = QLabel("Bitte wähle das Startdatum deiner Schulung.\n"
                           "Die Anwesenheitsquote wird über 2 Jahre (24 Monate) berechnet.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)
        
        self.selected_label = QLabel()
        layout.addWidget(self.selected_label)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
        
        self.calendar.clicked.connect(self.on_date_selected)
        
        self.setLayout(layout)
        self.resize(400, 400)
    
    def on_date_selected(self, qdate):
        date_str = qdate.toString("dd.MM.yyyy")
        end_date = qdate.addYears(2).addDays(-1)
        end_str = end_date.toString("dd.MM.yyyy")
        self.selected_label.setText(f"Zeitraum: {date_str} - {end_str}")
    
    def get_start_date(self):
        """Gibt das gewählte Startdatum als datetime zurück."""
        qdate = self.calendar.selectedDate()
        return datetime(qdate.year(), qdate.month(), qdate.day())


class AttendanceCalendar(QWidget):
    """
    Ein Kalender-Widget zur Erfassung persönlicher Anwesenheit.
    Status: Karlsruhe, Homeoffice, Urlaub, Krankheit, Feiertag.
    """

    STATUS_COLORS = {
        "Karlsruhe": "#2E8B57",      
        "Homeoffice": "#DAA520",     
        "Urlaub": "#4682B4",         
        "Krankheit": "#DC143C",      
        "Feiertag": "#708090"        
    }

    STATUS_OPTIONS = list(STATUS_COLORS.keys())

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meine Anwesenheit")
        self.resize(420, 350)

        # Widgets
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.status_label = QLabel()
        self.combo = QComboBox()
        self.combo.addItems(self.STATUS_OPTIONS)
        self.save_button = QPushButton("Status setzen")

        # Neue Anzeige für Anwesenheitsquote
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: gray; font-size: 11px; margin-top: 4px;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.combo)
        layout.addWidget(self.save_button)
        layout.addWidget(self.stats_label)
        self.setLayout(layout)

        # Signals
        self.save_button.clicked.connect(self.set_status_for_selected_date)
        self.calendar.clicked.connect(self.on_date_clicked)

        # Daten laden
        self.attendance = self.load_data()
        
        # Startdatum abfragen (nur wenn noch nicht gesetzt)
        if "start_date" not in self.attendance:
            self.ask_for_start_date()
        
        self.highlight_saved_days()
        self.update_stats_label()

    def ask_for_start_date(self):
        """Zeigt den Dialog zum Festlegen des Startdatums."""
        dialog = StartDateDialog(self)
        if dialog.exec():
            start_date = dialog.get_start_date()
            self.attendance["start_date"] = start_date.strftime("%Y-%m-%d")
            self.save_data()

    def load_data(self):
        try:
            with open(CLASS_JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(CLASS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.attendance, f, indent=2, ensure_ascii=False)

    def on_date_clicked(self, qdate: QDate):
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.attendance.get(date_str)
        self.status_label.setText(f"Status am {date_str}: {status or 'Kein Status gesetzt'}")

    def set_status_for_selected_date(self):
        qdate = self.calendar.selectedDate()
        if not qdate.isValid():
            print(f"Ungültiges Datum: {qdate}")
            return

        date_str = qdate.toString("yyyy-MM-dd")
        status = self.combo.currentText()
        self.attendance[date_str] = status
        self.save_data()
        self.status_label.setText(f"Status am {date_str}: {status}")
        self.highlight_day(qdate, status)
        self.update_stats_label()

    def highlight_day(self, qdate: QDate, status: str):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(self.STATUS_COLORS.get(status, "white")))
        self.calendar.setDateTextFormat(qdate, fmt)

    def highlight_saved_days(self):
        for date_str, status in self.attendance.items():
            if date_str == "start_date":
                continue
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.highlight_day(qdate, status)

    def update_stats_label(self):
        """Berechnet die Statistik für den 2-Jahres-Schulungszeitraum."""
        
        # Startdatum holen
        start_date_str = self.attendance.get("start_date")
        if not start_date_str:
            self.stats_label.setText("Kein Startdatum gesetzt.")
            return
        
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = start_date + timedelta(days=730)  # 2 Jahre = 730 Tage
        
        # Nur ungültige Einträge entfernen
        valid_entries = {}
        invalid_found = False
        
        for date_str, status in self.attendance.items():
            if date_str == "start_date":
                valid_entries[date_str] = status
                continue
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                valid_entries[date_str] = status
            except ValueError:
                print(f"⚠️ Ungültiges Datum übersprungen: {date_str}")
                invalid_found = True
        
        if invalid_found:
            self.attendance = valid_entries
            self.save_data()
        
        # Nur Schulungszeitraum filtern
        training_entries = {
            date_str: status
            for date_str, status in self.attendance.items()
            if date_str != "start_date" 
            and start_date <= datetime.strptime(date_str, "%Y-%m-%d") < end_date
        }

        if not training_entries:
            start_str = start_date.strftime("%m/%Y")
            end_str = (end_date - timedelta(days=1)).strftime("%m/%Y")
            self.stats_label.setText(f"Keine Einträge im Schulungszeitraum ({start_str} - {end_str}).")
            return

        counts = Counter(training_entries.values())
        total_days = sum(counts.values())

        stats_text = " / ".join(
            f"{status}: {round((counts.get(status, 0) / total_days) * 100)}%"
            for status in self.STATUS_OPTIONS
            if counts.get(status)
        )

        start_str = start_date.strftime("%m/%Y")
        end_str = (end_date - timedelta(days=1)).strftime("%m/%Y")
        self.stats_label.setText(
            f"Anwesenheitsquote Schulung ({start_str} - {end_str}): {stats_text}"
        )