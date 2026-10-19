
PERCHE ERRORE "Failed to execute script 'app' due to unhandled exception: streamlit"?

CAUSA:
ANA_Gestionale_Varese.exe è stato creato con PyInstaller da app.py che è una app STREAMLIT.
Streamlit NON può essere eseguito come .exe normale! Deve essere avviato con "streamlit run app.py".
PyInstaller non include i metadati di streamlit -> importlib.metadata.PackageNotFoundError: streamlit -> crash!

SOLUZIONI:

SOLUZIONE 1 (CONSIGLIATA - come ANA Varese su Cloud):
Non usare .exe! Usa Python:
1. Installa Python da python.org (spunta Add to PATH)
2. Metti in una cartella: app.py + requirements.txt
3. Apri CMD nella cartella e fai: pip install -r requirements.txt
4. Poi: streamlit run app.py
5. Si apre browser su http://localhost:8501

SOLUZIONE 2 (Usa il .bat):
Usa il file AVVIA_ANA_GESTIONALE.bat che ho creato - fa tutto automatico!

SOLUZIONE 3 (Se vuoi proprio .exe):
Devi ricompilare .exe con PyInstaller con questi parametri:
pyinstaller --onefile --collect-all streamlit --collect-data streamlit --hidden-import streamlit --hidden-import pandas --hidden-import openpyxl --hidden-import reportlab app.py

Oppure usa il fix che ho messo in app.py FIX EXE - include patch per importlib.metadata

Ma la Soluzione 1 è quella che usi per ANA Varese e GAE su Streamlit Cloud!

Ezio - GAE Caronno
