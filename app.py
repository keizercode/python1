import streamlit as st
import random
import string

st.title("🎮 Game Tebak Huruf")

# --- Pilih Mode Permainan ---
mode = st.selectbox("Pilih Mode Permainan:", ["Versus Komputer", "Versus Player 2"])

# --- Inisialisasi State ---
if "secret" not in st.session_state:
    st.session_state.secret = ""
    st.session_state.attempts = 3
    st.session_state.history = []
    st.session_state.game_started = False

# --- Mode VS Komputer ---
if mode == "Versus Komputer" and not st.session_state.game_started:
    st.session_state.secret = random.choice(string.ascii_uppercase)
    st.session_state.attempts = 3
    st.session_state.history = []
    st.session_state.game_started = True
    st.info("Komputer telah memilih huruf rahasia. Tebak sekarang!")

# --- Mode VS Player 2 ---
if mode == "Versus Player 2" and not st.session_state.game_started:
    secret_input = st.text_input("Player 2, masukkan huruf rahasia (A-Z):", type="password")
    if secret_input:
        if len(secret_input) == 1 and secret_input.upper() in string.ascii_uppercase:
            st.session_state.secret = secret_input.upper()
            st.session_state.attempts = 3
            st.session_state.history = []
            st.session_state.game_started = True
            st.success("Huruf rahasia berhasil disimpan. Player 1, giliranmu menebak!")
        else:
            st.error("❌ Input harus satu huruf dari A sampai Z.")

# --- Game Dimulai ---
if st.session_state.game_started and st.session_state.attempts > 0:
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
                st.session_state.attempts = 0
            elif guess > st.session_state.secret:
                st.info("📈 Huruf terlalu besar.")
            else:
                st.info("📉 Huruf terlalu kecil.")
            st.session_state.attempts -= 1

    st.write(f"📝 Riwayat Tebakan: {', '.join(st.session_state.history)}")
    st.write(f"❤️ Sisa Kesempatan: {st.session_state.attempts}")

# --- Game Over ---
if st.session_state.attempts == 0 and st.session_state.secret != "":
    if st.session_state.history[-1] != st.session_state.secret:
        st.error(f"💀 Game Over! Huruf rahasianya adalah: {st.session_state.secret}")

    # Tombol Main Lagi
    if st.button("🔁 Main Lagi"):
        st.session_state.secret = ""
        st.session_state.attempts = 3
        st.session_state.history = []
        st.session_state.game_started = False
        st.experimental_rerun()
