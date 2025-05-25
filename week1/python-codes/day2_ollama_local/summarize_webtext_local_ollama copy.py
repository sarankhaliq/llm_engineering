import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from bs4 import BeautifulSoup

# Constants

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}



class website:
    def __init__(self, url):
        self.url = url 
        response = requests.get(self.url, headers=HEADERS) # using request comand we access website and get a response and it has web content
        soup=BeautifulSoup(response.content, 'html.parser')
        self.title=soup.title.string if soup.title else "No title found"
        for extras in soup.body(["img", "style","script", "input"]):
            extras.decompose()
        self.text=soup.body.get_text(separator="\n", strip=True)

    def system_prompt(self, system_prompt):
        self.system_prompt=system_prompt
    
    def user_prompt(self, user_prompt):
        self.user_prompt=user_prompt
    
    def set_messages_for_ollama(self):
        self.messages=[
            {"role" : "system", "content": self.system_prompt},
            {"role" : "user", "content": self.user_prompt}
        ]
    def requiest_ollama(self, model):
        self.model=model
        self.payload = {"model": self.model,"messages": self.messages,"stream": False}
        self.response = requests.post(OLLAMA_API, json=self.payload, headers=HEADERS)
    
    def summarize_web(self):
        print(self.response.json()['message']['content'])



web=website("https://learnobots.com/")
web.system_prompt("You are an AI Agent that parse the website, collect text and provide summarize results. You also ignore the text which are navigaion for")
web.user_prompt(f"You are looking at a website titled {web.title}"+" The contents of this website is as follows\n" +web.text+"\n please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too")
web.set_messages_for_ollama()
web.requiest_ollama("llama3.2")
web.summarize_web()