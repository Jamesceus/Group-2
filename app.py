import streamlit as st
import setup as chat

###################################
# UI Code
st.title('Lecture Navigator')

question = st.text_input("Type in your question related to Data Science and Machine Learning lessons:")

if (len(question) != 0):
    st.write("You asked: " + question)
    container = st.container(border=True)
    container.write("Answers:")
    container.write(chat.ask(question))