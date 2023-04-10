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
from streamlit_tags import st_tags
from Skills import ds_keyword,web_keyword,android_keyword,ios_keyword,uiux_keyword,n_any
from Recommendations import web_skills,ds_skills,ios_skills,android_skills,uiux_skills,no_skills
from Courses import ds_course,web_course,android_course,ios_course,uiux_course
import nltk
nltk.download('stopwords')


st.set_page_config(
   page_title="Resume Screener",
   page_icon='./imgs/design.jpg',
)

def main():
    img = Image.open('./imgs/design.jpg')
    resized_img = img.resize((300, 300))
    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
    col2.image(resized_img, use_column_width=True)
    
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities, key="level_select")
    return choice

def User():
    st.write('Welcome to user panel')
    st.markdown('''<h5 style='text-align: left; color: #70FA79;'> Upload Your Resume </h5>''',unsafe_allow_html=True)
    
    # course recommendations from Courses.py
    def course_recommender(course_list):
        st.subheader("**Courses & Certificates Recommendations📖**")
        c = 0
        rec_course = []
        no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
        random.shuffle(course_list)
        for c_name, c_link in course_list:
            c += 1
            st.markdown(f"({c}) [{c_name}]({c_link})")
            rec_course.append(c_name)
            if c == no_of_reco:
                break
        return rec_course
    
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
        with st.spinner('Processing your information...'):
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
            print(resume_text)
        
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
            keywords = {
                'INTERNSHIP': 'Intermediate',
                'INTERNSHIPS': 'Intermediate',
                'Internship': 'Intermediate',
                'Internships': 'Intermediate',
                'EXPERIENCE': 'Experienced',
                'WORK EXPERIENCE': 'Experienced',
                'Experience': 'Experienced',
                'Work Experience': 'Experienced',
            }

            cand_level = ''
            for key, value in keywords.items():
                if key in resume_text:
                    cand_level = value
                    break

            if not cand_level:
                cand_level = 'Beginner'

            color = {
                'Intermediate': '#1ed760',
                'Experienced': '#fba171',
                'Fresher': '#d73b5c'
            }

            st.markdown(f'''<h4 style='text-align: left; color: {color[cand_level]};'>You are at {cand_level.lower()} level!</h4>''', unsafe_allow_html=True)
            ### Skill Recommendations Starts
            # st.subheader("**Skills Recommendation**")                
            recommended_skills = []
            reco_field = ''
            rec_course = ''

            ### condition starts to check skills from keywords and predict 
            for i in resume_data['skills']:
            
                #### Data science recommendation
                if i.lower() in ds_keyword:
                    print(i.lower())
                    reco_field = 'Data Science'
                    st.success("** Our analysis says you are looking for Data Science Jobs.**")
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                    text='Recommended skills generated from System',value=ds_skills,key = '2')
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job</h5>''',unsafe_allow_html=True)
                    rec_course = course_recommender(ds_course)
                    break

                #### Web development recommendation
                elif i.lower() in web_keyword:
                    print(i.lower())
                    reco_field = 'Web Development'
                    st.success("**Our analysis says you are looking for Web Development Jobs**")
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                    text='Recommended skills generated from System',value=web_skills,key = '3')
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                    rec_course = course_recommender(web_course)
                    break

                #### Android App Development
                elif i.lower() in android_keyword:
                    print(i.lower())
                    reco_field = 'Android Development'
                    st.success("** Our analysis says you are looking for Android App Development Jobs **")
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                    text='Recommended skills generated from System',value=android_skills,key = '4')
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                    rec_course = course_recommender(android_course)
                    break

                #### IOS App Development
                elif i.lower() in ios_keyword:
                    print(i.lower())
                    reco_field = 'IOS Development'
                    st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                    text='Recommended skills generated from System',value=ios_skills,key = '5')
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                    rec_course = course_recommender(ios_course)
                    break

                #### Ui-UX Recommendation
                elif i.lower() in uiux_keyword:
                    print(i.lower())
                    reco_field = 'UI-UX Development'
                    st.success("**Our analysis says you are looking for UI-UX Development Jobs**")
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                    text='Recommended skills generated from System',value=uiux_skills,key = '6')
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                    rec_course = course_recommender(uiux_course)
                    break

                #### For Not Any Recommendations
                elif i.lower() in n_any:
                    print(i.lower())
                    reco_field = 'NA'
                    st.warning("** Currently our tool only predicts and recommends for Data Science, Web, Android, IOS and UI/UX Development**")
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                    text='Currently No Recommendations',value=no_skills,key = '6')
                    st.markdown('''<h5 style='text-align: left; color: #092851;'>Maybe Available in Future Updates</h5>''',unsafe_allow_html=True)
                    rec_course = "Sorry! Not Available for this Field"
                    break
        
            ## Resume Scorer & Resume Writing Tips
            st.subheader("**Resume Tips & Ideas 📝**")
            resume_score = 0
            
            ### Predicting Whether these key points are added to the resume
            if 'Objective' or 'Summary' in resume_text:
                resume_score = resume_score+6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective/Summary</h4>''',unsafe_allow_html=True)                
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

            if 'Education' or 'School' or 'College'  in resume_text:
                resume_score = resume_score + 12
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)

            if 'EXPERIENCE' in resume_text:
                resume_score = resume_score + 16
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
            elif 'Experience' in resume_text:
                resume_score = resume_score + 16
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

            if 'INTERNSHIPS'  in resume_text:
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
            elif 'INTERNSHIP'  in resume_text:
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
            elif 'Internships'  in resume_text:
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
            elif 'Internship'  in resume_text:
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

            if 'SKILLS'  in resume_text:
                resume_score = resume_score + 7
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
            elif 'SKILL'  in resume_text:
                resume_score = resume_score + 7
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
            elif 'Skills'  in resume_text:
                resume_score = resume_score + 7
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
            elif 'Skill'  in resume_text:
                resume_score = resume_score + 7
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)

            if 'HOBBIES' in resume_text:
                resume_score = resume_score + 4
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
            elif 'Hobbies' in resume_text:
                resume_score = resume_score + 4
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

            if 'INTERESTS'in resume_text:
                resume_score = resume_score + 5
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h4>''',unsafe_allow_html=True)
            elif 'Interests'in resume_text:
                resume_score = resume_score + 5
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Interest. It will show your interest other that job.</h4>''',unsafe_allow_html=True)

            if 'ACHIEVEMENTS' in resume_text:
                resume_score = resume_score + 13
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
            elif 'Achievements' in resume_text:
                resume_score = resume_score + 13
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

            if 'CERTIFICATIONS' in resume_text:
                resume_score = resume_score + 12
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
            elif 'Certifications' in resume_text:
                resume_score = resume_score + 12
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
            elif 'Certification' in resume_text:
                resume_score = resume_score + 12
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

            if 'PROJECTS' in resume_text:
                resume_score = resume_score + 19
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
            elif 'PROJECT' in resume_text:
                resume_score = resume_score + 19
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
            elif 'Projects' in resume_text:
                resume_score = resume_score + 19
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
            elif 'Project' in resume_text:
                resume_score = resume_score + 19
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFFFFF;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

            st.subheader("**Resume Score 📝**")
            
            st.markdown(
                """
                <style>
                    .stProgress > div > div > div > div {
                        background-color: #d73b5c;
                    }
                </style>""",
                unsafe_allow_html=True,
            )

            ### Score Bar
            my_bar = st.progress(0)
            score = 0
            for percent_complete in range(resume_score):
                score +=1
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1)

            ### Score
            st.success('** Your Resume Writing Score: ' + str(score)+'**')
            st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")


   
def Admin():
    st.write('Welcome to admin panel')

if main() == "User":
    User()
else:
    Admin()

  

