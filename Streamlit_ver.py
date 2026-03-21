import streamlit as st
import random

st.set_page_config(page_title="Guessing Game", page_icon="🎯")

# --- SESSION VARIABLES ---
if "secret" not in st.session_state:
    st.session_state.secret = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_started" not in st.session_state:
    st.session_state.game_started = False


# --- FUNCTIONS ---
def start_game(start, end):
    st.session_state.secret = random.randint(start, end)
    st.session_state.attempts = 0
    st.session_state.game_started = True


def reset_game():
    st.session_state.secret = None
    st.session_state.attempts = 0
    st.session_state.game_started = False


# --- UI ---
st.title("🎯 Number Guessing Game")
st.write("Try to guess the number chosen by the computer!")

# Difficulty selection before game starts
if not st.session_state.game_started:
    st.subheader("Choose Difficulty")

    difficulty = st.selectbox(
        "Select level:",
        [
            "Easy (1–20)",
            "Medium (1–50)",
            "Hard (1–100)",
            "Custom Range",
        ],
    )

    if difficulty == "Easy (1–20)":
        start, end = 1, 20
    elif difficulty == "Medium (1–50)":
        start, end = 1, 50
    elif difficulty == "Hard (1–100)":
        start, end = 1, 100
    else:
        start = st.number_input("Start number:", step=1, value=1)
        end = st.number_input("End number:", step=1, value=100)

    if st.button("Start Game"):
        if start >= end:
            st.error("Start must be LESS than End!")
        else:
            start_game(start, end)
            st.success("Game Started! Scroll down to play.")

# GAME PANEL
if st.session_state.game_started:
    st.subheader("Make a Guess")

    guess = st.number_input("Enter your guess:", step=1)

    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        if guess < st.session_state.secret:
            st.warning("📉 Too low!")
        elif guess > st.session_state.secret:
            st.warning("📈 Too high!")
        else:
            st.success(f"🎉 Correct! You got it in {st.session_state.attempts} attempts!")
            st.balloons()
            st.button("Play Again", on_click=reset_game)

    st.info(f"Attempts: {st.session_state.attempts}")

    # Hint every 3 attempts
    if st.session_state.attempts > 0 and st.session_state.attempts % 3 == 0:
        hint = "even" if st.session_state.secret % 2 == 0 else "odd"
        st.write(f"💡 Hint: The number is **{hint}**!")

    st.button("Restart Game", on_click=reset_game)