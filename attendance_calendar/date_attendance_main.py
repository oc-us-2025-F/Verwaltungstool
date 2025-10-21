# date_attendance_main.py

import json
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QCalendarWidget
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QColor

CLASS_JSON_FILE = "meine_anwesenheit.json"

class AttendanceCalendar(QWidget):
    """
    Ein Kalender-Widget zur Erfassung persönlicher Anwesenheit.
    Status: Karlsruhe, Homeoffice, Urlaub, Krankheit, Feiertag.
    """

    STATUS_COLORS = {
        "Karlsruhe": "lightgreen",
        "Homeoffice": "#f7f78a",
        "Urlaub": "lightblue",
        "Krankheit": "lightcoral",
        "Feiertag": "lightgray"
    }

    STATUS_OPTIONS = list(STATUS_COLORS.keys())

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meine Anwesenheit")
        self.resize(400, 300)

        # Kalender-Widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)

        self.status_label = QLabel()
        self.combo = QComboBox()
        self.combo.addItems(self.STATUS_OPTIONS)
        self.save_button = QPushButton("Status setzen")

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.set_status_for_selected_date)
        self.calendar.clicked.connect(self.on_date_clicked)

        self.attendance = self.load_data()
        self.highlight_saved_days()

    def load_data(self):
        try:
            with open(CLASS_JSON_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(CLASS_JSON_FILE, "w") as f:
            json.dump(self.attendance, f, indent=2, ensure_ascii=False)

    def on_date_clicked(self, qdate: QDate):
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.attendance.get(date_str)
        self.status_label.setText(f"Status am {date_str}: {status or 'Kein Status gesetzt'}")

    def set_status_for_selected_date(self):
        qdate = self.calendar.selectedDate()
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.combo.currentText()
        self.attendance[date_str] = status
        self.save_data()
        self.status_label.setText(f"Status am {date_str}: {status}")
        self.highlight_day(qdate, status)

    def highlight_day(self, qdate: QDate, status: str):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(self.STATUS_COLORS.get(status, "white")))
        self.calendar.setDateTextFormat(qdate, fmt)

    def highlight_saved_days(self):
        for date_str, status in self.attendance.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.highlight_day(qdate, status)
