import streamlit as st
import random
import time
import urllib.parse

st.set_page_config(page_title="🎅 Tajny Mikołaj Deluxe", page_icon="🎁", layout="centered")

# -------------------- CSS --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #00111a 0%, #004466 100%);
    overflow: hidden;
}
.snowflake {
    position: fixed;
    top: -10px;
    z-index: 9999;
    color: white;
    font-size: 1em;
    user-select: none;
    animation-name: fall;
    animation-timing-function: linear;
}
@keyframes fall {
    0% { top: -10px; opacity: 1; }
    100% { top: 110vh; opacity: 0; }
}
.reveal {
    font-size: 1.3rem;
    color: #004b23;
    background-color: #fff4e6;
    padding: 1rem;
    border-radius: 15px;
    animation: fadeIn 1.5s ease forwards;
    border: 2px dashed #d62828;
    box-shadow: 0 0 15px rgba(255, 100, 100, 0.5);
}
@keyframes fadeIn {
    0% { opacity: 0; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1); }
}
</style>
<script>
const snowflakes = 30;
for (let i = 0; i < snowflakes; i++) {
  const snowflake = document.createElement('div');
  snowflake.classList.add('snowflake');
  snowflake.textContent = '❄';
  snowflake.style.left = Math.random() * 100 + 'vw';
  snowflake.style.animationDuration = 5 + Math.random() * 10 + 's';
  snowflake.style.fontSize = 10 + Math.random() * 20 + 'px';
  snowflake.style.opacity = 0.3 + Math.random() * 0.7;
  snowflake.style.animationDelay = Math.random() * 10 + 's';
  document.body.appendChild(snowflake);
}
</script>
""", unsafe_allow_html=True)

# -------------------- Konfiguracja --------------------
organizer_password = "Mikolaj2025"

if "assignments" not in st.session_state:
    st.session_state.assignments = None

query_params = st.experimental_get_query_params()
user_param = query_params.get("user", [None])[0]

# -------------------- Widok uczestnika --------------------
if user_param:
    st.title("🎁 Twój Prezent Tajnego Mikołaja 🎅")
    name = urllib.parse.unquote(user_param)

    if st.session_state.assignments and name in st.session_state.assignments:
        if st.button("🎁 Otwórz prezent!"):
            placeholder = st.empty()
            with placeholder.container():
                st.markdown(
                    f"<div class='reveal'>🎄 {name}, wylosowałeś/aś: "
                    f"<strong>{st.session_state.assignments[name]}</strong> 🎁</div>",
                    unsafe_allow_html=True
                )
                st.info("Wynik zniknie automatycznie po 10 sekundach ⏳")
                time.sleep(10)
                placeholder.empty()
                st.warning("⏰ Czas minął — prezent schowany! 🤫")
    else:
        st.warning("🎅 Losowanie jeszcze się nie odbyło lub Twoje imię nie znajduje się na liście.")
    st.stop()

# -------------------- Widok organizatora --------------------
st.title("🎄 Tajny Mikołaj — Panel Organizatora")
if "authorized" not in st.session_state:
    st.session_state.authorized = False

if not st.session_state.authorized:
    with st.expander("🔑 Zaloguj się jako organizator"):
        password = st.text_input("Hasło:", type="password")
        if st.button("✅ Zaloguj"):
            if password == organizer_password:
                st.session_state.authorized = True
                st.success("Zalogowano pomyślnie!")
            else:
                st.error("❌ Niepoprawne hasło.")
    if not st.session_state.authorized:
        st.stop()

# -------------------- Panel losowania --------------------
st.subheader("🧑‍🎄 Wprowadź uczestników")
names_input = st.text_area("Każde imię w nowej linii:")
if names_input.strip():
    names = [n.strip() for n in names_input.split("\n") if n.strip()]
else:
    names = []

if len(names) < 2:
    st.warning("⚠️ Wprowadź przynajmniej 2 osoby.")
else:
    if st.button("🎲 Wylosuj pary"):
        success = False
        tries = 0
        while not success and tries < 100:
            available = names.copy()
            assignments = {}
            success = True
            for generator in names:
                options = [n for n in available if n != generator]
                if not options:
                    success = False
                    break
                draw = random.choice(options)
                assignments[generator] = draw
                available.remove(draw)
            tries += 1

        if not success:
            st.error("❌ Nie udało się wylosować unikalnych par. Spróbuj ponownie.")
        else:
            st.session_state.assignments = assignments
            st.success("🎁 Losowanie zakończone!")
            st.balloons()

# -------------------- Linki --------------------
if st.session_state.assignments:
    st.divider()
    st.subheader("🔗 Indywidualne linki dla uczestników")

    base_url = st.experimental_get_query_params()
    app_url = st.experimental_get_url()
    # Usuń parametry, jeśli istnieją
    app_url = app_url.split('?')[0]

    for name in st.session_state.assignments.keys():
        encoded = urllib.parse.quote(name)
        link = f"{app_url}?user={encoded}"
        st.markdown(f"🎅 **{name}** → [Otwórz swój prezent]({link})")
