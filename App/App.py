import streamlit as st
import pandas as pd
import base64, random
import time,datetime
import os
from pyresparser import ResumeParser
from PIL import Image
import nltk
nltk.download('stopwords')


st.set_page_config(
   page_title="Resume Screener",
   page_icon='./imgs/design.jpg',
)

def main():
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities, key="level_select")
    return choice

def User():
    st.write('Welcome to user panel')
    st.markdown('''<h5 style='text-align: left; color: #70FA79;'> Upload Your Resume </h5>''',unsafe_allow_html=True)
    
    # show uploaded file path to view pdf_display
    def show_pdf(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
    ## file upload in pdf format
    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    if pdf_file is not None:
        with st.spinner('Hang On While We Cook Magic For You...'):
            time.sleep(4)
    
    ### saving the uploaded resume to folder
        save_image_path = './Uploaded_Resumes/'+pdf_file.name
        pdf_name = pdf_file.name
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        show_pdf(save_image_path)

   
def Admin():
    st.write('Welcome to admin panel')

if main() == "User":
    User()
else:
    Admin()

  

