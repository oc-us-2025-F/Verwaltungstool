from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QInputDialog,
)
import sys

from fuctions import (
    binaer_zu_dezi,
    dezi_zu_binaer,
    dezi_zu_hexadezi,
    hexadezi_zu_dezi,
)


def ask_and_check(module):
    prompt, answer, input_type = module.get_quiz()
    text, ok = QInputDialog.getText(None, "Quiz", prompt)
    if not ok:
        return
    if input_type == 'int':
        try:
            user = int(text)
        except ValueError:
            QMessageBox.warning(None, "Fehler", "Bitte eine Zahl eingeben!")
            return
        correct = (user == answer)
    else:
        user = text.strip().upper()
        correct = (user == str(answer).upper())

    if correct:
        QMessageBox.information(None, "Ergebnis", "Richtig!")
    else:
        QMessageBox.information(None, "Ergebnis", f"Falsch! Richtig wäre: {answer}")


def run():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("Zahlensysteme Quiz")
    layout = QVBoxLayout()

    btn1 = QPushButton("Binär -> Dezimal")
    btn2 = QPushButton("Dezimal -> Binär")
    btn3 = QPushButton("Dezimal -> Hexadezimal")
    btn4 = QPushButton("Hexadezimal -> Dezimal")
    btn5 = QPushButton("Beenden")

    btn1.clicked.connect(lambda: ask_and_check(binaer_zu_dezi))
    btn2.clicked.connect(lambda: ask_and_check(dezi_zu_binaer))
    btn3.clicked.connect(lambda: ask_and_check(dezi_zu_hexadezi))
    btn4.clicked.connect(lambda: ask_and_check(hexadezi_zu_dezi))
    btn5.clicked.connect(app.quit)

    for btn in (btn1, btn2, btn3, btn4, btn5):
        layout.addWidget(btn)

    w.setLayout(layout)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
