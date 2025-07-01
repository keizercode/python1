import streamlit as st
import random
import string

st.title("🎮 Game Tebak Huruf - Versus Komputer")

if "secret" not in st.session_state:
    st.session_state.secret = random.choice(string.ascii_uppercase)
    st.session_state.attempts = 3
    st.session_state.history = []

guess = st.text_input("Tebak huruf (A-Z):").upper()

if guess:
    if guess not in string.ascii_uppercase or len(guess) != 1:
        st.error("❌ Input tidak valid!")
    elif st.session_state.attempts > 0:
        st.session_state.history.append(guess)
        if guess == st.session_state.secret:
            st.success("🎉 Congratsss! Kamu berhasil menebak hurufnya!")
        elif guess > st.session_state.secret:
            st.info("📈 Huruf terlalu besar.")
        else:
            st.info("📉 Huruf terlalu kecil.")

        st.session_state.attempts -= 1

        st.write(f"Tebakan: {', '.join(st.session_state.history)}")
        st.write(f"Sisa kesempatan: {st.session_state.attempts}")

    if st.session_state.attempts == 0 and guess != st.session_state.secret:
        st.error(f"💀 Game Over! Hurufnya adalah: {st.session_state.secret}")
