from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()

        image_parts = [{"mime_type": upload_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multilanguage invoice extractor")

st.header("Multilanguage invoice extractor")

input = st.text_input("Input prompt: ", key="input")

upload_file = st.file_uploader(
    "Choose an image of the invoice", type=["jpg", "jpeg", "png"]
)

image = ""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded image...", use_column_width=True)

submit = st.button("Tell me about the invoice")
input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice and
you will have to answer any questions based on the uploaded invoice image
"""
if submit:
    image_data = input_image_details(upload_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is")
    st.write(response)
