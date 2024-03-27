
import requests 
from bs4 import BeautifulSoup 

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

response = requests.get(url)

if response.ok: 
    soup = BeautifulSoup(response.text)
    title = soup.find("title")
    print(title.text)












