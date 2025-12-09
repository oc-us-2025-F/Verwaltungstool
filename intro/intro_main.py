#------------------------------------
#-------------importe----------------
#------------------------------------
from pyside6.QtCore import Qt
from pyside6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
import i18n
#------------------------------------
#---------------klasse---------------
#------------------------------------
class IntroManager:
    def __init__(self, perant=None):
        super().__init__(perant)
        self.setWindowTitle("Einführungsmodus")
        self.setGeometry(100, 100, 300, 150)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.init_ui()
        self.init_data()
#------------------------------------
#----> Gui Elemente <----------------
#------------------------------------
    def init_ui(self):
        main_layout = QVBoxLayout()
        PAGE = 1
        self.intro_label = QLabel(i18n.t(f"intro.page_{PAGE}_text"))# zu ordnung aufrufen über page text
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(i18n.t(f"intro.page_{PAGE}_image"))#zu ordnung aufrufen über page bild
        main_layout.addWidget(self.intro_label)
        main_layout.addWidget(self.image_label)
        self.next_button = QPushButton(i18n.t("intro.next_button_text"))#nächster
        self.back_button = QPushButton(i18n.t("intro.back_button_text"))#zurück

    def load_page(self, page_number):
        self.intro_label.setText(i18n.t(f"intro.page_{page_number}_text"))
        self.image_label.setPixmap(i18n.t(f"intro.page_{page_number}_image"))
        self.next_button.setText(i18n.t("intro.next_button_text"))
        self.back_button.setText(i18n.t("intro.back_button_text"))

    def next_page(self):
        self.load_page(self.current_page + 1)
  

    def back_page(self):
        if self.current_page > 1:
            self.load_page(self.current_page - 1)
        else:
            pass