import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
# Chrome will open visibly (not headless) so you can see it
service = Service(ChromeDriverManager().install())  # Auto-downloads correct driver for macOS

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://google.com")
print("Chrome opened successfully! You should see a Chrome window open.")
print("Waiting 5 seconds so you can see it...")
time.sleep(5)  # Wait 5 seconds so you can see Chrome open
driver.quit()
print("Chrome closed.")
