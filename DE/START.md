# Smart Home verstehen und ohne Gerätezugriff ausprobieren

## 1. Was du baust
Ein kleines lokales Übungsdashboard aus fünf frei erfundenen Messwerten. Es zeigt Zeit und Einheit, erkennt einen veralteten Wert, unterscheidet Schaltwunsch und Bestätigung und merkt sich ein vorbereitetes Morgenbriefing über einen Neustart hinweg. Kein Haus, Gerät, Bot oder Sprachmodell wird angesprochen. Unser privater Haus-Butler Hermes auf einem ODROID H4 ist ein eigenes Python-Projekt und hat nichts mit dem Nous-Hermes-Agenten zu tun.

## 2. Download und Voraussetzungen
Entpacke das vollständige Lernpaket in einen neuen Ordner. Du brauchst vorhandenes Python3.10 oder neuer, keine zusätzlichen Bibliotheken. Lies BUTLER-UEBUNG.py und DATEN-SYNTHETISCH.json. Das Paket installiert nichts. Die Dateien enthalten keine echten Termine, Hausdaten, API-Schlüssel oder Geräteadressen.

## 3. Erste Übung ausführen
In PowerShell im entpackten Ordner:
```powershell
python ./BUTLER-UEBUNG.py --data ./DATEN-SYNTHETISCH.json --state ./zustand.sqlite --output ./lauf-1
```
Öffne lauf-1/DASHBOARD.html im Browser. Es lädt nichts aus dem Netz und braucht keinen laufenden Server. BERICHT.json daneben enthält dieselben Zahlen maschinenlesbar. Der Ausgangsordner darf noch nicht existieren; vorhandene Ergebnisse werden erhalten. Die SQLite-Datei enthält nur den synthetischen Briefing-Zustand und wird bewusst zwischen Läufen behalten.

## 4. Den ersten Bericht lesen
Die feste Übungszeit ist2026-10-07 um07:00UTC. Frisch bedeutet in dieser Übung höchstens900Sekunden alt und nicht aus der Zukunft. Solar350W, Batterie58Prozent und die beiden Taupunkte sind frisch. Der Heizungswert vom Vorabend wird als veraltet markiert.350W sind Leistung, keine350kWh Energie. Die Messwerte und Regeln sind Übungsdaten, kein Tagesprotokoll unseres Hauses.

## 5. Taupunkt vergleichen
Die vorgegebenen Taupunkte sind innen12°C und außen8°C. Die Übung meldet lediglich: außen niedrigerer Taupunkt. Sie öffnet kein Fenster. Sie beurteilt weder Schadstoffe noch Wetter, Raumtemperatur, bauliche Situation oder die notwendige Lüftungsdauer. Ein Prozentwert der relativen Feuchte allein beantwortet diese Frage nicht. Veraltete, fehlende oder anders beschriftete Taupunktwerte führen zu unbekannt.

## 6. Schaltwunsch ist kein Gerätebeweis
switch_request fordert off an. switch_ack ist zunächst null und die synthetische Rückmeldung sagt noch on. Deshalb lautet das Ergebnis not_confirmed. Ein Bot darf daraus nicht behaupten: Die Steckdose ist aus. Dieses Paket betätigt auch nach einer positiven Übungsbestätigung kein Gerät.

## 7. Eine rein synthetische Bestätigung ausprobieren
Kopiere DATEN-SYNTHETISCH.json unter einen neuen Namen DATEN-BESTAETIGT.json. Ersetze switch_ack durch:
```json
{"request_id":"exercise-001","applied":true,"at":"2026-10-07T06:59:10+00:00"}
```
Setze in switch_observation nur state auf off. Zeit und Request-ID müssen passen; Rückmeldung darf nicht älter als der Wunsch oder aus der Zukunft sein. Dann:
```powershell
python ./BUTLER-UEBUNG.py --data ./DATEN-BESTAETIGT.json --state ./zustand.sqlite --output ./lauf-bestaetigt
```
synthetic_confirmation_matches bedeutet nur: Diese erfundenen Daten erfüllen den Übungsvertrag. Für echte Geräte ist zusätzlich ein geprüfter Adapter mit authentischer Rückmeldung nötig.

## 8. Neustartfehler nachvollziehen
Führe den ersten Befehl erneut aus, diesmal mit --output ./lauf-2 und derselben zustand.sqlite. Im ersten Lauf war new_preparation true. Jetzt ist es false und stored_event_count bleibt1. Die UNIQUE-Ereigniskennung morning-2026-10-07 bleibt dauerhaft gespeichert. Das dedupliziert nur unsere lokale Briefing-Vorbereitung; es beweist keine Nachrichtenzustellung.

## 9. Was bei echter Zustellung zusätzlich fehlt
Reale Abfragen, Kalenderadapter, Gerätebestätigung, Rechte, wiederholbare Jobs und Zustellprotokolle müssen separat implementiert und getestet werden. Ein Telegram-Offset betrifft empfangene Updates; ein Tagesbriefing braucht eine eigene stabile Ereigniskennung. Bei Absturz zwischen Versand und Speicherung ist Zustellung ungewiss. Unser Status lautet prepared_simulation_not_sent, niemals erfolgreich gesendet. Keine riskante automatische Wiederholung wird empfohlen.

## 10. Lokal und Cloud genau trennen
Eine lokale Python-Anwendung macht externe Dienste nicht automatisch offline. Unser Originalprojekt nutzte verschiedene Anbindungen; Telegram, manche Herstellerdienste, regionale Nachrichten und gegebenenfalls externe KI können Internetzugang benötigen. Der Offline-Helfer in diesem Download ist davon unabhängig und enthält keine Zugangsdaten. Ein Herstellername ist kein Beleg für eine schon funktionierende neue Installation.

## 11. Erweiterung als Planung
Zeichne zuerst Quellen→Zeit/Einheit→Datenbank→Anzeige. Geräteaktionen erhalten einen getrennten Zweig mit Anfrage, Werkzeugantwort und Rücklesung. Notiere im leeren PRUEFPROTOKOLL.csv deine echte Quelle und Grenzen, sobald du später selbst Adapter prüfst. Heizungsmanager, Energiesparen und Hardwareunterstützung sind hier nicht neu erprobt. Eine lokale KI kann den Bericht erklären; sie soll fehlende Daten nicht erfinden und wird von unserem Helfer nicht gestartet.

## 12. Fertig bedeutet hier
Du kannst den Bericht nachvollziehen, den alten Wert finden, eine fehlende Schaltbestätigung erkennen und die Briefing-Vorbereitung nach einem erneuten Prozessstart auf genau einem Eintrag halten. Das ist ein überprüfbarer kleiner Lernschritt. Der komplette private Haus-Butler wird nicht ausgeliefert, und eine tatsächliche Nachricht oder Hardwareaktion gehört nicht zu diesem Übungsergebnis.
