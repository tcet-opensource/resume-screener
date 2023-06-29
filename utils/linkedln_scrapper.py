from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
url = "https://linkedin-profiles-and-company-data.p.rapidapi.com/profile-details"

API_KEYS = [
    os.getenv('API_KEY_1'),
    os.getenv('API_KEY_2'),
    os.getenv('API_KEY_3')
]  # Replace with your actual API keys
API_KEY_INDEX = 0  # Current API key index



def rotate_api_key():
    global API_KEY_INDEX
    API_KEY_INDEX = (API_KEY_INDEX + 1) % len(API_KEYS)

def Scrapper(linkedinid):
    api_key_collection = API_KEYS[API_KEY_INDEX]

    payload = {
        "profile_id": linkedinid,
        "profile_type": "personal",
        "contact_info": False,
        "recommendations": False,
        "related_profiles": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key_collection,
        "X-RapidAPI-Host": "linkedin-profiles-and-company-data.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if API limit is reached
    if response.status_code == 429:
        rotate_api_key()
        return Scrapper(linkedinid)  # Retry the request with the new API key
    else:

        data = response.json()
        skills = data.get("skills", [])
        # projects = data.get("projects", [])
        # experience = data.get("experience", [])
        return skills
        # print(skills)
        #
        # extracted_data = {
        #     'skills': skills,
        #     # 'projects': projects,
        #     # 'experience': experience
        # }
        #
        # # Convert the extracted data to JSON
        # extracted_data_json = json.dumps(extracted_data, indent=4)
        #
        # return extracted_data_json
