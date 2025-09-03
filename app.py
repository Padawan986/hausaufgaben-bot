import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(page_title="📚 Hausaufgaben-Bot", page_icon="📖")
st.title("📚 Hausaufgaben-Bot")

# -----------------------
# LOGIN
# -----------------------
PASSWORD = "1234"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pwd = st.text_input("🔒 Passwort eingeben:", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Erfolgreich eingeloggt!")
        else:
            st.error("❌ Falsches Passwort")
else:
    st.info("Du bist eingeloggt. Hausaufgaben können hinzugefügt oder gelöscht werden.")

# -----------------------
# GOOGLE SHEET VERBINDUNG MIT DEBUG
# -----------------------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

try:
    creds_dict = json.loads(st.secrets["GOOGLE_CREDS_JSON"])
    st.write("✅ Secrets geladen")
except Exception as e:
    st.error(f"❌ Fehler beim Laden der Secrets: {e}")

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    st.write("✅ Credentials erstellt")
except Exception as e:
    st.error(f"❌ Fehler beim Erstellen der Credentials: {e}")

try:
    client = gspread.authorize(creds)
    st.write("✅ Client autorisiert")
except Exception as e:
    st.error(f"❌ Fehler bei der Autorisierung: {e}")

try:
    sheet = client.open_by_key("1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU").sheet1
    st.write("✅ Sheet geöffnet")
except Exception as e:
    st.error(f"❌ Fehler beim Öffnen des Sheets: {e}")
try:
    sheet = client.open_by_key("1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU").sheet1
    st.write("✅ Sheet geöffnet")
    st.write("Erste Zeile:", sheet.row_values(1))
except Exception as e:
    st.error(f"❌ Fehler beim Öffnen des Sheets: {e}")
