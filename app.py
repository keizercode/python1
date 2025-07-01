import streamlit as st
import random
import json
import os

# Konfigurasi game
MIN_NUMBER = 1
MAX_NUMBER = 10
MAX_ATTEMPTS = 3
SCOREBOARD_FILE = "scoreboard.json"

# ====== FUNGSI ======
def load_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    converted = {}
                    for entry in data:
                        name = entry.get("nama") or "Anonim"
                        converted[name] = converted.get(name, 0) + 1
                    return converted
                return data
            except:
                return {}
    return {}

def save_scoreboard(scoreboard):
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scoreboard, f)

def add_win_to_scoreboard(winner):
    scoreboard = load_scoreboard()
    scoreboard[winner] = scoreboard.get(winner, 0) + 1
    save_scoreboard(scoreboard)

def reset_game():
    st.session_state.secret = None
    st.session_state.attempts = MAX_ATTEMPTS
    st.session_state.history = []
    st.session_state.guessed_correctly = False
    st.session_state.ready_to_play = False
    st.session_state.turns_randomized = False
    st.session_state.penebak = ""
    st.session_state.penyimpan = ""


# ====== LOGIKA APP ======
st.title("🎮 Game Tebak Angka - Giliran Acak")

scoreboard = load_scoreboard()

# Input nama pemain
col1, col2 = st.columns(2)
with col1:
    player1 = st.text_input("👤 Nama Player 1:")
with col2:
    player2 = st.text_input("🎭 Nama Player 2:")

# Init state
if "secret" not in st.session_state:
    reset_game()

# Random giliran
if player1 and player2 and not st.session_state.turns_randomized:
    if st.button("🎲 Acak Giliran & Mulai"):
        names = [player1, player2]
        random.shuffle(names)
        st.session_state.penebak = names[0]
        st.session_state.penyimpan = names[1]
        st.session_state.turns_randomized = True
        st.success(f"Giliran acak selesai! 🎯 {st.session_state.penyimpan} menyimpan angka rahasia, {st.session_state.penebak} akan menebak.")

# Masukkan angka rahasia
if st.session_state.turns_randomized and not st.session_state.ready_to_play:
    secret_input = st.text_input(f"{st.session_state.penyimpan}, masukkan angka rahasia ({MIN_NUMBER}-{MAX_NUMBER}):", type="password")
    if st.button("🔒 Simpan Angka Rahasia"):
        if secret_input.isdigit():
            num = int(secret_input)
            if MIN_NUMBER <= num <= MAX_NUMBER:
                st.session_state.secret = num
                st.session_state.ready_to_play = True
                st.success(f"✅ Angka disimpan! Sekarang {st.session_state.penebak} menebak!")
            else:
                st.error(f"Masukkan angka antara {MIN_NUMBER}-{MAX_NUMBER}.")
        else:
            st.error("❌ Input tidak valid.")

# Gameplay
if st.session_state.ready_to_play and st.session_state.attempts > 0 and not st.session_state.guessed_correctly:
    guess = st.number_input(f"{st.session_state.penebak}, tebak angka:", min_value=MIN_NUMBER, max_value=MAX_NUMBER, step=1)
    if st.button("✅ Submit Tebakan"):
        if guess in st.session_state.history:
            st.warning("⚠️ Kamu sudah menebak angka ini.")
        else:
            st.session_state.history.append(guess)

            if guess == st.session_state.secret:
                st.success(f"🎉 Selamat {st.session_state.penebak}, kamu berhasil nebak angkanya!")
                st.session_state.guessed_correctly = True
                add_win_to_scoreboard(st.session_state.penebak)
            elif guess > st.session_state.secret:
                st.info("📉 Terlalu besar.")
            else:
                st.info("📈 Terlalu kecil.")

            st.session_state.attempts = max(0, st.session_state.attempts - 1)

    st.write(f"📜 Tebakan sejauh ini: {', '.join(map(str, st.session_state.history))}")
    st.write(f"❤️ Sisa kesempatan: {st.session_state.attempts}")

# Game selesai
if (st.session_state.guessed_correctly or st.session_state.attempts == 0) and st.session_state.ready_to_play:
    if not st.session_state.guessed_correctly:
        st.error(f"💀 {st.session_state.penebak} gagal nebak. Angkanya adalah: {st.session_state.secret}")
        add_win_to_scoreboard(st.session_state.penyimpan)

    if st.button("🔁 Main Lagi"):
        reset_game()
        st.experimental_rerun()

# Scoreboard
with st.expander("🏆 Scoreboard Menang"):
    if scoreboard:
        sorted_scores = sorted(scoreboard.items(), key=lambda x: x[1], reverse=True)
        for i, (nama, skor) in enumerate(sorted_scores, 1):
            st.markdown(f"**{i}. {nama}** - 🏅 {skor} kemenangan")
    else:
        st.write("Belum ada pemenang.")
