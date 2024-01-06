## Q&A chatbot
from dotenv import load_dotenv
import streamlit as st
import os
from langchain.llms import OpenAI


load_dotenv()


def get_openai_response(question):
    llm = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.6,
        model_name="text-davinci-003",
    )
    response = llm(question)
    return response


st.set_page_config(page_title="Q&A demo")

st.header("LLM application")
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_openai_response(input)
    st.subheader("The response is")
    st.write(response)
