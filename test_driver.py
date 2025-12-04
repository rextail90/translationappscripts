from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
service = Service("drivers/chromedriver-win64/chromedriver.exe")   # <-- PATH HERE

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://google.com")
print("Chrome opened successfully!")
driver.quit()
