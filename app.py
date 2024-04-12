from dotenv import load_dotenv

load_dotenv()  # load all the environment variables from .env
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load Gemini pro vision
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response_Model = model.generate_content([input, image[0], prompt])
    return response_Model.parts


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



# initialize our streamlit app

st.set_page_config(page_title="Invoice Extractor")
st.header("Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Get Data")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices and
               you will have to answer questions based on the input image
               """

# if submit button is clicked
if submit:
    combine_string = ""
    image_data = input_image_setup(uploaded_file)
    responses = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    for response in responses:
        combine_string += response.text
    st.write(combine_string)

