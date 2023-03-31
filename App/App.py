import streamlit as st
import pandas as pd
import base64, random
import time,datetime
import os
from pyresparser import ResumeParser
from PIL import Image
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
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
    
    # Reads Pdf file and checks extraction
    def pdf_reader(file):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                        caching=True,
                                        check_extractable=True):
                page_interpreter.process_page(page)
                print(page)
            text = fake_file_handle.getvalue()

        ## close open handles
        converter.close()
        fake_file_handle.close()
        return text
    
    # show uploaded pdf to user
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
    
    ### saving the uploaded resume to local folder
        save_image_path = './Uploaded_Resumes/'+pdf_file.name
        pdf_name = pdf_file.name
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        show_pdf(save_image_path)
    ### parsing & extract whole resume using ResumeParser
        resume_data = ResumeParser(save_image_path).get_extracted_data()
        if resume_data:
            
            
            resume_text = pdf_reader(save_image_path)

        
            st.header("**Resume Analysis 📄**")
            # st.write("Hello "+ resume_data['name'])
            st.subheader("**Your Basic info 👀**")
            try:
                st.text('Name: '+resume_data['name'])
                st.text('Email: ' + resume_data['email'])
                st.text('Contact: ' + resume_data['mobile_number'])
                st.text('Degree: '+str(resume_data['degree']))                    
                st.text('Resume pages: '+str(resume_data['no_of_pages']))

            except:
                pass

   
def Admin():
    st.write('Welcome to admin panel')

if main() == "User":
    User()
else:
    Admin()

  

