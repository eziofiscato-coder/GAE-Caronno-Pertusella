"""
GAE - Google Sheets Multi Utente
Sistema per sincronizzare tutti i dati del gestionale su Google Sheets
Permette a più utenti di lavorare sullo stesso database in tempo reale
"""

import json
import os
from datetime import datetime
import pandas as pd

# Configurazione Sheets
SHEETS_CONFIG = {
    "volontari": ["Nome", "Cognome", "Comune", "Via", "CapoODV", "ODVAppartenenza", "DataNascita", "CodFisc", "Cellulare", "Email", "TelEmergenza", "Ruolo", "Squadra", "RadioID", "ModelloRadio", "Documento", "DocNum", "ScadDoc", "DataIns"],
    "ospiti": ["Nome", "Cognome", "Comune", "Via", "ODVAppartenenza", "Cellulare", "Email", "Ruolo", "DataIns"],
    "radio_db": ["IDRadio", "Modello", "Stato", "AssegnataA", "DataAcquisto", "Note"],
    "consegna_radio": ["Volontario", "IDRadio", "DataConsegna", "DataRestituzione", "Note"],
    "alias_radio": ["Alias", "Descrizione", "Frequenza", "Note"],
    "mappa_avanzata_markers": ["Nome", "Alias", "Lat", "Lon", "Comune", "Via", "NomeEmergenza", "NomeEvento", "NomeVolontario", "CognomeVolontario", "CellVolontario", "ODV", "VolontarioCompleto", "Tipo", "Provider", "Descrizione", "DataIns"],
    "eventi": ["Nome", "Data", "Luogo", "Descrizione", "Stato"],
    "emergenze": ["Nome", "Data", "Luogo", "Priorita", "Stato", "Descrizione"],
    "interventi": ["Data", "Ora", "Squadra", "Tipo", "Luogo", "Descrizione", "Stato"],
    "mezzi": ["Nome", "Tipo", "Targa", "Stato", "Note"],
    "attrezzature": ["Nome", "Categoria", "Quantita", "Stato", "Note"],
    "icone": ["Nome", "Emoji", "Colore", "Tipo"],
    "utenti": ["username", "nome", "ruolo", "attivo"]
}

def get_mock_sheets_client():
    """Client mock per test senza credenziali"""
    return None

def connect_google_sheets(credentials_json=None, credentials_file=None):
    """
    Connette a Google Sheets usando service account
    credentials_json: dict con credenziali JSON
    credentials_file: path file JSON credenziali
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        if credentials_json:
            creds = Credentials.from_service_account_info(credentials_json, scopes=scopes)
        elif credentials_file and os.path.exists(credentials_file):
            creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        else:
            # Cerca file default
            for f in ["google_credentials.json", "credentials.json", "/mnt/data/google_credentials.json"]:
                if os.path.exists(f):
                    creds = Credentials.from_service_account_file(f, scopes=scopes)
                    break
            else:
                return None, "File credenziali non trovato. Carica google_credentials.json"
        
        client = gspread.authorize(creds)
        return client, "Connesso"
    except ImportError as e:
        return None, f"Librerie mancanti: {e} - Aggiungi gspread e google-auth a requirements.txt"
    except Exception as e:
        return None, f"Errore connessione: {e}"

def create_spreadsheet_structure(client, title="GAE Protezione Civile - Multi Utente"):
    """Crea un nuovo spreadsheet con struttura completa"""
    try:
        spreadsheet = client.create(title)
        # Condividi con chiunque abbia link? No, l'utente deve condividere manualmente
        
        # Crea worksheets per ogni tabella
        for sheet_name, columns in SHEETS_CONFIG.items():
            try:
                ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(columns)+5)
                ws.append_row(columns)  # Header
            except:
                # Worksheet già esiste
                pass
        
        # Rimuovi Sheet1 default se esiste
        try:
            sheet1 = spreadsheet.worksheet("Sheet1")
            spreadsheet.del_worksheet(sheet1)
        except:
            pass
        
        return spreadsheet, f"Spreadsheet creato: {spreadsheet.url}"
    except Exception as e:
        return None, f"Errore creazione: {e}"

def save_to_sheets(client, spreadsheet_id, data_dict):
    """Salva dati su Google Sheets"""
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        results = []
        
        for sheet_name, columns in SHEETS_CONFIG.items():
            if sheet_name not in data_dict:
                continue
            
            data_list = data_dict.get(sheet_name, [])
            if not data_list:
                continue
            
            try:
                ws = spreadsheet.worksheet(sheet_name)
            except:
                ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(columns)+5)
                ws.append_row(columns)
            
            # Pulisci e riscrivi
            ws.clear()
            ws.append_row(columns)
            
            # Prepara righe
            rows = []
            for item in data_list:
                if isinstance(item, dict):
                    row = []
                    for col in columns:
                        val = item.get(col, "")
                        # Pulisci valori non serializzabili
                        if isinstance(val, bytes):
                            val = ""
                        elif isinstance(val, (dict, list)):
                            val = json.dumps(val, default=str)[:500]
                        row.append(str(val)[:500])
                    rows.append(row)
            
            if rows:
                # Scrivi in batch da 100 righe
                for i in range(0, len(rows), 100):
                    batch = rows[i:i+100]
                    ws.append_rows(batch)
            
            results.append(f"{sheet_name}: {len(rows)} righe")
        
        return True, f"Salvato: {', '.join(results)}"
    except Exception as e:
        return False, f"Errore salvataggio: {e}"

def load_from_sheets(client, spreadsheet_id):
    """Carica dati da Google Sheets"""
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        data_dict = {}
        
        for sheet_name in SHEETS_CONFIG.keys():
            try:
                ws = spreadsheet.worksheet(sheet_name)
                records = ws.get_all_records()
                # Filtra righe vuote
                clean_records = []
                for r in records:
                    # Se almeno un campo non vuoto
                    if any(str(v).strip() for v in r.values()):
                        clean_records.append(r)
                data_dict[sheet_name] = clean_records
            except:
                data_dict[sheet_name] = []
        
        return data_dict, f"Caricato {sum(len(v) for v in data_dict.values())} record totali"
    except Exception as e:
        return {}, f"Errore caricamento: {e}"

def sync_status_file():
    """File per tracciare ultimo sync"""
    return "google_sheets_sync.json"

def save_sync_info(spreadsheet_id, user=""):
    info = {
        "spreadsheet_id": spreadsheet_id,
        "last_sync": datetime.now().isoformat(),
        "last_user": user,
        "url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    }
    try:
        with open(sync_status_file(), 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2)
    except:
        pass
    return info

def load_sync_info():
    try:
        if os.path.exists(sync_status_file()):
            with open(sync_status_file(), 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

# Funzioni per Streamlit UI
def render_google_sheets_ui():
    """UI Streamlit per configurazione Google Sheets"""
    import streamlit as st
    
    st.markdown("""
    ### 🌐 Google Sheets Multi Utente
    Sincronizza tutti i dati su Google Sheets per lavorare in più utenti in tempo reale
    """)
    
    sync_info = load_sync_info()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Ultimo Sync:** {sync_info.get('last_sync', 'Mai')[:19] if sync_info.get('last_sync') else 'Mai'}")
        if sync_info.get('url'):
            st.markdown(f"[📊 Apri Google Sheet]({sync_info['url']})")
    with col2:
        if sync_info.get('spreadsheet_id'):
            st.code(sync_info['spreadsheet_id'], language="text")
    
    st.divider()
    
    # Configurazione
    st.subheader("⚙️ Configurazione")
    
    # Input Spreadsheet ID
    spreadsheet_id = st.text_input(
        "Spreadsheet ID (dalla URL di Google Sheets)",
        value=sync_info.get('spreadsheet_id', ''),
        placeholder="Es: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        help="Prendi ID dalla URL: https://docs.google.com/spreadsheets/d/QUESTO_ID/edit"
    )
    
    # Credenziali
    st.markdown("**Credenziali Service Account**")
    st.caption("Crea un service account su https://console.cloud.google.com/ e scarica JSON")
    
    uploaded_creds = st.file_uploader("Carica google_credentials.json", type=["json"])
    creds_json = None
    if uploaded_creds:
        try:
            creds_json = json.load(uploaded_creds)
            st.success(f"✅ Credenziali caricate: {creds_json.get('client_email', 'N/D')}")
            # Salva file per uso futuro
            with open("google_credentials.json", "w") as f:
                json.dump(creds_json, f)
        except Exception as e:
            st.error(f"Errore lettura credenziali: {e}")
    
    # Prova connessione
    if st.button("🔌 Testa Connessione Google Sheets", use_container_width=True):
        client, msg = connect_google_sheets(credentials_json=creds_json)
        if client:
            st.success(f"✅ {msg}")
            if spreadsheet_id:
                try:
                    sheet = client.open_by_key(spreadsheet_id)
                    st.success(f"✅ Spreadsheet trovato: {sheet.title}")
                    st.info(f"Titolo: {sheet.title} - {len(sheet.worksheets())} fogli")
                except Exception as e:
                    st.error(f"Spreadsheet non accessibile: {e}")
                    st.warning("Condividi il foglio con l'email del service account: " + (creds_json.get('client_email', '') if creds_json else ''))
        else:
            st.error(f"❌ {msg}")
    
    st.divider()
    
    # Azioni Sync
    st.subheader("🔄 Sincronizzazione")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("📤 Salva su Google Sheets", type="primary", use_container_width=True):
            if not spreadsheet_id:
                st.error("Inserisci Spreadsheet ID")
            else:
                client, msg = connect_google_sheets(credentials_json=creds_json)
                if not client:
                    st.error(msg)
                else:
                    # Raccogli dati da session_state
                    data_dict = {}
                    for key in SHEETS_CONFIG.keys():
                        if key in st.session_state:
                            data_dict[key] = st.session_state[key]
                    
                    # Aggiungi anche backup_eventi e altri
                    with st.spinner("Salvataggio in corso..."):
                        ok, res = save_to_sheets(client, spreadsheet_id, data_dict)
                        if ok:
                            st.success(res)
                            save_sync_info(spreadsheet_id, st.session_state.get('username', ''))
                            st.balloons()
                        else:
                            st.error(res)
    
    with col_b:
        if st.button("📥 Carica da Google Sheets", use_container_width=True):
            if not spreadsheet_id:
                st.error("Inserisci Spreadsheet ID")
            else:
                client, msg = connect_google_sheets(credentials_json=creds_json)
                if not client:
                    st.error(msg)
                else:
                    with st.spinner("Caricamento in corso..."):
                        data_dict, res = load_from_sheets(client, spreadsheet_id)
                        if data_dict:
                            # Carica in session_state
                            for k, v in data_dict.items():
                                st.session_state[k] = v
                            st.success(res)
                            save_sync_info(spreadsheet_id, st.session_state.get('username', ''))
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(res)
    
    with col_c:
        if st.button("🆕 Crea Nuovo Spreadsheet", use_container_width=True):
            client, msg = connect_google_sheets(credentials_json=creds_json)
            if not client:
                st.error(msg)
            else:
                with st.spinner("Creazione spreadsheet..."):
                    sheet, res = create_spreadsheet_structure(client, f"GAE Protezione Civile - {datetime.now().strftime('%Y-%m-%d')}")
                    if sheet:
                        st.success(res)
                        st.markdown(f"[📊 Apri: {sheet.url}]({sheet.url})")
                        st.code(sheet.id)
                        save_sync_info(sheet.id, st.session_state.get('username', ''))
                        # Condividi info
                        st.warning(f"IMPORTANTE: Condividi questo foglio con {creds_json.get('client_email', 'service account') if creds_json else 'il service account'} con permesso Editor, altrimenti non funzionerà per altri utenti")
                    else:
                        st.error(res)
    
    st.divider()
    st.markdown("""
    #### 📖 Istruzioni Multi Utente:
    
    1. **Crea Service Account:**
       - Vai su https://console.cloud.google.com/
       - Crea progetto → Abilita Google Sheets API e Drive API
       - Crea Service Account → Scarica JSON
       - Carica JSON qui sopra
    
    2. **Crea Spreadsheet:**
       - Clicca "Crea Nuovo Spreadsheet"
       - Condividi il foglio con l'email del service account (Editor)
       - Condividi anche con tutti gli utenti che devono collaborare
    
    3. **Uso Quotidiano:**
       - Ogni utente apre il gestionale
       - Clicca "Carica da Google Sheets" per prendere dati aggiornati
       - Lavora normalmente
       - Clicca "Salva su Google Sheets" per condividere con altri
    
    4. **Multi Utente Reale:**
       - Tutti vedono stessi dati
       - Se due utenti modificano contemporaneamente, l'ultimo che salva vince
       - Consigliato: sincronizzare spesso (carica prima di modificare, salva dopo)
    """)
