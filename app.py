import streamlit as st

st.set_page_config(page_title="📚 Hausaufgaben-Bot", page_icon="📖")
st.title("📚 Hausaufgaben-Bot")

# --- LOGIN ---
PASSWORD = "Padawan985!"  # dein Passwort
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
subjects = ["Mathe", "Deutsch", "Englisch", "Biologie", "Chemie", "Physik", 
            "Geschichte", "Geographie", "Sport", "Kunst", "Musik"]

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
    st.subheader("🗑️ Hausaufgaben löschen")
    # 1️⃣ Datum komplett löschen
    all_dates = list(st.session_state.hausaufgaben.keys())
    if all_dates:
        del_date = st.selectbox("📅 Ganzes Datum löschen", all_dates, key="del_date_all")
        if st.button("🗑️ Datum löschen"):
            if del_date in st.session_state.hausaufgaben:
                del st.session_state.hausaufgaben[del_date]
                st.success(f"🗑️ Alle Aufgaben am {del_date} gelöscht!")

    # 2️⃣ Einzelne Aufgabe löschen
    if all_dates:
        date_for_subject = st.selectbox("📅 Datum auswählen für einzelne Aufgabe", all_dates, key="del_date_subject")
        subjects_for_date = list(st.session_state.hausaufgaben[date_for_subject].keys())
        if subjects_for_date:
            subject_to_delete = st.selectbox("📘 Fach auswählen", subjects_for_date, key="del_subject_single")
            if st.button("🗑️ Einzelne Aufgabe löschen"):
                del st.session_state.hausaufgaben[date_for_subject][subject_to_delete]
                st.success(f"🗑️ {subject_to_delete} am {date_for_subject} gelöscht!")
                # Wenn danach kein Fach mehr am Datum ist, Datum auch löschen
                if not st.session_state.hausaufgaben[date_for_subject]:
                    del st.session_state.hausaufgaben[date_for_subject]

# --- ABFRAGE ---
query_date = st.text_input("🔍 Datum eingeben (z.B. 21.7.1):", key="query_date")

if query_date in st.session_state.hausaufgaben:
    st.write("### 📖 Hausaufgaben:")
    for fach, aufgabe in st.session_state.hausaufgaben[query_date].items():
        st.write(f"- **{fach}**: {aufgabe}")
elif query_date:
    st.warning("❌ Keine Hausaufgaben für dieses Datum gefunden.")
