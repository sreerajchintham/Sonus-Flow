import requests
from bs4 import BeautifulSoup
def get_novel(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    
