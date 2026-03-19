ja klar


* sqlite-Datenbank zu supabase migrieren





* DB-Funktionen so umschreiben, dass sie die REST-Api von supabase abfragen
* git-Aufrufe entfernen
* Config datei erstellen




ggf. nach Tabellenimport sowas wie: 

SELECT setval(
  pg_get_serial_sequence('quotes', 'id'), 
  (SELECT MAX(id) FROM quotes)
);