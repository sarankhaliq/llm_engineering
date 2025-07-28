import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
    
MODEL = 'gpt-4o-mini'
openai = OpenAI()

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    This class is used to call a website and extract its data
    """
    def __init__(self, url):
        self.url=url
        response=requests.get(url, headers=headers)
        self.body=response.content
        soup=BeautifulSoup(self.body, 'html.parser')

        if soup.title:
            self.title = soup.title.string
        else:
            print("No title found") 
        
        if soup.body:
            for bad_tags in soup.body(["script", "style", "img", "input"]):
                bad_tags.decompose()
            self.text=soup.body.get_text(separator="\n", strip=True)
        else:
            self.text=""

        links=[]
        
        for a_tags in soup.find_all('a'):
            href=a_tags.get('href')
            if href:
                links.append(href)
            else:
                print("No links found")
        self.links=links
                




web=Website("https://scholar.google.com/citations?user=fApwIBsAAAAJ&hl=en&oi=ao")
print(web.links)

json_format_text="""
{
"links": [
{"type": "about page", "url": "https://full.url/goes/here/about"}, "type": "career page", "url": "https://anoyher.full.url/goes/here/about"}
]
}
"""

print(json_format_text)