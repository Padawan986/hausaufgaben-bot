import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# -----------------------
# Seite konfigurieren
# -----------------------
st.set_page_config(page_title="📚 Hausaufgaben-Bot", page_icon="📖")
st.title("📚 Hausaufgaben-Bot")

# -----------------------
# LOGIN
# -----------------------
PASSWORD = "1234"  # Passwort ändern
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
# GOOGLE SHEET VERBINDUNG
# -----------------------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Secrets müssen in Streamlit Cloud unter "Secrets" hinzugefügt werden:
# GOOGLE_CREDS_JSON = <dein JSON-Inhalt als String>
creds_dict = json.loads(st.secrets["GOOGLE_CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open_by_key("1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU").sheet1

# -----------------------
# Hilfsfunktionen
# -----------------------
def load_hw():
    data = sheet.get_all_records()
    hw = {}
    for row in data:
        date, fach, task = row["Datum"], row["Fach"], row["Aufgabe"]
        if date not in hw:
            hw[date] = {}
        hw[date][fach] = task
    return hw

def save_hw(date, fach, task):
    sheet.append_row([date, fach, task])

def delete_hw(date, fach=None):
    all_records = sheet.get_all_records()
    sheet.clear()
    sheet.append_row(["Datum", "Fach", "Aufgabe"])  # Header
    for row in all_records:
        r_date, r_fach, r_task = row["Datum"], row["Fach"], row["Aufgabe"]
        if fach:
            if not (r_date == date and r_fach == fach):
                sheet.append_row([r_date, r_fach, r_task])
        else:
            if r_date != date:
                sheet.append_row([r_date, r_fach, r_task])

# -----------------------
# Fächerliste
# -----------------------
subjects = ["Mathe", "Deutsch", "Englisch", "Biologie", "Chemie", "Physik",
            "Geschichte", "Geographie", "Sport", "Kunst", "Musik"]

hw_data = load_hw()

# -----------------------
# Hausaufgaben hinzufügen
# -----------------------
if st.session_state.logged_in:
    with st.form("add_hw"):
        date = st.text_input("📅 Datum (z.B. 21.09.2025)")
        fach = st.selectbox("📚 Fach auswählen", subjects)
        task = st.text_area("📝 Aufgabe")
        submitted = st.form_submit_button("➕ Hinzufügen")
        if submitted:
            save_hw(date, fach, task)
            st.success(f"✅ Hausaufgabe für {fach} am {date} hinzugefügt!")

# -----------------------
# Hausaufgaben löschen
# -----------------------
if st.session_state.logged_in:
    with st.form("delete_hw"):
        date = st.text_input("📅 Datum löschen")
        fach = st.selectbox("📚 Fach löschen (optional)", [""] + subjects)
        submitted = st.form_submit_button("❌ Löschen")
        if submitted:
            delete_hw(date, fach if fach else None)
            st.success(f"✅ Hausaufgaben gelöscht!")

# -----------------------
# Anzeige
# -----------------------
st.subheader("📋 Alle Hausaufgaben")
hw_data = load_hw()  # Daten nach Änderungen neu laden
for date, fachs in hw_data.items():
    st.markdown(f"**{date}**")
    for fach, task in fachs.items():
        st.write(f"- {fach}: {task}")
