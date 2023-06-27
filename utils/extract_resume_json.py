from flask import Flask, request, jsonify
import PyPDF2
import json

app = Flask(__name__)

@app.route('/extract-resume-content', methods=['GET'])
def extract_resume_content():
    file = "utils\example.pdf"
    content = file.read()
    resume_content = extract_resume_content(content)
    return jsonify(resume_content)


def extract_resume_content(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    resume_content = {
        'EDUCATION': [],
        'COURSEWORK / SKILLS': [],
        'PROJECTS': [],
        'INTERNSHIP': [],
        'TECHNICAL SKILLS': [],
        'CO/EXTRA-CURRICULAR ACTIVITIES': [],
        'CERTIFICATIONS': []
    }

    extract_education = True
    extract_coursework = True
    extract_projects = True
    extract_internship = True
    extract_technical_skills = True

    for page in pdf_reader.pages:
        page_content = page.extract_text().split('\n')
        page_content = [line.strip() for line in page_content if line.strip() != '']

        if extract_education and 'EDUCATION' in page_content:
            education_index = page_content.index('EDUCATION')
            education = page_content[education_index + 1:]
            if 'COURSEWORK / SKILLS' in education:
                coursework_index = education.index('COURSEWORK / SKILLS')
                education = education[:coursework_index]
            resume_content['EDUCATION'] = education
            extract_education = False

        if extract_coursework and 'COURSEWORK / SKILLS' in page_content:
            coursework_index = page_content.index('COURSEWORK / SKILLS')
            coursework = page_content[coursework_index + 1:]

            if 'PROJECTS' in coursework:
                projects_index = coursework.index('PROJECTS')
                coursework = coursework[:coursework_index]

            resume_content['COURSEWORK / SKILLS'] = coursework

            extract_coursework = False


        if extract_projects and 'PROJECTS' in page_content:
            projects_index = page_content.index('PROJECTS')
            projects = page_content[projects_index + 1:]


            if 'INTERNSHIP' in projects:
                internship_index = projects.index('INTERNSHIP')
                projects = projects[:projects_index]

            resume_content['PROJECTS'] = projects
            extract_projects = False


        if extract_internship and 'INTERNSHIP' in page_content:
            internship_index = page_content.index('INTERNSHIP')
            internship = page_content[internship_index + 1:]

            if 'TECHNICAL SKILLS' in internship:
                skills_index = internship.index('TECHNICAL SKILLS')
                internship = internship[:internship_index]


            resume_content['INTERNSHIP'] = internship
            extract_internship = False


        if extract_technical_skills and 'TECHNICAL SKILLS' in page_content:
            skills_index = page_content.index('TECHNICAL SKILLS')
            skills = page_content[skills_index + 1:]


            if 'CO/EXTRA-CURRICULAR ACTIVITIES' in skills:
                skills_index = skills.index('CO/EXTRA-CURRICULAR ACTIVITIES')
                skills = skills[:skills_index]


            resume_content['TECHNICAL SKILLS'] = skills
            extract_technical_skills = False

        if 'CO/EXTRA-CURRICULAR ACTIVITIES' in page_content:
            activities_index = page_content.index('CO/EXTRA-CURRICULAR ACTIVITIES')
            activities = page_content[activities_index + 1:]

            if 'CERTIFICATIONS' in activities:
                activities_index = activities.index('CERTIFICATIONS')
                activities = activities[:activities_index]

            resume_content['CO/EXTRA-CURRICULAR ACTIVITIES'] = activities


        if 'CERTIFICATIONS' in page_content:
            certifications_index = page_content.index('CERTIFICATIONS')
            certifications = page_content[certifications_index + 1:]

            resume_content['CERTIFICATIONS'] = certifications
    pdf_file.close()

    return resume_content

if __name__ == '__main__':
    app.run()
