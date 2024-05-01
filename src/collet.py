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
    for em in ems:
        key, value = em.text.split(":")
        key = key.strip(" ")
        info[key] = value.strip(" ")
    
    return info

def get_basic_infos(soup) -> dict:    
    # Find the div element containing the main content
    div_content = soup.find('div', class_='td-page-content')
    paragraph = div_content.find_all('p')[1]
    ems = paragraph.find_all('em')

    # Function to transform <em> HTML tags into a Python dict
    data = transform_info(ems)

    return data 

url = 'https://www.residentevildatabase.com/personagens/ada-wong/'

response = get_content(url)

status:int = response.status_code

if status != 200:
    print(f"something went wrong: code {status}")

# Initialize BeautifulSoup with the HTML response text
soup = BeautifulSoup(response.text, features="lxml")

get_basic_infos(soup)
