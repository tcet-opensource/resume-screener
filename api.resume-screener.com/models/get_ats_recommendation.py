from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

# gives recommendations based on the ats format
def ats_recommendations(json_data):
    recommendations = []
    skills = json_data['filename']['skills']
    experience = json_data['filename']['total_experience']
    degree = json_data['filename']['degree']
    designation = json_data['filename']['designation']
    company_names = json_data['filename']['company_names']

    if experience < 1:
        recommendations.append("Consider adding some internships or freelance work to gain experience. (Context : Experience)")        
    if len(skills) < 5:
        recommendations.append("Consider adding more skills to showcase your abilities.(Context : Skills)")
    if not degree:
        recommendations.append("Consider adding your educational qualifications to the resume.(Context : Degree)")
    if not designation:
        recommendations.append("Add a clear job title to your resume to showcase your current role.(Context : Designation)")
    if not company_names:
        recommendations.append("Add your current or previous employers to your resume.(Context : Company names)")

    if not recommendations:
        recommendations.append("Your resume looks great! Good luck with your job search.")

    return recommendations

if __name__ == '__main__':
    app.run(debug=True)
