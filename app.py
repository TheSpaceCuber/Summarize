import streamlit as st
import openai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
load_dotenv()

st.title("PDF Summarizer")
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that allows you to interact with 
       the OpenAI API's **text-davinci-003** model.
       Simply upload a pdf file and the model will summarize it in point form.
       '''
)

# Set the model engine and your OpenAI API key
model_engine = "text-davinci-003"
# follow step 4 to get a secret_key
openai.api_key = os.environ["OPENAI_API_KEY"]

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
text = ""
if uploaded_file is not None:
    # creating a pdf reader object
    reader = PdfReader(uploaded_file)
    
    # printing number of pages in pdf file
    print(len(reader.pages))
    
    
    # extracting text from page
    for page in reader.pages:
        text += page.extract_text() + "\n"

st.subheader("Summary:")
def main(text):
    '''
    This function gets the user input, pass it to ChatGPT function and 
    displays the response
    '''
    if text != "":
        text = "Here is the content of a pdf file. Can you summarize it in point form?\n" + text
    response = process(text)
    return st.write(f"{response}")


def process(user_query):
    ''' 
    This function uses the OpenAI API to generate a response to the given 
    user_query using the ChatGPT model
    '''
    # Use the OpenAI API to generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=user_query,
        max_tokens=1024,
        n=1,
        temperature=0.2,
    )
    print(completion.choices)
    response = completion.choices[0].text
    return response

main(text)
