import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from utils.llm_client import GroqClient
from utils.mcp_helper import build_mcp_prompt


# ✅ NEW: Split into individual questions
def parse_questions(text: str):
    lines = text.split("\n")
    questions = []
    current = []

    for line in lines:
        line = line.strip()

        if line.startswith("Q"):
            if current:
                questions.append(current)
                current = []
        
        current.append(line)

    if current:
        questions.append(current)

    return questions


def main():
    st.set_page_config(
        page_title="MCP Generator / AI Tutor",
        page_icon="📝",
        layout="centered"
    )

    st.title("📝 AI MCP Generator & Tutor")
    st.write("Generate **15 MCP Questions** based on a topic and difficulty level.")

    topic = st.text_input(
        "Enter Topic:",
        placeholder="e.g. Python Lists, ML Algorithms, Docker, Git, MLOps etc."
    )

    level = st.selectbox(
        "Select Difficulty Level:",
        options=["Easy", "Medium", "Hard"],
        index=0
    )

    # ✅ SESSION STATE
    if "full_response" not in st.session_state:
        st.session_state.full_response = None

    if st.button("Generate Questions"):
        if not topic.strip():
            st.warning("Please enter a topic")
            return
        
        with st.spinner("Generating MCQs..."):
            try:
                prompt = build_mcp_prompt(topic, level)
                client = GroqClient()
                response = client.ask(prompt)

                st.session_state.full_response = response

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # ✅ SHOW QUESTIONS WITH TOGGLE
    if st.session_state.full_response:
        st.markdown("---")
        st.subheader("📘 Questions")

        questions = parse_questions(st.session_state.full_response)

        for i, q_lines in enumerate(questions):
            question_part = []
            answer_part = []

            is_answer = False

            for line in q_lines:
                if line.startswith("Answer"):
                    is_answer = True

                if is_answer:
                    answer_part.append(line)
                else:
                    question_part.append(line)

            # ✅ Show Question
            if question_part:
                st.markdown(f"### {question_part[0]}")

                for line in question_part[1:]:
                    st.text(line)

            # ✅ Toggle per question
            if st.checkbox(f"Show Answer {i+1}", key=f"ans_{i}"):
                for line in answer_part:
                    st.text(line)

            st.markdown("---")


if __name__ == "__main__":
    main()