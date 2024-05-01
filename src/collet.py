import requests
import json
from bs4 import BeautifulSoup

def get_headers(file_path) -> any:
    with open(file_path, 'r') as file:
        headers = json.load(file)
    
    return headers

def get_content(url, headers_json='../json/headers.json') -> requests.Response:
    headers = get_headers(headers_json)
    response = requests.get(url, headers=headers)

    return response

def transform_info(ems) -> dict:
    info = {}
    # Iterate over each emphasized text
    for em in ems:
        key, value, *_ = em.text.split(":")
        key = key.strip(" ")
        info[key] = value.strip(" ")
    
    return info

def get_basic_infos(content) -> dict:   
    paragraph = content.find_all('p')[1]
    ems = paragraph.find_all('em')
    # Function to transform <em> HTML tags into a Python dict
    data = transform_info(ems)
    return data 

def get_apparitions(content) -> list:
        
    li_elements = content.find('h4').find_next().find_all('li')

    apparitions:list = [li.text for li in li_elements]
    return apparitions

def get_characters_infos(url) -> dict:
    response = get_content(url)
    status = response.status_code

    if status != 200:
        print(f"Something went wrong: code {status}")
        return {}  # Return empty dictionary if there's an error
    else:
        soup = BeautifulSoup(response.text, features="lxml")
        content = soup.find("div", class_='td-page-content')
        data = get_basic_infos(content)
        data['Apparitions'] = get_apparitions(content)
        return data


def get_links() -> list: 
    url = 'https://www.residentevildatabase.com/personagens/'
    response = get_content(url)
    characters_text = BeautifulSoup(response.text, features="lxml")
    links_html = characters_text.find("div", class_='td-page-content').find_all('a')
    links:list = [link['href'] for link in links_html]  
    
    return links

links_characters:list = get_links()
data_characters = []

for link in links_characters:
    print(link)
    character = get_characters_infos(link)
    if character != None:  # Check if the character dictionary is not empty
        character['Link'] = link  # Assign the link to the character dictionary
        data_characters.append(character)
    else:
        print(f"Failed to retrieve data for {link}. Skipping...")
