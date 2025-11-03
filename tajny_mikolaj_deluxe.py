import streamlit as st
import random
import time

# ------------------------------
# 🎅 Konfiguracja aplikacji
# ------------------------------
st.set_page_config(page_title="Tajny Mikołaj 🎁", page_icon="🎅", layout="centered")

PASSWORD = "Mikolaj2025"
IMIONA = ["Sonia", "Mateusz", "Marzena", "Edek", "Martyna", "Jacek"]

# Niedozwolone pary (obustronnie)
BANNED = {
    "Sonia": ["Mateusz"],
    "Mateusz": ["Sonia"],
    "Jacek": ["Martyna"],
    "Martyna": ["Jacek"],
    "Marzena": ["Edek"],
    "Edek": ["Marzena"],
}

# ------------------------------
# 💾 Stan aplikacji
# ------------------------------
if "assignments" not in st.session_state:
    st.session_state.assignments = {}
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ------------------------------
# 🎨 CSS i animacje
# ------------------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #003366 0%, #001122 100%);
        color: white;
        text-align: center;
    }
    .snowflake {
        position: fixed;
        top: 0;
        color: white;
        font-size: 24px;
        animation: fall 10s linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-10%); opacity: 1; }
        100% { transform: translateY(110vh); opacity: 0; }
    }
    .house {
        position: absolute;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #ffd700;
        font-size: 12px;
    }
    .present {
        background-color: #b30000;
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 10px #ff0000;
        cursor: pointer;
        transition: 0.3s;
    }
    .present:hover {
        background-color: #ff1a1a;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# 🎅 Funkcja losująca
# ------------------------------
def wylosuj_pary():
    available = IMIONA.copy()
    recipients = IMIONA.copy()
    assignments = {}

    for giver in available:
        possible = [p for p in recipients if p != giver and p not in BANNED.get(giver, [])]
        if not possible:
            return None  # wylosowanie się nie powiodło, spróbuj ponownie
        chosen = random.choice(possible)
        assignments[giver] = chosen
        recipients.remove(chosen)

    return assignments

# ------------------------------
# 🎁 Widok uczestnika
# ------------------------------
def show_user_view(user):
    st.title("🎄 Twój Prezent Tajnego Mikołaja 🎁")

    if user not in IMIONA:
        st.error("Twoje imię nie znajduje się na liście uczestników.")
        return

    if user not in st.session_state.assignments:
        st.warning("Losowanie jeszcze się nie odbyło lub nie masz przypisanego prezentu.")
        return

    st.markdown(f"### Witaj, **{user}**! 🎅")
    if st.button("🎁 Otwórz prezent!"):
        result = st.session_state.assignments[user]
        st.balloons()
        st.markdown(f"## 🎄 Wesołych Świąt 🎅! Jesteś Tajnym Mikołajem dla **{result}** 🎁")
        time.sleep(10)
        st.rerun()

# ------------------------------
# 🧑‍💼 Panel administratora
# ------------------------------
def show_admin_panel():
    st.title("🎅 Panel Organizatora Tajnego Mikołaja 🎄")

    if not st.session_state.admin_logged:
        password = st.text_input("🔑 Wprowadź hasło:", type="password")
        if st.button("Zaloguj"):
            if password == PASSWORD:
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("❌ Niepoprawne hasło.")
        return

    # Po zalogowaniu
    st.success("✅ Zalogowano jako organizator.")
    if st.button("🎲 Wylosuj pary"):
        pairs = None
        for _ in range(10):  # kilka prób, by uniknąć kolizji
            pairs = wylosuj_pary()
            if pairs:
                break
        if pairs:
            st.session_state.assignments = pairs
            st.success("✅ Pomyślnie wylosowano pary!")
        else:
            st.error("❌ Nie udało się wylosować poprawnych par. Spróbuj ponownie.")

    if st.button("❌ Wyczyść losowanie"):
        st.session_state.assignments = {}
        st.warning("Wszystkie losowania zostały wyczyszczone.")
        st.rerun()

    if st.session_state.assignments:
        st.markdown("### 📜 Wylosowane pary:")
        for giver, receiver in st.session_state.assignments.items():
            st.write(f"🎁 **{giver} ➜ {receiver}**")

        st.markdown("### 🔗 Indywidualne linki:")
        base_url = "https://tajny-mikolaj.streamlit.app"
        for name in IMIONA:
            st.code(f"{base_url}/?user={name}", language="text")

# ------------------------------
# 🚦 Routing
# ------------------------------
query_params = st.query_params
user_param = query_params.get("user", [None])[0] if isinstance(query_params.get("user"), list) else query_params.get("user")

if user_param:
    show_user_view(user_param)
else:
    show_admin_panel()
