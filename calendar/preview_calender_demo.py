# date_attendance.py

import sys
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from PySide6.QtWidgets import QCalendarWidget, QMessageBox
from PySide6.QtCore import QDate

CLASS_JSON_FILE = "meine_anwesenheit.json"

class AttendanceCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meine Anwesenheit")
        self.resize(400, 300)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        self.status_label = QLabel("", self)

        self.combo = QComboBox(self)
        self.combo.addItems(["Anwesend", "Abwesend", "Urlaub"])

        self.save_button = QPushButton("Status setzen", self)
        self.save_button.clicked.connect(self.set_status_for_selected_date)

        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Daten laden
        self.attendance = self.load_data()

        # Wenn Datum im Kalender ausgewählt wird, zeigen wir evtl. vorhandenen Status
        self.calendar.clicked.connect(self.on_date_clicked)

        # Markiere die bereits gespeicherten Tage beim Start
        self.highlight_saved_days()

    def load_data(self):
        try:
            with open(CLASS_JSON_FILE, "r") as f:
                data = json.load(f)
            return data  # erwartet: {"YYYY-MM-DD": "Anwesend", ...}
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(CLASS_JSON_FILE, "w") as f:
            json.dump(self.attendance, f, indent=2, ensure_ascii=False)

    def on_date_clicked(self, qdate: QDate):
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.attendance.get(date_str, None)
        if status:
            self.status_label.setText(f"Status am {date_str}: {status}")
        else:
            self.status_label.setText(f"Kein Status für {date_str} gesetzt")

    def set_status_for_selected_date(self):
        qdate = self.calendar.selectedDate()
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.combo.currentText()
        self.attendance[date_str] = status
        self.save_data()
        self.status_label.setText(f"Status am {date_str}: {status}")
        self.highlight_day(qdate, status)

    def highlight_day(self, qdate: QDate, status: str):
        # Farbwahl basierend auf Status
        fmt = self.calendar.dateTextFormat(qdate)
        from PySide6.QtGui import QTextCharFormat, QColor

        new_fmt = QTextCharFormat(fmt)
        if status == "Anwesend":
            new_fmt.setBackground(QColor("lightgreen"))
        elif status == "Abwesend":
            new_fmt.setBackground(QColor("lightcoral"))
        elif status == "Urlaub":
            new_fmt.setBackground(QColor("lightblue"))
        else:
            new_fmt.setBackground(QColor("white"))

        self.calendar.setDateTextFormat(qdate, new_fmt)

    def highlight_saved_days(self):
        from PySide6.QtGui import QTextCharFormat, QColor
        for date_str, status in self.attendance.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                fmt = QTextCharFormat()
                if status == "Anwesend":
                    fmt.setBackground(QColor("lightgreen"))
                elif status == "Abwesend":
                    fmt.setBackground(QColor("lightcoral"))
                elif status == "Urlaub":
                    fmt.setBackground(QColor("lightblue"))
                self.calendar.setDateTextFormat(qdate, fmt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AttendanceCalendar()
    win.show()
    sys.exit(app.exec())

#TODO:optionen angeben 
#TODO:auswahl funktionalität ändern