import streamlit as st
import pandas as pd
import random
import time
import urllib.parse

# ==============================
#  ŚWIĄTECZNA APLIKACJA 2025 🎅
# ==============================

st.set_page_config(page_title="Tajny Mikołaj Deluxe 2025", page_icon="🎁", layout="centered")

# --- Świąteczny CSS + tło ---
page_bg = """
<style>
body {
    background: linear-gradient(180deg, #003366 0%, #336699 50%, #99ccff 100%);
    background-attachment: fixed;
    color: white;
}
h1, h2, h3, h4, h5, h6 { text-align: center; color: #fff; }
footer {visibility: hidden;}
.snowflake {
    position: fixed;
    top: 0;
    color: white;
    font-size: 1.2em;
    animation-name: fall;
    animation-timing-function: linear;
}
@keyframes fall {
    0% { top: -10px; opacity: 1; }
    100% { top: 100vh; opacity: 0; }
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Efekt spadającego śniegu ---
for i in range(25):
    st.markdown(
        f"<div class='snowflake' style='left: {random.randint(0,100)}%; animation-duration: {random.randint(8,15)}s; animation-delay: {random.random()}s;'>❄️</div>",
        unsafe_allow_html=True
    )

# --- Dane na stałe ---
uczestnicy = ["Sonia", "Mateusz", "Marzena", "Edek", "Martyna", "Jacek"]
wykluczenia = {
    "Mateusz": ["Sonia"],
    "Sonia": ["Mateusz"],
    "Jacek": ["Martyna"],
    "Martyna": ["Jacek"],
    "Marzena": ["Edek"],
    "Edek": ["Marzena"]
}

# --- Hasło organizatora ---
HASLO = "Mikolaj2025"

# --- Funkcja losująca pary ---
def losuj_pary(uczestnicy, wykluczenia):
    losowani = uczestnicy.copy()
    pary = {}
    for osoba in uczestnicy:
        mozliwi = [x for x in losowani if x != osoba and x not in wykluczenia.get(osoba, [])]
        if not mozliwi:
            return None  # brak możliwości poprawnego losowania
        wybor = random.choice(mozliwi)
        pary[osoba] = wybor
        losowani.remove(wybor)
    return pary

# --- Sekcja aplikacji ---
st.title("🎅 Tajny Mikołaj Deluxe 2025 🎁")
st.markdown("**Świąteczna wioska pełna prezentów!** 🌲✨")

# --- Stan aplikacji ---
if "pary" not in st.session_state:
    st.session_state.pary = None

# --- Sprawdzenie parametrów URL ---
params = st.query_params
if "user" in params and st.session_state.pary:
    user = params["user"]
    if user in st.session_state.pary:
        odbiorca = st.session_state.pary[user]
        st.subheader("🎁 Otwierasz prezent...")
        time.sleep(1)
        st.success(f"Wesołych Świąt 🎅! Jesteś Tajnym Mikołajem dla **{odbiorca}** 🎄")
        st.markdown("<p style='text-align:center; color:gold;'>🎉🎄🎉</p>", unsafe_allow_html=True)
        time.sleep(10)
        st.warning("🎅 Wynik ukryty — nie podglądaj ponownie! 🎁")
        st.stop()
    else:
        st.error("🎅 Nie znaleziono Twojego imienia w losowaniu.")
        st.stop()

# --- Panel organizatora ---
st.subheader("🔒 Panel organizatora")

input_haslo = st.text_input("Wpisz hasło, aby przeprowadzić losowanie:", type="password")

if input_haslo == HASLO:
    if st.button("🎁 Wylosuj pary"):
        pary = None
        for _ in range(1000):
            pary = losuj_pary(uczestnicy, wykluczenia)
            if pary:
                break
        if not pary:
            st.error("Nie udało się wylosować poprawnych par! Spróbuj ponownie.")
        else:
            st.session_state.pary = pary
            st.success("🎄 Losowanie zakończone sukcesem!")
            st.balloons()

    if st.session_state.pary:
        st.subheader("📜 Wyniki (tylko dla organizatora)")
        df = pd.DataFrame(list(st.session_state.pary.items()), columns=["Osoba", "Prezent dla"])
        st.dataframe(df)

        st.markdown("### 🔗 Indywidualne linki dla uczestników")
        base_url = "https://tajny-mikolaj.streamlit.app"
        for osoba in uczestnicy:
            link = f"{base_url}/?user={urllib.parse.quote(osoba)}"
            st.markdown(f"🎅 **{osoba}:** [Kliknij, by otworzyć prezent]({link})")
else:
    st.info("🧑‍🎄 Wpisz hasło organizatora, aby rozpocząć losowanie.")

