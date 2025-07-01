import streamlit as st
import random
import string

st.title("🎮 Game Tebak Huruf")

# --- Pilih Mode ---
mode = st.selectbox("Pilih Mode Permainan:", ["Versus Komputer", "Versus Player 2"])

# --- Inisialisasi State ---
if "secret" not in st.session_state:
    st.session_state.secret = ""
    st.session_state.attempts = 3
    st.session_state.history = []
    st.session_state.game_started = False
    st.session_state.guessed_correctly = False
    st.session_state.ready_to_play = False

# --- Reset Game Function ---
def reset_game():
    st.session_state.secret = ""
    st.session_state.attempts = 3
    st.session_state.history = []
    st.session_state.game_started = False
    st.session_state.guessed_correctly = False
    st.session_state.ready_to_play = False

# --- Mode VS Komputer ---
if mode == "Versus Komputer" and not st.session_state.game_started:
    st.session_state.secret = random.choice(string.ascii_uppercase)
    st.session_state.game_started = True
    st.session_state.ready_to_play = True
    st.info("Komputer telah memilih huruf rahasia. Tebak sekarang!")

# --- Mode VS Player 2 ---
if mode == "Versus Player 2" and not st.session_state.game_started:
    secret_input = st.text_input("Player 2, masukkan huruf rahasia (A-Z):", type="password")
    if secret_input:
        if len(secret_input) == 1 and secret_input.upper() in string.ascii_uppercase:
            st.session_state.secret = secret_input.upper()
            st.session_state.game_started = True
            st.session_state.ready_to_play = True
            st.success("Huruf rahasia berhasil disimpan. Player 1, giliranmu menebak!")
        else:
            st.error("❌ Input harus satu huruf dari A sampai Z.")

# --- Game Berjalan ---
if st.session_state.ready_to_play and st.session_state.attempts > 0 and not st.session_state.guessed_correctly:
    guess = st.text_input("Tebak huruf (A-Z):").upper()

    if guess:
        if guess not in string.ascii_uppercase or len(guess) != 1:
            st.error("❌ Input tidak valid!")
        elif guess in st.session_state.history:
            st.warning("⚠️ Kamu sudah menebak huruf ini sebelumnya.")
        else:
            st.session_state.history.append(guess)

            if guess == st.session_state.secret:
                st.success("🎉 Congratsss! Kamu berhasil menebak hurufnya!")
                st.session_state.guessed_correctly = True
            elif guess > st.session_state.secret:
                st.info("📈 Huruf terlalu besar.")
            else:
                st.info("📉 Huruf terlalu kecil.")

            st.session_state.attempts = max(0, st.session_state.attempts - 1)

    st.write(f"📝 Riwayat Tebakan: {', '.join(st.session_state.history)}")
    st.write(f"❤️ Sisa Kesempatan: {st.session_state.attempts}")

# --- Game Berakhir ---
if st.session_state.attempts == 0 and not st.session_state.guessed_correctly:
    st.error(f"💀 Game Over! Huruf rahasianya adalah: {st.session_state.secret}")

# --- Tombol Main Lagi muncul kalau game selesai ---
if (st.session_state.attempts == 0 or st.session_state.guessed_correctly) and st.session_state.game_started:
    if st.button("🔁 Main Lagi"):
        reset_game()
        st.experimental_rerun()
