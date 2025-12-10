#------------------------------------
#-------------importe----------------
#------------------------------------
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
import i18n
#------------------------------------
#---------------klasse---------------
#------------------------------------
class IntroManager(QDialog):
    def __init__(self,total_pages = 10, perant=None):# auch hier seitenanzahl festlegen 
        super().__init__(perant)
        self.total_pages = total_pages
        self.current_page = 1
        self.setWindowTitle("Einführungsmodus")
        self.setGeometry(100, 100, 300, 150)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.init_ui()


#------------------------------------
#----> Gui Elemente <----------------
#------------------------------------
    def init_ui(self):
        #erstellen des widgets
        main_layout = QVBoxLayout()
        self.intro_label = QLabel()
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.image_label = QLabel()
        #buttons
        self.next_button = QPushButton()# text wird in ui update gesetzt
        self.back_button = QPushButton()# text wird in ui update gesetzt
        #layout zusammenstellen
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.intro_label)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.next_button)
        main_layout.addWidget(self.back_button)
        #verbindungen 
        self.next_button.clicked.connect(self.next_page)
        self.back_button.clicked.connect(self.back_page)

    def updade_ui(self):
        page = self.current_page
        # inhalte aktualisieren
        self.intro_label.setText(i18n.t(f"intro.page_{page}.text"))
        image_path = i18n.t(f"intro.page_{page}.image")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Bild nicht gefunden.")

        # button texte aktualisieren
        self.next_button.setText(i18n.t("intro.next_button_text"))
        self.back_button.setText(i18n.t("intro.back_button_text"))
        #zustände der buttons(aktiv/ inaktiv schalten der buttons)
        self.back_button.setEnabled(page > 1)
        self.next_button.setEnabled(page < self.total_pages)

#------------------------------------
#------> steuerfunktionen <----------
#------------------------------------

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.updade_ui()

    def back_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.updade_ui()

