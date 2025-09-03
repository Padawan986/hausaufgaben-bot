import streamlit as st
import pandas as pd
import requests
from io import StringIO

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
# GOOGLE SHEET VERBINDUNG (öffentlich, CSV)
# -----------------------
PUBLIC_SHEET_CSV = "https://docs.google.com/spreadsheets/d/1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU/export?format=csv"

def load_hw():
    try:
        resp = requests.get(PUBLIC_SHEET_CSV)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text))
        hw = {}
        for _, row in df.iterrows():
            date, fach, task = row["Datum"], row["Fach"], row["Aufgabe"]
            if date not in hw:
                hw[date] = {}
            hw[date][fach] = task
        return hw
    except Exception as e:
        st.error(f"❌ Fehler beim Laden des Sheets: {e}")
        return {}

hw_data = load_hw()

# -----------------------
# Fächerliste
# -----------------------
subjects = ["Mathe", "Deutsch", "Englisch", "Biologie", "Chemie", "Physik",
            "Geschichte", "Geographie", "Sport", "Kunst", "Musik"]

# -----------------------
# Anzeige
# -----------------------
st.subheader("📋 Alle Hausaufgaben")
if hw_data:
    for date, fachs in hw_data.items():
        st.markdown(f"**{date}**")
        for fach, task in fachs.items():
            st.write(f"- {fach}: {task}")
else:
    st.info("Keine Hausaufgaben gefunden oder Fehler beim Laden des Sheets.")
