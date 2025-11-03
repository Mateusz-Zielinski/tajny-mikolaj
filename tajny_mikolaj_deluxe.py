import streamlit as st
import random
import time
import json
import os
import io

# ------------------------------
# 🎅 Konfiguracja aplikacji
# ------------------------------
st.set_page_config(page_title="Tajny Mikołaj 🎁", page_icon="🎅", layout="centered")

PASSWORD = "Mikolaj2025"
IMIONA = ["Sonia", "Mateusz", "Marzena", "Edek", "Martyna", "Jacek"]
ASSIGN_FILE = "assignments.json"

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
# 💾 Wczytaj istniejące losowanie
# ------------------------------
if "assignments" not in st.session_state:
    if os.path.exists(ASSIGN_FILE):
        with open(ASSIGN_FILE, "r", encoding="utf-8") as f:
            st.session_state.assignments = json.load(f)
    else:
        st.session_state.assignments = {}

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ------------------------------
# 🎅 Losowanie par
# ------------------------------
def wylosuj_pary():
    available = IMIONA.copy()
    recipients = IMIONA.copy()
    assignments = {}

    for giver in available:
        possible = [p for p in recipients if p != giver and p not in BANNED.get(giver, [])]
        if not possible:
            return None
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
        st.snow()
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

    st.success("✅ Zalogowano jako organizator.")

    # 🎲 Losowanie
    if st.button("🎲 Wylosuj pary"):
        pairs = None
        for _ in range(10):
            pairs = wylosuj_pary()
            if pairs:
                break
        if pairs:
            st.session_state.assignments = pairs
            with open(ASSIGN_FILE, "w", encoding="utf-8") as f:
                json.dump(pairs, f, ensure_ascii=False, indent=2)
            st.success("✅ Pomyślnie wylosowano pary! Plik zapisany jako assignments.json")

            # 📥 Przycisk do pobrania pliku
            json_bytes = json.dumps(pairs, ensure_ascii=False, indent=2).encode('utf-8')
            st.download_button(
                label="📥 Pobierz assignments.json",
                data=json_bytes,
                file_name="assignments.json",
                mime="application/json"
            )
        else:
            st.error("❌ Nie udało się wylosować poprawnych par. Spróbuj ponownie.")

    # ❌ Czyszczenie
    if st.button("❌ Wyczyść losowanie"):
        st.session_state.assignments = {}
        if os.path.exists(ASSIGN_FILE):
            os.remove(ASSIGN_FILE)
        st.warning("Wszystkie losowania zostały wyczyszczone.")
        st.rerun()

    # 📜 Podgląd par
    if st.session_state.assignments:
        st.markdown("### 📜 Wylosowane pary:")
        for giver, receiver in st.session_state.assignments.items():
            st.write(f"🎁 **{giver} ➜ {receiver}**")

        # 🔗 Linki
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
