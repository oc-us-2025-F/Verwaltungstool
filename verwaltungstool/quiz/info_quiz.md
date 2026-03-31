---
hier eigige infos und anmerkungen zum quiz

---

### das quiz

es ist kleines fragen und antworten system 1 frage mit bis zu 4 antwortmöglichkeiten 
davon muss mindes 1 richtig sein 
es muss mindestens 2 antwortn geben 
maximal können vier antworten richtig sein 
---

### wertung 
wen mehr als 1 antwort möglichkeit richtig wäre aber nur ein richtige antwort gegeben wurde ist die frage nicht richtig beantwortet 

---

### fragen 
fragne wender in einer BD gespeichert diese DB speichert fragen als sting in der DB je frage erhält einen eindeutige ID um sie zu orndnen zu können

---
### antworten 

jede frage kann bis zu 4 antworten mit liefern 
antworten werden als stinge gespeichert (plus vermerk ob diese richt oder falsch sind )

---

### ablauf 

das quiz generriet über die nutzung einen count wert der die häfigkeit der fragen steuert je nach dem wie 
oft man eine frage richtig oder flasch bantwortet hat wird der count steigen oder fallen 
je höher der count (eisehbar in der "quiz_scores.json") des soltender die frage in der rotation aber nicht ausgeschlossen 
je niedriger des so öfter kommt die frage 

---

### zukünftige äderung :

geplant ist es den teil des scriptes zu ändern der die häufigkeit der fragen steuert so zu ergänzen das 1 frage nie direkt 2 mal hinter einander kommen kann so das dazischen mindests 5 andere fragen kommen müssen warscheinlich mit einer liste die sich inmer die id der fragen merkt und wen mehr als 5 id´s enthalten sind den ersten eintrag löscht mit einer gegenprüfung das keine fragen kommen können deren id in der liste einthalten sind als grober pall 

---

### danke 
aktuelle version könnte man als test version sehen daher nicht so streng damit sein 

