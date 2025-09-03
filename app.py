import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

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

# JSON-Key aus Streamlit Secret
creds_dict = json.loads(st.secrets["GOOGLE_CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open_by_key("1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU").sheet1  # Sheet-ID anpassen

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
    sheet.append_row(["Datum", "Fach", "Aufgabe"])  # Header wieder hinzufügen
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
        date = st.text_input("📅 Datum (z.B. 21.7.1)", key="add_date")
        subject = st.selectbox("📘 Fach auswählen", subjects, key="add_subject")
        task = st.text_input("✏️ Aufgabe", key="add_task")
        submit = st.form_submit_button("➕ Hinzufügen")
        if submit and date and subject and task:
            save_hw(date, subject, task)
            st.success(f"✅ Aufgabe hinzugefügt: {subject} → {task} ({date})")
            hw_data = load_hw()

# -----------------------
# Hausaufgaben löschen
# -----------------------
if st.session_state.logged_in:
    st.subheader("🗑️ Hausaufgaben löschen")
    all_dates = list(hw_data.keys())
    if all_dates:
        del_date = st.selectbox("📅 Ganzes Datum löschen", all_dates, key="del_date_all")
        if st.button("🗑️ Datum löschen"):
            delete_hw(del_date)
            st.success(f"🗑️ Alle Aufgaben am {del_date} gelöscht!")
            hw_data = load_hw()

        date_for_subject = st.selectbox("📅 Datum auswählen für einzelne Aufgabe", all_dates, key="del_date_subject")
        subjects_for_date = list(hw_data[date_for_subject].keys())
        if subjects_for_date:
            subject_to_delete = st.selectbox("📘 Fach auswählen", subjects_for_date, key="del_subject_single")
            if st.button("🗑️ Einzelne Aufgabe löschen"):
                delete_hw(date_for_subject, subject_to_delete)
                st.success(f"🗑️ {subject_to_delete} am {date_for_subject} gelöscht!")
                hw_data = load_hw()

# -----------------------
# Hausaufgaben abfragen
# -----------------------
query_date = st.text_input("🔍 Datum eingeben (z.B. 21.7.1):", key="query_date")
if query_date in hw_data:
    st.write("### 📖 Hausaufgaben:")
    for fach, task in hw_data[query_date].items():
        st.write(f"- **{fach}**: {task}")
elif query_date:
    st.warning("❌ Keine Hausaufgaben für dieses Datum gefunden.")
