import streamlit as st
import random
import json
import os

# ----- KONFIGURASI -----
MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 5
SCOREBOARD_FILE = "scoreboard.json"

# ----- FUNGSI BANTUAN -----
def load_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_scoreboard(scoreboard):
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scoreboard, f)

def reset_game():
    st.session_state.secret = None
    st.session_state.attempts = MAX_ATTEMPTS
    st.session_state.history = []
    st.session_state.guessed_correctly = False
    st.session_state.ready_to_play = False
    st.session_state.player_name = ""

# ----- UI & LOGIKA -----
st.title("🎮 Game Tebak Angka")
scoreboard = load_scoreboard()

# --- Mode ---
mode = st.selectbox("Pilih Mode Permainan:", ["Versus Komputer", "Versus Player 2"])

# --- State awal ---
if "secret" not in st.session_state:
    reset_game()

# --- Input nama player ---
st.session_state.player_name = st.text_input("Masukkan nama kamu:")

# --- Inisialisasi angka rahasia ---
if mode == "Versus Komputer" and not st.session_state.ready_to_play:
    if st.button("Mulai Game 🎲"):
        st.session_state.secret = random.randint(MIN_NUMBER, MAX_NUMBER)
        st.session_state.ready_to_play = True
        st.info("Komputer sudah memilih angka. Ayo tebak!")

elif mode == "Versus Player 2" and not st.session_state.ready_to_play:
    secret_input = st.text_input("Player 2, masukkan angka rahasia:", type="password")
    if st.button("Mulai Game 🎯"):
        if secret_input.isdigit():
            num = int(secret_input)
            if MIN_NUMBER <= num <= MAX_NUMBER:
                st.session_state.secret = num
                st.session_state.ready_to_play = True
                st.success("Angka rahasia disimpan! Player 1, silakan tebak!")
            else:
                st.error(f"Masukkan angka antara {MIN_NUMBER}-{MAX_NUMBER}.")
        else:
            st.error("Input tidak valid. Masukkan angka!")

# --- Gameplay aktif ---
if st.session_state.ready_to_play and st.session_state.attempts > 0 and not st.session_state.guessed_correctly:
    guess = st.number_input(f"Tebak angka ({MIN_NUMBER}-{MAX_NUMBER}):", min_value=MIN_NUMBER, max_value=MAX_NUMBER, step=1)

    if st.button("Submit Tebakan"):
        if guess in st.session_state.history:
            st.warning("⚠️ Kamu sudah nebak angka ini.")
        else:
            st.session_state.history.append(guess)

            if guess == st.session_state.secret:
                st.success("🎉 Congratsss! Kamu berhasil nebak angkanya!")
                st.session_state.guessed_correctly = True
                # Tambah skor ke scoreboard
                scoreboard.append({
                    "nama": st.session_state.player_name or "Anonim",
                    "mode": mode,
                    "sisa_kesempatan": st.session_state.attempts,
                    "total_tebakan": len(st.session_state.history)
                })
                save_scoreboard(scoreboard)
            elif guess > st.session_state.secret:
                st.info("📉 Terlalu besar.")
            else:
                st.info("📈 Terlalu kecil.")

            st.session_state.attempts = max(0, st.session_state.attempts - 1)

    # Tampilin info progress
    st.write(f"🧾 Tebakan sejauh ini: {', '.join(map(str, st.session_state.history))}")
    st.write(f"❤️ Sisa kesempatan: {st.session_state.attempts}")

# --- Game selesai ---
if (st.session_state.guessed_correctly or st.session_state.attempts == 0) and st.session_state.ready_to_play:
    if not st.session_state.guessed_correctly:
        st.error(f"💀 Game Over! Angka rahasianya adalah: {st.session_state.secret}")
    
    if st.button("🔁 Main Lagi"):
        reset_game()
        st.experimental_rerun()

# --- Tampilkan Scoreboard ---
with st.expander("📊 Lihat Scoreboard"):
    if scoreboard:
        for i, entry in enumerate(reversed(scoreboard[-10:]), 1):
            st.markdown(
                f"**{i}. {entry['nama']}** ({entry['mode']}) - "
                f"Sisa Kesempatan: {entry['sisa_kesempatan']}, "
                f"Tebakan: {entry['total_tebakan']}"
            )
    else:
        st.write("Belum ada skor. Yuk main dulu!")
