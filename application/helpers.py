# Helper functions

import requests
import json
import os

from config import TEXT_PATH


def is_active(current_path:str, nav_path:str) -> str:
    """Returns a string that shows which page is active in the navigation menu."""

    if current_path == nav_path:
        return "is-active"
    
    return ""


def read_description(file_path:str) -> list:
    """Returns the content of a text file as a list of strings where each string is a paragraph."""

    content = []

    try:
        with open(file_path) as file:
            current_paragraph = ""

            # Loop over each line
            for line in file:
                # Check if the line is blank (i.e. contains only white spaces)
                if line.strip() == "":
                    # If so, add the current paragraph to the list and reset current paragraph
                    content.append(current_paragraph)
                    current_paragraph = ""
                # If line is not blank, add it to the current paragraph
                else:
                    current_paragraph += line

            # Add the final paragraph to the list
            if current_paragraph != "":
                content.append(current_paragraph)
    except FileNotFoundError:
        print(f"ERROR! File could not be found for path: {file_path}.")
    except Exception as error:
        print(f"ERROR! {error}.")

    return content


def get_skills(file_path:str) -> tuple:
    """Returns three lists one for each type of cards in the JSON file."""

    try:
        with open(file_path) as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"ERROR! File could not be found for path: {file_path}.")
    except json.JSONDecodeError as error:
        print(f"ERROR! {error}.")
    except Exception as error:
        print(f"ERROR! {error}.")

    # 1. 對應 skills[0]: 開發與作業環境 (type: "language")
    development = [card for card in data["cards"] if card["type"] == "language"]
    # 2. 對應 skills[1]: AI 與智慧交通 (type: "technology")
    ai_its = [card for card in data["cards"] if card["type"] == "technology"]
    # 3. 對應 skills[2]: 資訊安全 (type: "security")
    security = [card for card in data["cards"] if card["type"] == "security"]
    # 回傳這三個陣列 (在路由中通常會被打包成 skills_data = get_skills("path_to_json"))
    return development, ai_its, security


def get_repositories() -> list:
    """Returns a list of dictionaries which contains information about each public repository on my GitHub profile."""

    github_token = os.environ["GITHUB_ACCESS"]

    url = "https://api.github.com/users/unicorn526/repos"
    params = {"per_page": 1000}
    headers = {"Authorization": f"token {github_token}"}

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)

            repo_list = []

            # Iterate through each repository and add the information needed to the list
            for repo in data:
                # Retrieve information only for non-forked repositories
                if not repo["fork"]:
                    # Check for the README repository so it won't be included
                    if "unicorn526" not in repo["name"]:
                        repo_info = {}
                        repo_info["name"] = repo["name"]
                        repo_info["description"] = repo["description"]
                        repo_info["url"] = repo["html_url"]

                        # Get all languages used in the repository
                        languages = repo["languages_url"]
                        languages_response = requests.get(languages)
                        languages_data = languages_response.json()
                        sorted_languages = sorted(languages_data.items(), key=lambda x: x[1], reverse=True)

                        # Get top three most used languages in repository
                        top_languages = [lang[0] for lang in sorted_languages[:3]]
                        repo_info["languages"] = top_languages

                        # Add the repository dictionary to the list of repositories
                        repo_list.append(repo_info)

            return repo_list
        else:
            print(f"ERROR! {response.status_code} - {response.reason}.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects.")
    except requests.exceptions.RequestException as error:
        print(f"ERROR! {error}.")


def get_language_image(language:str) -> str:
    """Returns the image of a programming language from 'skills.json'."""

    try:
        with open(f"{TEXT_PATH}/skills.json") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        print(f"ERROR! {error}.")
    else:
        for card in data.get("cards", []):
            if card.get("type") == "language" and card.get("title", "").lower() == language.lower():
                return card.get("image")
