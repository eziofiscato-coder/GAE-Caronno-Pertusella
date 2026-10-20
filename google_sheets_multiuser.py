
"""
GAE - Multi Utente SENZA Service Account Key
Soluzione alternativa per quando l'organizzazione blocca la creazione chiavi
Usa Google Sheets pubblico condiviso + sincronizzazione via Excel
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime

def render_google_sheets_simple_ui():
    st.markdown("""
    ### 🌐 Multi Utente SEMPLICE - Senza Service Account
    **Questa versione NON ha bisogno di cliccare su JSON!**
    Funziona anche con il blocco organizzazione.
    """)
    
    st.success("✅ **Nessuna chiave service account richiesta!**")
    
    st.markdown("""
    #### Come funziona (senza JSON):
    1. **Crea Google Sheet** su https://sheets.google.com
       - Chiamalo "GAE Protezione Civile - Multi Utente"
    2. **Condividi** con Mimmo, Pietro, Ezio con permesso **Editor**
    3. **Nel gestionale:** Esporta Excel qui sotto → caricalo su Google Sheets
    4. **Altri utenti:** Scaricano da Google Sheets → Importano qui
    """)
    
    st.divider()
    st.subheader("📤 1. Esporta dati per Google Sheets")
    
    if st.button("📥 Prepara Excel per Google Sheets", type="primary", use_container_width=True):
        try:
            all_data = {}
            keys = ["volontari", "ospiti", "radio_db", "consegna_radio", "alias_radio", "mappa_avanzata_markers", "eventi", "emergenze", "interventi", "mezzi", "attrezzature", "spese_odv"]
            for k in keys:
                if k in st.session_state and st.session_state[k]:
                    try:
                        items = st.session_state[k]
                        if not items:
                            continue
                        clean = []
                        for item in items:
                            if isinstance(item, dict):
                                c = {}
                                for kk,vv in item.items():
                                    if "Bytes" in kk or "B64" in kk or "b64" in kk.lower():
                                        continue
                                    try:
                                        if isinstance(vv, (str,int,float,bool)) or vv is None:
                                            c[kk] = vv
                                        else:
                                            c[kk] = str(vv)[:200]
                                    except:
                                        c[kk] = str(vv)[:200]
                                clean.append(c)
                        if clean:
                            all_data[k] = pd.DataFrame(clean)
                    except Exception as e:
                        st.warning(f"Salto {k}: {e}")
            
            if not all_data:
                st.warning("Nessun dato da esportare - Aggiungi volontari, mappe, radio, ecc. prima")
                return
                
            # Crea Excel in memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in all_data.items():
                    df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            
            output.seek(0)
            st.success(f"✅ Preparato {len(all_data)} fogli: {', '.join(all_data.keys())}")
            
            st.download_button(
                label="⬇️ SCARICA Excel per Google Sheets",
                data=output,
                file_name=f"GAE_Multiutente_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.info("Ora vai su sheets.google.com → File → Importa → Carica questo file → Sostituisci fogli")
            
        except Exception as e:
            st.error(f"Errore: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    st.divider()
    st.subheader("📥 2. Importa da Google Sheets Condiviso")
    st.markdown("Scarica il Google Sheet come Excel (File → Scarica → Microsoft Excel) e caricalo qui:")
    
    uploaded = st.file_uploader("Carica Excel scaricato da Google Sheets", type=["xlsx", "xls"], key="gs_upload")
    if uploaded:
        try:
            xls = pd.ExcelFile(uploaded)
            st.write(f"Fogli trovati: {xls.sheet_names}")
            if st.button("✅ Importa TUTTI i fogli nel gestionale", type="primary", use_container_width=True, key="import_all"):
                count_total = 0
                for sheet in xls.sheet_names:
                    try:
                        df = pd.read_excel(xls, sheet_name=sheet)
                        df = df.dropna(how='all')
                        if df.empty:
                            continue
                        records = df.to_dict(orient="records")
                        if records:
                            # pulizia
                            clean_records = []
                            for r in records:
                                cr = {k: v for k,v in r.items() if pd.notna(v)}
                                clean_records.append(cr)
                            
                            # mappa
                            key_map = {
                                "volontari": "volontari",
                                "ospiti": "ospiti",
                                "radio_db": "radio_db",
                                "consegna_radio": "consegna_radio",
                                "alias_radio": "alias_radio",
                                "mappa_avanzata": "mappa_avanzata_markers",
                                "mappe": "mappa_avanzata_markers",
                                "eventi": "eventi",
                                "emergenze": "emergenze",
                                "interventi": "interventi",
                                "mezzi": "mezzi",
                                "attrezzature": "attrezzature",
                                "spese": "spese_odv"
                            }
                            target_key = None
                            sl = sheet.lower()
                            for k,v in key_map.items():
                                if k in sl:
                                    target_key = v
                                    break
                            if not target_key:
                                target_key = sl
                            
                            if target_key in ["volontari", "ospiti", "radio_db", "consegna_radio", "alias_radio", "mappa_avanzata_markers", "eventi", "emergenze", "interventi", "mezzi", "attrezzature", "spese_odv"]:
                                st.session_state[target_key] = clean_records
                                st.success(f"Importato {len(clean_records)} in {target_key}")
                                count_total += len(clean_records)
                    except Exception as e:
                        st.error(f"Errore foglio {sheet}: {e}")
                if count_total>0:
                    st.balloons()
                    st.success(f"✅ Importati {count_total} record totali! Vai su Dashboard per vederli.")
                else:
                    st.warning("Nessun record importato")
        except Exception as e:
            st.error(f"Errore lettura: {e}")

    st.divider()
    st.subheader("🔄 Metodo alternativo ULTRA SEMPLICE")
    st.markdown("""
    Se anche questo è complicato:
    1. In **Backup** → **Esporta tutto** → scarica Excel
    2. Carica quel file su Google Drive condiviso con Mimmo e Pietro
    3. Loro da **Backup** → **Importa** → caricano il file
    4. Fine! Multi utente senza chiavi!
    """)

def render_google_sheets_ui():
    render_google_sheets_simple_ui()
