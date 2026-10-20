
"""
GAE - Multi Utente SENZA Service Account Key
Soluzione alternativa per quando l'organizzazione blocca la creazione chiavi
Usa Google Sheets pubblico condiviso + sincronizzazione via CSV/Excel
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def render_google_sheets_simple_ui():
    """Versione semplice senza service account - usa Google Sheet condiviso"""
    st.markdown("""
    ### 🌐 Multi Utente SEMPLICE - Senza Service Account
    
    **Per organizzazioni che bloccano le chiavi service account**
    Usa Google Sheets condiviso manualmente - Nessuna chiave richiesta!
    """)
    
    st.info("**Metodo 1: Google Sheet condiviso + Copia/Incolla (funziona subito)**")
    
    st.markdown("""
    #### Come funziona senza chiavi:
    
    1. **Crea Google Sheet** su https://sheets.google.com
       - Chiamalo "GAE Protezione Civile - Multi Utente"
       - Crea fogli: volontari, mappa_avanzata_markers, radio_db, ecc.
    
    2. **Condividi** con tutti: Mimmo, Pietro, Ezio con permesso Editor
    
    3. **Uso:**
       - Ogni utente apre gestionale → fa modifiche
       - Esporta Excel da Backup → incolla dati nel Google Sheet condiviso
       - Altri utenti importano da Google Sheet
    
    Questo funziona SUBITO senza sbloccare policy!
    """)
    
    st.divider()
    
    # Esportazione per Google Sheets
    st.subheader("📤 Esporta per Google Sheets Condiviso")
    
    if st.button("📥 Prepara file Excel per Google Sheets Condiviso", type="primary", use_container_width=True):
        try:
            # Raccogli tutti i dati
            all_data = {}
            keys = ["volontari", "ospiti", "radio_db", "consegna_radio", "alias_radio", "mappa_avanzata_markers", "eventi", "emergenze", "interventi", "mezzi", "attrezzature"]
            for k in keys:
                if k in st.session_state and st.session_state[k]:
                    # Pulisci dati non serializzabili
                    clean = []
                    for item in st.session_state[k]:
                        if isinstance(item, dict):
                            c = {kk: str(vv)[:500] if not isinstance(vv, (str,int,float,bool)) else vv for kk,vv in item.items() if "Bytes" not in kk and "B64" not in kk}
                            clean.append(c)
                    if clean:
                        all_data[k] = pd.DataFrame(clean)
            
            if all_data:
                # Crea Excel multi-foglio
                output = pd.ExcelWriter(f"/tmp/gae_multiutente_{datetime.now().strftime('%Y%m%d')}.xlsx", engine='xlsxwriter')
                for sheet_name, df in all_data.items():
                    df.to_excel(output, sheet_name=sheet_name[:31], index=False)
                output.close()
                
                st.success(f"✅ Preparato {len(all_data)} fogli - Carica questo file su Google Sheets!")
                st.info("Su Google Sheets: File → Importa → Carica → Sostituisci fogli")
            else:
                st.warning("Nessun dato da esportare")
        except Exception as e:
            st.error(f"Errore: {e}")
    
    st.divider()
    st.subheader("📥 Importa da Google Sheets Condiviso")
    st.markdown("Scarica Google Sheet come Excel e caricalo qui:")
    
    uploaded = st.file_uploader("Carica Excel scaricato da Google Sheets", type=["xlsx", "xls"])
    if uploaded:
        try:
            xls = pd.ExcelFile(uploaded)
            st.write(f"Fogli trovati: {xls.sheet_names}")
            if st.button("✅ Importa tutti i fogli nel gestionale", type="primary", use_container_width=True):
                for sheet in xls.sheet_names:
                    try:
                        df = pd.read_excel(xls, sheet_name=sheet)
                        df = df.dropna(how='all')
                        records = df.to_dict(orient="records")
                        if records:
                            # Mappa nome foglio a chiave session_state
                            key_map = {
                                "volontari": "volontari",
                                "ospiti": "ospiti",
                                "radio_db": "radio_db",
                                "consegna_radio": "consegna_radio",
                                "alias_radio": "alias_radio",
                                "mappa_avanzata_markers": "mappa_avanzata_markers",
                                "mappe": "mappa_avanzata_markers",
                                "eventi": "eventi",
                                "emergenze": "emergenze",
                                "interventi": "interventi",
                                "mezzi": "mezzi",
                                "attrezzature": "attrezzature"
                            }
                            for k,v in key_map.items():
                                if k in sheet.lower():
                                    st.session_state[v] = records
                                    st.success(f"Importato {len(records)} in {v}")
                    except Exception as e:
                        st.error(f"Errore foglio {sheet}: {e}")
                st.balloons()
                st.rerun()
        except Exception as e:
            st.error(f"Errore lettura: {e}")

# Per compatibilità
def render_google_sheets_ui():
    render_google_sheets_simple_ui()
