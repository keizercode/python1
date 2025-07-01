import streamlit as st
import random
import json
import os

# Konfigurasi game
MIN_NUMBER = 1
MAX_NUMBER = 10
MAX_ATTEMPTS = 3
SCOREBOARD_FILE = "scoreboard.json"

# Fungsionalitas file scoreboard
def load_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_scoreboard(scoreboard):
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scoreboard, f)

def add_win_to_scoreboard(winner):
    scoreboard = load_scoreboard()
    if winner in scoreboard:
        scoreboard[winner] += 1
    else:
        scoreboard[winner] = 1
    save_scoreboard(scoreboard)

def reset_game():
    st.session_state.secret = None
    st.session_state.attempts = MAX_ATTEMPTS
    st.session_state.history = []
    st.session_state.guessed_correctly = False
    st.session_state.ready_to_play = False

# Title
st.title("🎮 Game Tebak Angka - Dua Pemain")

# Scoreboard lokal
scoreboard = load_scoreboard()

# Input nama pemain
col1, col2 = st.columns(2)
with col1:
    player1_name = st.text_input("👤 Nama Player 1 (Penebak):")
with col2:
    player2_name = st.text_input("🎭 Nama Player 2 (Pemilik angka):")

# Inisialisasi state
if "secret" not in st.session_state:
    reset_game()

# Player 2 masukkan angka rahasia
if player1_name and player2_name and not st.session_state.ready_to_play:
    secret_input = st.text_input(f"{player2_name}, masukkan angka rahasia ({MIN_NUMBER}-{MAX_NUMBER}):", type="password")
    if st.button("Mulai Game"):
        if secret_input.isdigit():
            num = int(secret_input)
            if MIN_NUMBER <= num <= MAX_NUMBER:
                st.session_state.secret = num
                st.session_state.ready_to_play = True
                st.success(f"Angka rahasia disimpan. {player1_name}, giliranmu menebak!")
            else:
                st.error(f"Angka harus antara {MIN_NUMBER}-{MAX_NUMBER}")
        else:
            st.error("Masukkan angka valid!")

# Gameplay
if st.session_state.ready_to_play and st.session_state.attempts > 0 and not st.session_state.guessed_correctly:
    guess = st.number_input(f"{player1_name}, tebak angka:", min_value=MIN_NUMBER, max_value=MAX_NUMBER, step=1)

    if st.button("Submit Tebakan"):
        if guess in st.session_state.history:
            st.warning("⚠️ Kamu sudah menebak angka ini.")
        else:
            st.session_state.history.append(guess)
            if guess == st.session_state.secret:
                st.success(f"🎉 Selamat {player1_name}, kamu berhasil menebak angka!")
                st.session_state.guessed_correctly = True
                add_win_to_scoreboard(player1_name)
            elif guess > st.session_state.secret:
                st.info("📉 Terlalu besar.")
            else:
                st.info("📈 Terlalu kecil.")

            st.session_state.attempts = max(0, st.session_state.attempts - 1)

    st.write(f"🧾 Riwayat Tebakan: {', '.join(map(str, st.session_state.history))}")
    st.write(f"❤️ Sisa kesempatan: {st.session_state.attempts}")

# Game over
if (st.session_state.guessed_correctly or st.session_state.attempts == 0) and st.session_state.ready_to_play:
    if not st.session_state.guessed_correctly:
        st.error(f"💀 Sayang sekali, {player1_name} gagal menebak. Angka: {st.session_state.secret}")
        add_win_to_scoreboard(player2_name)

    if st.button("🔁 Main Lagi"): 
        reset_game() 
        st.session_state.game_started = False  # ✅ biar bisa mulai ulang dengan bersih
        

# Tampilkan scoreboard
with st.expander("🏆 Scoreboard Menang"):
    if scoreboard:
        sorted_scores = sorted(scoreboard.items(), key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(sorted_scores, 1):
            st.markdown(f"**{i}. {name}** - 🏅 {score} kemenangan")
    else:
        st.write("Belum ada pemenang.")
