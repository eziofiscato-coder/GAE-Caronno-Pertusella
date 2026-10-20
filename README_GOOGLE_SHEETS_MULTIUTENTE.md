# GAE Protezione Civile - Google Sheets Multi Utente

## Setup Multi Utente con Google Sheets

### 1. Crea Progetto Google Cloud
- Vai su https://console.cloud.google.com/
- Crea nuovo progetto: GAE Protezione Civile
- Abilita API:
  - Google Sheets API
  - Google Drive API

### 2. Crea Service Account
- IAM e amministrazione → Service Account → Crea
- Nome: gae-multiutente
- Ruolo: Editor
- Crea chiave JSON → Scarica file
- Rinomina in google_credentials.json e metti nella cartella app

### 3. Crea Spreadsheet
- Vai su https://sheets.google.com
- Crea nuovo foglio: GAE Multi Utente
- Condividi con email del service account (da JSON: client_email) con permesso Editor
- Condividi anche con tutti gli utenti che devono collaborare
- Copia ID dalla URL: https://docs.google.com/spreadsheets/d/QUESTO_ID/edit

### 4. Configura App
- Apri gestionale → Google Sheets Multi Utente
- Incolla Spreadsheet ID
- Carica google_credentials.json
- Clicca Testa Connessione
- Clicca Crea Nuovo Spreadsheet (se vuoi crearne uno nuovo automaticamente)

### 5. Uso Quotidiano Multi Utente
- Ogni utente: Carica da Google Sheets (prende dati aggiornati)
- Lavora normalmente
- Salva su Google Sheets (condivide con altri)
- Ripeti spesso!

### Vantaggi
- Tutti vedono stessi dati in tempo reale
- Backup automatico su Google Drive
- Accesso da qualsiasi dispositivo
- Storico versioni di Google Sheets
- Multi utente reale

### Best Practice
- Carica sempre prima di modificare
- Salva spesso
- Usa Chat interna per coordinarsi
- Non modificare stesso volontario contemporaneamente
