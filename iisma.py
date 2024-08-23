from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


chrome_options = Options()
chrome_options.add_argument("--headless")  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service() 
driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://iisma.kemdikbud.go.id/info/host-universities-list/"
driver.get(url)


wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swiper-slide")))


html = driver.page_source


soup = BeautifulSoup(html, 'html.parser')


slides = soup.find_all('div', class_='swiper-slide')

for slide in slides:
    
    img = slide.find('img', class_='swiper-slide-image')
    if img:
        img_src = img.get('src')
        img_alt = img.get('alt')
    
    link = slide.find('a')
    if link:
        href = link.get('href')
    
    print(f"Image: {img_src}")
    print(f"Alt text: {img_alt}")
    print(f"Link: {href}")
    print("---")

driver.quit()