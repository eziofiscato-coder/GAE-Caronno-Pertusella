SOLUZIONE 2 - AVVIO CON FILE .BAT (Scelta Ezio)

COSA HAI:
- app.py (fix definitivo, cell non obbligatorio, no errori rossi)
- requirements.txt (librerie necessarie)
- AVVIA_ANA_GESTIONALE.bat (doppio click per avviare)

COME USARE (1 volta sola setup):

1. Installa Python (se non ce l'hai):
   - Vai su https://www.python.org/downloads/
   - Scarica Python 3.11 o 3.12 (pulsante giallo)
   - Lancia installer
   - IMPORTANTE: Spunta in basso "Add python.exe to PATH" o "Add Python to PATH"
   - Clicca Install Now
   - Aspetta fine installazione

2. Metti questi 3 file in una cartella:
   - Crea cartella C:\ANA_Gestionale\ (o dove vuoi)
   - Copia dentro: app.py, requirements.txt, AVVIA_ANA_GESTIONALE.bat

3. Avvia:
   - Doppio click su AVVIA_ANA_GESTIONALE.bat
   - La prima volta installa librerie (1-2 minuti, vedi scritte che scorrono)
   - Poi si apre automaticamente browser su http://localhost:8501
   - Vedi ANA Gestionale Varese!

4. Uso quotidiano:
   - Sempre doppio click su AVVIA_ANA_GESTIONALE.bat
   - Si apre subito (librerie già installate)

PER CHIUDERE:
- Chiudi browser
- Vai nella finestra nera (cmd) e premi Ctrl+C, poi S + Invio
- Oppure chiudi finestra nera

SE ERRORE:
- Se dice "Python non trovato" -> reinstalla Python spuntando Add to PATH
- Se dice errore librerie -> cancella cartella e rifai da capo
- Se porta 8501 occupata -> chiudi altre app Streamlit o cambia porta nel .bat

VANTAGGI SOLUZIONE 2:
- NO .exe che da errore "Failed to execute script"
- Funziona come Streamlit Cloud ma sul tuo PC
- Aggiorni solo copiando nuovo app.py
- Cell non obbligatorio, no errori rossi template

Ezio - ANA Varese - GAE Caronno Pertusella
