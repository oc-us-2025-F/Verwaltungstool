#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# hier wird die passwort generriung gemacht <-----------------------------<-----------------------------<-------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------
# importe <-------------------
#-----------------------------
import random
import string
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
#-----------------------------
# passwort <------------------
#-----------------------------
def generate_random_password(length=8):
    """
    hier wird ein passwort generiert mit einer länge von 8 zeichen standardmäßig
    Das passwort enthält mindestens einen Großbuchstaben, eine Zahl und ein Sonderzeichen(10 = chars 8 zeichen lang + die beiden sonder regeln )
    
    :param length: Länge des generierten Passworts
    :return: Generiertes Passwort als String

    anpassbar durch den length parameter
    8 zeichen = 10 chars (1 uppercase, 1 special char, 8 digits)
    einfach ändern um längere passwörter zu generieren
    """
    Uppercase_char = random.choice(string.ascii_uppercase)
    chars = string.digits
    a = ''.join(random.choice(chars) for _ in range(length))
    special_chars = "!@#$%^&*()"
    special_chars = ''.join(random.choice(special_chars) for _ in range(1))
    final_password = Uppercase_char + a + special_chars
    print(final_password)
    return final_password

generate_random_password(8)



class PasswordWindow(QWidget):
    """
    Gui für den Passwort Generator
    1. Label um das generierte Passwort anzuzeigen
    2. Textfeld um das Passwort anzuzeigen
    3. Button um ein neues Passwort zu generieren
    4. Beim Klicken auf den Button wird ein neues Passwort generiert und im Textfeld angezeigt
    5. Das Textfeld ist nur lesbar, um zu verhindern, dass der Benutzer das Passwort ändert
    6. Das Fenster hat den Titel "Passwort Generator"
    7. Die Länge des generierten Passworts ist standardmäßig 10 Zeichen
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Passwort Generator")
        layout = QVBoxLayout()

        self.label = QLabel("Generiertes Passwort:")
        layout.addWidget(self.label)
#----------------------------------------------
# -----> TEXT feld für generintes passwort<----
#----------------------------------------------
        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        layout.addWidget(self.password_field)
#----------------------------------------------
# -----> Button um Passwort zu generieren <----
#----------------------------------------------
        self.generate_btn = QPushButton("Passwort generieren")
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)

    def generate_password(self):
        """
        generiert ein neues Passwort und zeigt es im Textfeld an
        8 zeichen lang + 2 sonderregelzeichen = 10 chars
        1 großbuchstabe, 1 sonderzeichen, 8 zahlen
        """
        password = generate_random_password(8)
        self.password_field.setText(password)