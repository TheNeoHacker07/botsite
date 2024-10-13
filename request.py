import requests
import json


def get_json(url):
    request_json = requests.get(url)
    try:
        data = request_json.json()
        return data
    except Exception as error:
        print(error)

# article = get_json(article_url)

# print(article)

def format_data(articles):
    formatted_data = ''
    
    if not articles:
        return 'none'
    
    for article in articles:
        formatted_data += f"{article['title']}------{article['text']}"

    return formatted_data

# print(format_data(article))
'-----------------------------------------get mine articles-------------------------------------'


def get_profile(username):
    request_json = requests.get(f'http://127.0.0.1:5000/{username}/')
    try:
        user_data = request_json.json()
        return user_data
    
    except Exception as error:
        print(error)


    


