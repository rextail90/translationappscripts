import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome driver
options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Go to Reverso translation page
    print("Opening Reverso...")
    driver.get("https://www.reverso.net/text-translation")
    time.sleep(3)
    
    # Close popup if it appears
    try:
        close_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='close'], button[aria-label*='Close']")
        if close_btn.is_displayed():
            close_btn.click()
            time.sleep(1)
    except:
        pass
    
    # Find and click English button (left side)
    print("Selecting Arabic as source language...")
    english_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]")
    
    for elem in english_elements:
        if elem.is_displayed() and elem.location['x'] < 600:
            if elem.tag_name != 'a' and not elem.get_attribute('href'):
                # Use WebDriverWait to ensure element is clickable
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_elem = wait.until(EC.element_to_be_clickable(elem))
                    clickable_elem.click()
                    time.sleep(2)
                    break
                except:
                    # If click fails, try direct click
                    elem.click()
                    time.sleep(2)
                    break
    
    # Wait for dropdown to open, then find and click Arabic option
    time.sleep(1)
    arabic_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'arabic')]")
    for opt in arabic_options:
        if opt.is_displayed() and opt.tag_name != 'a' and not opt.get_attribute('href'):
            if opt.tag_name in ['li', 'button', 'div', 'span']:
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                    clickable_opt.click()
                    time.sleep(1)
                    print("Selected Arabic")
                    break
                except:
                    opt.click()
                    time.sleep(1)
                    print("Selected Arabic")
                    break
    
    # Find and click French button (right side) - remember its position
    print("Selecting English as target language...")
    french_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'french')]")
    
    french_button_y = None
    for elem in french_elements:
        if elem.is_displayed() and elem.location['x'] > 300:
            if elem.tag_name != 'a' and not elem.get_attribute('href'):
                french_button_y = elem.location['y']
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_elem = wait.until(EC.element_to_be_clickable(elem))
                    clickable_elem.click()
                    time.sleep(2)
                    break
                except:
                    elem.click()
                    time.sleep(2)
                    break
    
    # Wait for dropdown to open, then find and click English option
    time.sleep(2)
    print("Looking for English in dropdown...")
    english_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]")
    
    print(f"Found {len(english_options)} English elements")
    if french_button_y:
        print(f"French button is at y={french_button_y}, looking for English below it (y > {french_button_y + 20})")
    
    # Debug: print all English elements
    for i, opt in enumerate(english_options):
        if opt.is_displayed():
            print(f"  English element {i}: tag={opt.tag_name}, x={opt.location['x']}, y={opt.location['y']}, text={opt.text[:50]}, href={opt.get_attribute('href')}")
    
    english_selected = False
    
    # Find English in dropdown - it should be below the French button (higher y value)
    for opt in english_options:
        if not opt.is_displayed():
            continue
        
        # Skip links
        if opt.tag_name == 'a' or opt.get_attribute('href'):
            continue
        
        location = opt.location
        tag_name = opt.tag_name.lower()
        
        # Check if it's in the dropdown (below the French button)
        is_in_dropdown = False
        if french_button_y:
            # Dropdown items are below the button (y > french_button_y + some margin)
            if location['y'] > french_button_y + 20:
                is_in_dropdown = True
        else:
            # If we don't know French button position, use x position and reasonable y range
            # Dropdown should be in middle area and not too far down the page
            if 200 < location['x'] < 800 and 300 < location['y'] < 1000:
                is_in_dropdown = True
        
        if is_in_dropdown and tag_name in ['li', 'button', 'div', 'span']:
            # Check if text is just "English" (not "English Definitions" or other phrases)
            text_lower = opt.text.strip().lower()
            if 'english' in text_lower and len(text_lower) < 20:
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                    clickable_opt.click()
                    time.sleep(2)
                    print(f"Selected English from {tag_name} at y={location['y']}")
                    english_selected = True
                    break
                except Exception as e:
                    print(f"Failed to click {tag_name}: {e}")
                    try:
                        opt.click()
                        time.sleep(2)
                        print(f"Selected English from {tag_name} (direct click)")
                        english_selected = True
                        break
                    except:
                        continue
    
    # Verify English is selected by checking URL or visible text
    if not english_selected:
        print("ERROR: Could not select English! Stopping.")
        driver.quit()
        exit(1)
    
    # Wait for dropdown to close and verify English is selected
    time.sleep(2)
    
    # Check URL to verify English is selected (should contain tl=eng)
    current_url = driver.current_url
    if 'tl=eng' in current_url or 'tl=en' in current_url:
        print("English confirmed as target language (verified in URL)")
    else:
        # Try to verify by checking visible text
        print("Warning: Could not verify English in URL, but continuing...")
        print(f"Current URL: {current_url}")
    
    # Find input box
    print("Finding input box...")
    input_box = None
    
    # Try textarea first
    try:
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        for ta in textareas:
            if ta.is_displayed():
                input_box = ta
                break
    except:
        pass
    
    # If no textarea, try contenteditable div
    if not input_box:
        contenteditables = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        for ce in contenteditables:
            if ce.is_displayed() and ce.location['x'] < 500:
                input_box = ce
                break
    
    if not input_box:
        print("Could not find input box")
        driver.quit()
        exit(1)
    
    # Make sure dropdowns are closed before entering text
    print("Waiting for page to be ready...")
    time.sleep(2)
    
    # Enter Arabic text
    arabic_text = "مرحبا"
    print(f"Entering Arabic text: {arabic_text}")
    
    # Try clicking with WebDriverWait
    try:
        wait = WebDriverWait(driver, 5)
        clickable_input = wait.until(EC.element_to_be_clickable(input_box))
        clickable_input.click()
        time.sleep(0.3)
        clickable_input.clear()
        clickable_input.send_keys(arabic_text)
        time.sleep(1)
        print("Text entered using Selenium")
    except:
        # If click fails, use JavaScript to set value
        print("Using JavaScript to enter text...")
        if input_box.tag_name.lower() == 'textarea':
            driver.execute_script("arguments[0].value = arguments[1];", input_box, arabic_text)
        else:
            driver.execute_script("arguments[0].innerText = arguments[1];", input_box, arabic_text)
        # Trigger input event
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", input_box)
        time.sleep(1)
        print("Text entered using JavaScript")
    
    # Wait for translation
    print("Waiting for translation...")
    time.sleep(5)
    
    # Find translation output
    translation = None
    
    # Look for contenteditable divs on right side
    all_contenteditables = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
    for elem in all_contenteditables:
        if elem.is_displayed():
            location = elem.location
            text = elem.text.strip()
            # Check if it's on right side and has different text
            if location['x'] > 400 and text and text != arabic_text:
                if len(text) < 200 and "translate text" not in text.lower():
                    translation = text
                    break
    
    # If not found, try other selectors
    if not translation:
        translation_elems = driver.find_elements(By.CSS_SELECTOR, "div[class*='translation'], span[class*='translation']")
        for elem in translation_elems:
            if elem.is_displayed():
                text = elem.text.strip()
                if text and text != arabic_text and len(text) < 200:
                    if "translate text" not in text.lower():
                        translation = text
                        break
    
    if translation:
        print(f"\nTranslation: {translation}")
    else:
        print("\nCould not find translation")
        print("Keeping browser open for 5 seconds...")
        time.sleep(5)
    
finally:
    driver.quit()
    print("Done")
