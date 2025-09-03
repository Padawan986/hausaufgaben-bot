import streamlit as st

st.set_page_config(page_title="📚 Hausaufgaben-Bot", page_icon="📖")
st.title("📚 Hausaufgaben-Bot")

# --- LOGIN ---
PASSWORD = "Padawan985.2012!"  # hier dein Passwort einstellen
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

# --- HAUSAUFGABEN DATEN ---
subjects = ["Mathe", "Deutsch", "Englisch", "Biologie", "Chemie", "Physik", "Geschichte", "Geographie", "Sport", "Kunst", "Musik"]

if "hausaufgaben" not in st.session_state:
    st.session_state.hausaufgaben = {
        "21.7.1": {"Mathe": "Seite 21/4", "Deutsch": "Seite 32/3", "Englisch": "-"}
    }

# --- HAUSAUFGABEN HINZUFÜGEN ---
if st.session_state.logged_in:
    with st.form("add_hw"):
        date = st.text_input("📅 Datum (z.B. 21.7.1)", key="add_date")
        subject = st.selectbox("📘 Fach auswählen", subjects, key="add_subject")
        task = st.text_input("✏️ Aufgabe", key="add_task")
        submit = st.form_submit_button("➕ Hinzufügen")

        if submit and date and subject and task:
            if date not in st.session_state.hausaufgaben:
                st.session_state.hausaufgaben[date] = {}
            st.session_state.hausaufgaben[date][subject] = task
            st.success(f"✅ Aufgabe hinzugefügt: {subject} → {task} ({date})")

# --- HAUSAUFGABEN LÖSCHEN ---
if st.session_state.logged_in:
    with st.form("delete_hw"):
        date_del = st.text_input("📅 Datum löschen (z.B. 21.7.1)", key="del_date")
        subject_del = st.selectbox("📘 Fach löschen", subjects, key="del_subject")
        delete = st.form_submit_button("🗑️ Löschen")
        if delete:
            if date_del in st.session_state.hausaufgaben and subject_del in st.session_state.hausaufgaben[date_del]:
                del st.session_state.hausaufgaben[date_del][subject_del]
                st.success(f"🗑️ {subject_del} für {date_del} gelöscht!")
                # falls kein Fach mehr an dem Datum existiert
                if not st.session_state.hausaufgaben[date_del]:
                    del st.session_state.hausaufgaben[date_del]
            else:
                st.warning("❌ Keine solche Aufgabe gefunden.")

# --- ABFRAGE ---
query_date = st.text_input("🔍 Datum eingeben (z.B. 21.7.1):", key="query_date")

if query_date in st.session_state.hausaufgaben:
    st.write("### 📖 Hausaufgaben:")
    for fach, aufgabe in st.session_state.hausaufgaben[query_date].items():
        st.write(f"- **{fach}**: {aufgabe}")
elif query_date:
    st.warning("❌ Keine Hausaufgaben für dieses Datum gefunden.")
