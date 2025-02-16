import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Api key not found")
elif not api_key.startswith("sk-proj-"):
    print("API key found, but it didnt start as expected")
elif api_key.strip() !=api_key:
    print("API key is found but it may contain some unwanted spaces or tabs please re-check")
else:
    print("Api key found")

openai=OpenAI()


# Some websites need you to use proper headers when fetching them:
# FEW WEBSsiteshave security system taht doesnt allow any bot to access their data
# using a header, make it appear that the request is generated via actual browser not this code
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class website:
    def __init__(self, url):
        self.url = url 
        response = requests.get(self.url, headers=headers) # using request comand we access website and get a response and it has web content
        soup=BeautifulSoup(response.content, 'html.parser')
        self.title=soup.title.string if soup.title else "No title found"
        for extras in soup.body(["img", "style","script", "input"]):
            extras.decompose()
        self.text=soup.body.get_text(separator="\n", strip=True)

    def system_prompt(self, system_prompt):
        self.system_prompt=system_prompt
    
    def user_prompt(self, user_prompt):
        self.user_prompt=user_prompt
    
    def set_messages_for_openai(self):
        self.messages=[
            {"role" : "system", "content": self.system_prompt},
            {"role" : "user", "content": self.user_prompt}
        ]
    def requiest_openai(self, model):
        self.model=model
        self.response=openai.chat.completions.create(model=self.model, messages=self.messages)
    
    def summarize_web(self):
        self.summary=self.response.choices[0].message.content
        print(self.summary)

web=website("https://learnobots.com/")
web.system_prompt("You are an AI Agent that parse the website, collect text and provide summarize results. You also ignore the text which are navigaion for")
web.user_prompt(f"You are looking at a website titled {web.title}"+" The contents of this website is as follows\n" +web.text+"\n please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too")
web.set_messages_for_openai()
web.requiest_openai("gpt-4o-mini")
web.summarize_web()
