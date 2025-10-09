import pyside6 

try:
    from git_funktions import git_pull_db, git_push_db
    from under_funktions_main import init_db, update_counter, get_counter_display_text 
    # Die Funktionen get_counter und update_labels werden jetzt nicht mehr direkt in der Klasse gebraucht!
except ImportError:
    print("Warnung: Imports fehlgeschlagen. Verwende Platzhalter.")
    def git_pull_db(): print("Git-Pull simuliert")
    def git_push_db(): print("Git-Push simuliert")
    def init_db(): print("DB init simuliert")
    def update_counter(art): print(f"Zähler für {art} in DB erhöht.")

    def get_counter_display_text(): return "Zählerstände konnten nicht geladen werden (Platzhalter)"


class CounterDialog(QDialog):
    # ... (__init__, init_ui, init_data bleiben unverändert, aber der Code ist kürzer geworden!) ...

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Label für den Gesamt- und Einzel-Counter
        self.total_label = QLabel("Gesamt: --")
        # Wichtig: Machen Sie das Label mehrzeilig, damit der neue Text passt
        self.total_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.total_label)
        
        # (Layout für die Zähl-Buttons bleibt unverändert)
        counter_button_layout = QHBoxLayout()
        self.tech_button = QPushButton("Techn. Störung zählen")
        self.tech_button.clicked.connect(lambda: self.count_störung("technisch"))
        counter_button_layout.addWidget(self.tech_button)
        self.general_button = QPushButton("Allg. Störung zählen")
        self.general_button.clicked.connect(lambda: self.count_störung("allgemein"))
        counter_button_layout.addWidget(self.general_button)
        main_layout.addLayout(counter_button_layout)
        
        self.close_button = QPushButton("Schließen & Speichern")
        self.close_button.clicked.connect(self.accept) 
        main_layout.addWidget(self.close_button)

        self.setLayout(main_layout)
        self.update_display() # Erste Anzeige nach UI-Setup laden
        
    def init_data(self):
        """Initialisiert DB, zieht und pusht beim Start."""
        init_db()
        git_pull_db()
        git_push_db()

    def count_störung(self, art):
        """Erhöht den Zähler, aktualisiert die Anzeige und pusht sofort."""
        print(f"Aktion: Zähle {art}...")
        
        update_counter(art) # Zähler in der lokalen DB erhöhen
        self.update_display() # Anzeige aktualisieren
        git_push_db() # Sofortiges Pushen
        print(f"Zähler für {art} erhöht und DB zu Git GEPUSHT.")

    def update_display(self):
        """Aktualisiert die Labels mit dem formatierten Text aus der Helferfunktion."""
        try:
            display_text = get_counter_display_text() 
            self.total_label.setText(display_text)
        except Exception as e:
            self.total_label.setText("Fehler beim Laden der Zählerstände.")
            print(f"FEHLER beim Update des Displays: {e}") 
            
    def start_periodic_pull(self):
        """Startet den Timer für den automatischen Pull."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.do_periodic_pull)
        self.timer.start(15000) # 15 Sekunden

    def do_periodic_pull(self):
        """Zieht Daten und aktualisiert die Anzeige."""
        print("Periodischer Pull...")
        git_pull_db()
        self.update_display()
        
    def reject(self):
        """Wird bei Schließen über X/ESC aufgerufen (mit abschließendem Push)."""
        print("Dialog abgebrochen (X/ESC) - Führe abschließenden Push durch.")
        git_push_db()
        super().reject()

    def accept(self):
        """Wird bei Klick auf 'Schließen & Speichern' aufgerufen (mit abschließendem Push)."""
        print("Dialog mit 'Schließen' beendet - Führe abschließenden Push durch.")
        git_push_db()
        super().accept()

#TODO: Integrationstest innerhalb Counter und außerhalb 