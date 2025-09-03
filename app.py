import streamlit as st

st.set_page_config(page_title="📚 Hausaufgaben-Bot", page_icon="📖")

st.title("📚 Hausaufgaben-Bot")

# Fächer-Liste (kannst du beliebig erweitern)
subjects = ["Mathe", "Deutsch", "Englisch", "Biologie", "Chemie", "Physik", "Geschichte", "Geographie", "Sport", "Kunst", "Musik"]

# Speicher für Hausaufgaben (normalerweise Datenbank, hier nur als dict)
if "hausaufgaben" not in st.session_state:
    st.session_state.hausaufgaben = {
        "21.7.1": {"Mathe": "Seite 21/4", "Deutsch": "Seite 32/3", "Englisch": "-"}
    }

# Eingabeformular zum Hinzufügen
with st.form("add_hw"):
    date = st.text_input("📅 Datum (z.B. 21.7.1)")
    subject = st.selectbox("📘 Fach auswählen", subjects)
    task = st.text_input("✏️ Aufgabe")
    submit = st.form_submit_button("➕ Hinzufügen")

    if submit and date and subject and task:
        if date not in st.session_state.hausaufgaben:
            st.session_state.hausaufgaben[date] = {}
        st.session_state.hausaufgaben[date][subject] = task
        st.success(f"✅ Aufgabe hinzugefügt: {subject} → {task} ({date})")

# Abfragefeld
query_date = st.text_input("🔍 Datum eingeben (z.B. 21.7.1):")

if query_date in st.session_state.hausaufgaben:
    st.write("### 📖 Hausaufgaben:")
    for fach, aufgabe in st.session_state.hausaufgaben[query_date].items():
        st.write(f"- **{fach}**: {aufgabe}")
elif query_date:
    st.warning("❌ Keine Hausaufgaben für dieses Datum gefunden.")
