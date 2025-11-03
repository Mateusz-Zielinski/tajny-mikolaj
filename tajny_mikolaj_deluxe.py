# tajny_mikolaj_deluxe.py  (ZASTĄP CAŁY POPRZEDNI PLIK)
import streamlit as st
import pandas as pd
import random
import time
import urllib.parse
import json
import os

st.set_page_config(page_title="Tajny Mikołaj Deluxe 2025", page_icon="🎁", layout="centered")

DATA_FILE = "assignments.json"
HASLO = "Mikolaj2025"

# ----------------- CSS i efekty (prostota) -----------------
st.markdown("""
<style>
body {
  background: linear-gradient(180deg,#00161a 0%, #00334d 50%, #e6f7ff 100%);
  color: #111;
}
h1,h2,h3 { text-align:center; color:#8b0000; }
.card {
  background: rgba(255,255,255,0.9);
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.2);
}
.reveal {
  font-size: 1.25rem;
  color: #083d2b;
  background: linear-gradient(90deg,#fff8e1,#fff);
  padding: 1rem;
  border-radius: 12px;
  border: 2px solid #d62828;
  text-align: center;
}
.confetti {
  text-align:center;
  font-size: 2rem;
}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# --- Stałe imiona i wykluczenia ---
uczestnicy = ["Sonia", "Mateusz", "Marzena", "Edek", "Martyna", "Jacek"]
wykluczenia = {
    "Mateusz": ["Sonia"],
    "Sonia": ["Mateusz"],
    "Jacek": ["Martyna"],
    "Martyna": ["Jacek"],
    "Marzena": ["Edek"],
    "Edek": ["Marzena"]
}

# ----------------- Funkcje zapisu/odczytu -----------------
def load_assignments():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # upewnij się, że klucze to str
                return {str(k): str(v) for k,v in data.items()}
        except Exception:
            return {}
    return {}

def save_assignments(assignments):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(assignments, f, ensure_ascii=False, indent=2)

def attempt_draw(names, exclusions, max_attempts=2000):
    """Próbuje losować unikalne przypisania z wykluczeniami."""
    for _ in range(max_attempts):
        available = names.copy()
        random.shuffle(available)
        pairs = {}
        ok = True
        for giver in names:
            # wybieramy spośród dostępnych tych nie będących giver i nie na liście wykluczeń
            choices = [c for c in available if c != giver and c not in exclusions.get(giver, [])]
            if not choices:
                ok = False
                break
            pick = random.choice(choices)
            pairs[giver] = pick
            available.remove(pick)
        if ok:
            return pairs
    return None

# ----------------- Obsługa zapytania URL (uczestnik) -----------------
params = st.experimental_get_query_params()
user_param = params.get("user", [None])[0]  # None lub string

# najpierw wczytaj istniejące przypisania z pliku (zanim zrobimy cokolwiek)
assignments = load_assignments()

# Jeśli ktoś wszedł z linku ?user=Imię -> pokaż widok uczestnika (NIE pokazuj panelu admina)
if user_param:
    name = urllib.parse.unquote(user_param)
    st.title("🎁 Twój Prezent — Tajny Mikołaj")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if assignments and name in assignments:
        if st.button("🎁 Otwórz prezent!"):
            # efekt "otwierania" (animacja prosta: krótka pauza)
            with st.spinner("Otwieram prezent..."):
                time.sleep(1.0)
            # tekst po odkryciu
            recipient = assignments[name]
            st.markdown(f"<div class='reveal'>Wesołych Świąt 🎅! Jesteś Tajnym Mikołajem dla<br><b>{recipient}</b></div>", unsafe_allow_html=True)
            # konfetti świąteczne (prostym tekstem/emotikonkami)
            st.markdown("<div class='confetti'>🎉🎄✨ 🎉 <span style='color:gold'>✨</span> 🎉</div>", unsafe_allow_html=True)
            st.info("Wynik zniknie automatycznie za 10 sekund. Nie pokazuj ekranu innym 😉")
            time.sleep(10)
            st.experimental_rerun()  # po upływie czasu odświeżamy, żeby ukryć wynik
        else:
            st.info("Kliknij „Otwórz prezent!\", aby zobaczyć, kogo obdarowujesz.")
    else:
        st.warning("🎅 Losowanie jeszcze się nie odbyło lub Twoje imię nie znajduje się na liście.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ----------------- Widok organizatora -----------------
st.title("🎄 Tajny Mikołaj — Panel Organizatora")
st.markdown("<div class='card'>", unsafe_allow_html=True)

if "authorized" not in st.session_state:
    st.session_state.authorized = False

if not st.session_state.authorized:
    with st.expander("🔑 Panel organizatora (zaloguj)"):
        pwd = st.text_input("Hasło organizatora:", type="password")
        if st.button("Zaloguj"):
            if pwd == HASLO:
                st.session_state.authorized = True
                st.success("Zalogowano pomyślnie ✅")
                # odśwież, by pokazać panel
                st.experimental_rerun()
            else:
                st.error("Niepoprawne hasło.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Tutaj jesteśmy jako zalogowany organizator
st.success("Jesteś zalogowany jako organizator. Możesz przeprowadzić losowanie lub podejrzeć wyniki.")
st.divider()

# Pokaż bieżące przypisania (jeśli istnieją)
if assignments:
    st.subheader("📜 Obecne przypisania (zapisane)")
    df_show = pd.DataFrame(list(assignments.items()), columns=["Osoba", "Wylosowany(a)"])
    st.dataframe(df_show, use_container_width=True)
else:
    st.info("Brak zapisanych przypisań. Wykonaj losowanie.")

st.write("")  # odstęp

# Przyciski: losuj na nowo / wyczyść zapis / pokaż linki
col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("🎲 Wylosuj pary"):
        result = attempt_draw(uczestnicy, wykluczenia)
        if not result:
            st.error("Nie udało się wygenerować par spełniających wszystkie wykluczenia. Spróbuj ponownie.")
        else:
            assignments = result
            save_assignments(assignments)
            st.success("🎁 Losowanie zakończone i zapisane.")
            st.experimental_rerun()

with col2:
    if st.button("🗑️ Wyczyść zapis (usuń plik)"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        assignments = {}
        st.success("Plik przypisań usunięty.")
        st.experimental_rerun()

with col3:
    if st.button("🔗 Pokaż linki dla uczestników"):
        if not assignments:
            st.warning("Najpierw wykonaj losowanie.")
        else:
            st.info("Gotowe linki (wyślij uczestnikom). Każdy link pokazuje tylko daną osobę.")
            st.markdown("---")
            # ustaw poprawny adres swojej aplikacji tutaj:
            app_url = "https://tajny-mikolaj.streamlit.app"  # <- ZMIEŃ na swój adres Streamlit
            data = []
            for osoba in uczestnicy:
                enc = urllib.parse.quote(osoba)
                link = f"{app_url}/?user={enc}"
                st.markdown(f"🎅 **{osoba}** → [Otwórz prezent]({link})")
                data.append({"Imię": osoba, "Link": link})
            # pobieranie CSV
            df_links = pd.DataFrame(data)
            csv = df_links.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Pobierz linki (CSV)", data=csv, file_name="tajny_mikolaj_linki.csv", mime="text/csv")

st.markdown("</div>", unsafe_allow_html=True)
