import streamlit as st
import random
import time

st.set_page_config(page_title="🎅 Tajny Mikołaj Deluxe", page_icon="🎁", layout="centered")

# --- CSS: Zimowa wioska + śnieg + animacje ---
st.markdown("""
    <style>
        body {
            margin: 0;
            background: linear-gradient(to bottom, #00111a 0%, #00334d 100%);
            overflow: hidden;
        }

        /* Tło - zimowa wioska SVG */
        .winter-bg {
            position: fixed;
            bottom: 0;
            width: 100%;
            height: 40vh;
            background: url('data:image/svg+xml;utf8,
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
                    <path fill="%23ffffff" fill-opacity="1" d="M0,192L60,186.7C120,181,240,171,360,160C480,149,600,139,720,154.7C840,171,960,213,1080,213.3C1200,213,1320,171,1380,149.3L1440,128L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"></path>
                </svg>');
            background-repeat: no-repeat;
            background-size: cover;
            animation: glow 4s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { filter: brightness(0.9); }
            to { filter: brightness(1.2); }
        }

        /* Śnieg */
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

        [data-testid="stAppViewContainer"] {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(8px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
        }

        h1, h2, h3 {
            color: #b30000 !important;
            text-align: center;
        }

        .stButton>button {
            background-color: #e63946;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff4d6d;
            transform: scale(1.05);
        }

        /* Efekt otwierania prezentu */
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

        /* Styl par dla organizatora */
        .pair-card {
            margin: 10px 0;
            padding: 10px;
            background: #f0fff4;
            border-left: 6px solid #2d6a4f;
            border-radius: 10px;
            font-size: 1.1rem;
            color: #004b23;
        }

        .pair-card:nth-child(even) {
            background: #fff4f4;
            border-left: 6px solid #e63946;
        }
    </style>

    <script>
        const snowflakes = 40;
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

        const bg = document.createElement('div');
        bg.classList.add('winter-bg');
        document.body.appendChild(bg);
    </script>
""", unsafe_allow_html=True)

# --------------------- Tytuł ---------------------
st.title("🎄 Tajny Mikołaj — Zimowa Wioska 🎁")
st.markdown("""
✨ Witaj w magicznej wiosce Świętego Mikołaja! ✨  
Każdy uczestnik wylosuje **inną osobę**, ale zobaczy **tylko swój wynik**.  
Kliknij **„Otwórz prezent” 🎁**, aby odkryć, kogo obdarowujesz — wynik zniknie po **10 sekundach**!
""")

st.divider()

# --------------------- Hasło organizatora ---------------------
organizer_password = "Mikolaj2025"
if "authorized" not in st.session_state:
    st.session_state["authorized"] = False

if not st.session_state["authorized"]:
    with st.expander("🔑 Panel organizatora"):
        password = st.text_input("Wprowadź hasło, aby rozpocząć losowanie:", type="password")
        if st.button("✅ Zaloguj"):
            if password == organizer_password:
                st.session_state["authorized"] = True
                st.success("🎁 Zalogowano pomyślnie! Można rozpocząć losowanie.")
            else:
                st.error("❌ Niepoprawne hasło.")
    if not st.session_state["authorized"]:
        st.stop()

# --------------------- Imiona ---------------------
st.subheader("🧑‍🎄 Wprowadź uczestników")
names_input = st.text_area(
    "✏️ Każde imię w nowej linii:",
    placeholder="np.\nAnna\nBartek\nCelina\nDamian\nEla\nFranek"
)

if names_input.strip():
    names = [n.strip() for n in names_input.split("\n") if n.strip()]
else:
    names = []

if len(names) < 2:
    st.warning("⚠️ Wprowadź przynajmniej 2 osoby, aby rozpocząć losowanie.")
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
            st.session_state["assignments"] = assignments
            st.balloons()
            st.success("✅ Losowanie zakończone! 🎅 Uczestnicy mogą teraz otwierać swoje prezenty.")

# --------------------- Otwieranie prezentu ---------------------
if "assignments" in st.session_state:
    st.divider()
    st.subheader("🎁 Otwórz swój prezent")
    selected_name = st.selectbox("Wybierz swoje imię:", ["(wybierz)"] + names)

    if selected_name != "(wybierz)":
        if st.button("🎁 Otwórz prezent!"):
            placeholder = st.empty()
            with placeholder.container():
                st.markdown(
                    f"<div class='reveal'>🎄 {selected_name}, wylosowałeś/aś: "
                    f"<strong>{st.session_state['assignments'][selected_name]}</strong> 🎁</div>",
                    unsafe_allow_html=True
                )
                st.info("Wynik zniknie automatycznie po 10 sekundach ⏳")
                time.sleep(10)
                placeholder.empty()
                st.warning("⏰ Czas minął — prezent schowany! 🤫")

    # --------------------- Tryb organizatora ---------------------
    st.divider()
    with st.expander("🧑‍💼 Widok organizatora (pełna lista par)"):
        admin_pass = st.text_input("🔐 Wprowadź hasło organizatora, aby podejrzeć listę:", type="password")
        if st.button("👀 Pokaż pełną listę"):
            if admin_pass == organizer_password:
                st.success("✅ Dostęp przyznany! Oto pełna lista losowania:")
                for giver, receiver in st.session_state["assignments"].items():
                    st.markdown(f"<div class='pair-card'>🎁 <b>{giver}</b> ➜ <i>{receiver}</i></div>", unsafe_allow_html=True)
            else:
                st.error("❌ Niepoprawne hasło — brak dostępu.")
