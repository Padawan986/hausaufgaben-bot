import streamlit as st
import gspread
import pandas as pd

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
# GOOGLE SHEET VERBINDUNG (öffentlicher Link)
# -----------------------
PUBLIC_SHEET_URL = "https://docs.google.com/spreadsheets/d/1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU/edit?usp=sharing"
SHEET_ID = PUBLIC_SHEET_URL.split("/")[5]

try:
    gc = gspread.public()  # Zugriff auf öffentliche Sheets
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.sheet1
    st.success("✅ Öffentlicher Google Sheet erfolgreich verbunden!")
except Exception as e:
    st.error(f"❌ Fehler beim Öffnen des Sheets: {e}")

# -----------------------
# Hilfsfunktionen
# -----------------------
def load_hw():
    data = worksheet.get_all_records()
    hw = {}
    for row in data:
        date, fach, task = row["Datum"], row["Fach"], row["Aufgabe"]
        if date not in hw:
            hw[date] = {}
        hw[date][fach] = task
    return hw

def save_hw(date, fach, task):
    worksheet.append_row([date, fach, task])

def delete_hw(date, fach=None):
    all_records = worksheet.get_all_records()
    worksheet.clear()
    worksheet.append_row(["Datum", "Fach", "Aufgabe"])  # Header
    for row in all_records:
        r_date, r_fach, r_task = row["Datum"], row["Fach"], row["Aufgabe"]
        if fach:
            if not (r_date == date and r_fach == fach):
                worksheet.append_row([r_date, r_fach, r_task])
        else:
            if r_date != date:
                worksheet.append_row([r_date, r_fach, r_task])

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
for date, fachs in hw_data.items():
    st.markdown(f"**{date}**")
    for fach, task in fachs.items():
        st.write(f"- {fach}: {task}")
