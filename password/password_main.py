import random
import string
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel



def generate_random_password(length=8):
    Uppercase_char = random.choice(string.ascii_uppercase)
    chars = string.digits
    a = ''.join(random.choice(chars) for _ in range(length))
    special_chars = "!@#$%^&*()"
    special_chars = ''.join(random.choice(special_chars) for _ in range(1))
    final_password = Uppercase_char + a + special_chars
    print(final_password)
    return final_password

generate_random_password(8)

#TODO: print entfernen
#TODO: Gui schreiben 

class PasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Passwort Generator")
        layout = QVBoxLayout()

        self.label = QLabel("Generiertes Passwort:")
        layout.addWidget(self.label)

        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        layout.addWidget(self.password_field)

        self.generate_btn = QPushButton("Passwort generieren")
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)

    def generate_password(self):
        password = generate_random_password(8)
        self.password_field.setText(password)