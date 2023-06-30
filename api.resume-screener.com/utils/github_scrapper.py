import requests

def fetch_user_details(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_details = response.json()
        return user_details
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_repo_details(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repo_details = response.json()
        return repo_details
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_user_corpus(username):
    user_details = fetch_user_details(username)
    if user_details:
        repo_details = fetch_repo_details(username)
        final_data = []
        
        if repo_details:
            for repo in repo_details:
                repo_name = repo.get('name')
                language = repo.get("language")
                repo_description = repo.get('description')
                if repo_name:
                    final_data.append(repo_name)
                if language:
                    final_data.append(language)
                if repo_description:
                    final_data.append(repo_description)
        return [' '.join(final_data)]
    return None

if __name__ == "__main__":
    username = input("Enter github username")
    result = fetch_user_corpus(username)
    print(result)