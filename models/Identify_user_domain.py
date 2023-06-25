from flask import Flask, request, jsonify
import PyPDF2
import re

app = Flask(__name__)

@app.route('/suggest-professions', methods=['POST'])
def suggest_professions():
    file = request.files['resume']
    content = file.read()
    keywords_found = content_ats(content)
    skills = keywords_found
    suggested_professions = suggest_professions(skills)
    return jsonify({'suggested_professions': suggested_professions})


def content_ats(content):
    reader = PyPDF2.PdfReader(content)
    num_pages = len(reader.pages)

    found_keywords = []
    for page_number in range(num_pages):
        page = reader.pages[page_number]
        text = page.extract_text()

        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text, re.IGNORECASE):
                found_keywords.append(keyword)

    return found_keywords


def suggest_professions(skills):
    professions = {
        "Software Developer": ["python", "java", "javascript", "c++", "web development"],
        "Data Scientist": ["data science", "machine learning", "data analysis", "python"],
        "DevOps Engineer": ["devops", "cloud computing", "docker", "kubernetes"],
        "Project Manager": ["project management", "agile", "scrum"],
        "Digital Marketer": ["digital marketing", "seo", "social media", "content marketing"],
        "Financial Analyst": ["finance", "accounting", "financial analysis"],
        "Human Resources Specialist": ["human resources", "recruitment", "employee relations"],
        "Customer Support Representative": ["customer service", "communication", "problem solving"],
        "Graphic Designer": ["graphic design", "ui/ux design", "illustration"],
        "Network Engineer": ["networking", "routers", "switches", "firewalls"],
        "Sales Representative": ["sales", "negotiation", "relationship management"],
        "UI/UX Designer": ["ui/ux design", "user research", "wireframing", "prototyping"],
        "Content Writer": ["content writing", "copywriting", "editing", "proofreading"],
        "Quality Assurance Analyst": ["quality assurance", "testing", "defect tracking"],
        "Business Analyst": ["business analysis", "requirements gathering", "process modeling"],
        "Product Manager": ["product management", "product strategy", "market research"],
        "Cybersecurity Analyst": ["cybersecurity", "network security", "vulnerability assessment"],
        "Systems Administrator": ["system administration", "server management", "troubleshooting"],
        "Video Editor": ["video editing", "motion graphics", "color correction"],
        "Artificial Intelligence Engineer": ["artificial intelligence", "neural networks", "deep learning"],
        "Technical Writer": ["technical writing", "documentation", "API documentation"],
        "Event Planner": ["event planning", "vendor management", "budgeting"],
        "UI Developer": ["ui design", "html", "css", "javascript"],
        "Data Engineer": ["data engineering", "ETL", "SQL", "big data"],
        "Market Research Analyst": ["market research", "data analysis", "statistics"],
        "Supply Chain Manager": ["supply chain", "logistics", "inventory management"],
        "UX Researcher": ["user research", "usability testing", "persona creation"],
        "Mobile App Developer": ["mobile app development", "iOS", "Android", "React Native"],
        "UX/UI Architect": ["ux design", "ui design", "information architecture"],
        "Systems Analyst": ["systems analysis", "requirements analysis", "solution design"],
        "Business Intelligence Analyst": ["business intelligence", "data visualization", "SQL"],
        "Social Media Manager": ["social media management", "content creation", "analytics"],

    }

    match_professions = []
    max_match_skills = 0

    for profession, required_skills in professions.items():
        match_skills = set(skills) & set(required_skills)
        num_match_skills = len(match_skills)

        if num_match_skills > max_match_skills:
            match_professions = [profession]
            max_match_skills = num_match_skills
        elif num_match_skills == max_match_skills:
            match_professions.append(profession)

    return match_professions


if __name__ == '__main__':
    app.run()
