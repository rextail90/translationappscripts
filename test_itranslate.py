import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome driver
options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Go to iTranslate translation page
    print("Opening iTranslate...")
    driver.get("https://itranslate.com/translate")
    time.sleep(3)
    
    # Close popup if it appears
    try:
        close_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='close'], button[aria-label*='Close'], button.close")
        if close_btn.is_displayed():
            close_btn.click()
            time.sleep(1)
    except:
        pass
    
    # Find and click the left language selector button (source language)
    print("Clicking left language selector to select Arabic (U.A.E.)...")
    source_button_y = None
    
    # Find language selector button on left side - look for buttons specifically
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if btn.is_displayed() and btn.location['x'] < 500:
            btn_text = btn.text.strip().lower()
            # Skip if it's the page title or heading
            if btn.tag_name == 'h1' or btn.tag_name == 'h2' or 'translate' in btn_text and 'to' in btn_text:
                continue
            # Look for language selector buttons (should have language name and be clickable)
            if any(word in btn_text for word in ['english', 'spanish', 'french', 'arabic', 'detect']) and len(btn_text) < 50:
                source_button_y = btn.location['y']
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_btn = wait.until(EC.element_to_be_clickable(btn))
                    clickable_btn.click()
                    time.sleep(2)
                    print(f"Clicked left language selector button")
                    break
                except:
                    btn.click()
                    time.sleep(2)
                    print(f"Clicked left language selector button")
                    break
    
    # If button not found, try div elements that act as buttons
    if not source_button_y:
        divs = driver.find_elements(By.CSS_SELECTOR, "div[role='button'], div[class*='selector'], div[class*='language']")
        for div in divs:
            if div.is_displayed() and div.location['x'] < 500:
                div_text = div.text.strip().lower()
                if any(word in div_text for word in ['english', 'spanish', 'french']) and len(div_text) < 50:
                    source_button_y = div.location['y']
                    try:
                        wait = WebDriverWait(driver, 5)
                        clickable_div = wait.until(EC.element_to_be_clickable(div))
                        clickable_div.click()
                        time.sleep(2)
                        print(f"Clicked left language selector div")
                        break
                    except:
                        div.click()
                        time.sleep(2)
                        print(f"Clicked left language selector div")
                        break
    
    # Wait for dropdown to open, then find and click UAE Arabic
    time.sleep(1)
    print("Looking for Arabic (U.A.E.) in dropdown...")
    
    # Find dropdown container and scroll through it
    dropdown_container = None
    try:
        dropdowns = driver.find_elements(By.CSS_SELECTOR, "div[class*='dropdown'], div[class*='menu'], ul[class*='menu'], div[class*='list']")
        for dd in dropdowns:
            if dd.is_displayed() and dd.location['x'] < 500:
                dropdown_container = dd
                break
    except:
        pass
    
    arabic_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'arabic')]")
    
    arabic_selected = False
    
    # First, try to find Arabic (U.A.E.) without scrolling
    for opt in arabic_options:
        if opt.is_displayed() and opt.tag_name != 'a' and not opt.get_attribute('href'):
            if opt.tag_name in ['li', 'button', 'div', 'span']:
                text_lower = opt.text.strip().lower()
                is_in_dropdown = False
                if source_button_y:
                    if opt.location['y'] > source_button_y + 20:
                        is_in_dropdown = True
                else:
                    if 200 < opt.location['x'] < 800 and 300 < opt.location['y'] < 1000:
                        is_in_dropdown = True
                
                # Look for Arabic (U.A.E.) specifically
                if is_in_dropdown and 'arabic' in text_lower and ('u.a.e' in text_lower or 'uae' in text_lower):
                    try:
                        wait = WebDriverWait(driver, 5)
                        clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                        clickable_opt.click()
                        time.sleep(1)
                        print(f"Selected Arabic (U.A.E.) - found: {opt.text}")
                        arabic_selected = True
                        break
                    except:
                        opt.click()
                        time.sleep(1)
                        print(f"Selected Arabic (U.A.E.) - found: {opt.text}")
                        arabic_selected = True
                        break
    
    # If not found, scroll through dropdown to find it
    if not arabic_selected and dropdown_container:
        print("Arabic (U.A.E.) not visible, scrolling dropdown...")
        try:
            # Scroll to find Arabic (U.A.E.)
            driver.execute_script("arguments[0].scrollTop = 0;", dropdown_container)
            time.sleep(0.5)
            
            # Search through dropdown by scrolling
            for scroll_pos in range(0, 2000, 100):
                driver.execute_script(f"arguments[0].scrollTop = {scroll_pos};", dropdown_container)
                time.sleep(0.3)
                
                # Re-find Arabic options after scrolling
                arabic_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'arabic')]")
                for opt in arabic_options:
                    if opt.is_displayed() and opt.tag_name != 'a' and not opt.get_attribute('href'):
                        text_lower = opt.text.strip().lower()
                        if 'arabic' in text_lower and ('u.a.e' in text_lower or 'uae' in text_lower):
                            try:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opt)
                                time.sleep(0.5)
                                wait = WebDriverWait(driver, 5)
                                clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                                clickable_opt.click()
                                time.sleep(1)
                                print(f"Selected Arabic (U.A.E.) after scrolling - found: {opt.text}")
                                arabic_selected = True
                                break
                            except:
                                opt.click()
                                time.sleep(1)
                                print(f"Selected Arabic (U.A.E.) after scrolling - found: {opt.text}")
                                arabic_selected = True
                                break
                
                if arabic_selected:
                    break
        except Exception as e:
            print(f"Error scrolling dropdown: {e}")
    
    if not arabic_selected:
        print("WARNING: Could not find Arabic (U.A.E.), trying any Arabic...")
        # Re-find elements to avoid stale element reference
        try:
            arabic_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'arabic')]")
            for opt in arabic_options:
                try:
                    if opt.is_displayed() and opt.tag_name != 'a' and not opt.get_attribute('href'):
                        text_lower = opt.text.strip().lower()
                        if 'arabic' in text_lower:
                            opt.click()
                            time.sleep(1)
                            print(f"Selected Arabic (fallback): {opt.text}")
                            arabic_selected = True
                            break
                except:
                    continue
        except:
            pass
    
    # Wait a bit to ensure left dropdown is closed and Arabic (U.A.E.) is selected
    time.sleep(3)
    print("Left language should be Arabic (U.A.E.) - leaving it alone")
    
    # Find and click the right language selector button (target language) ONLY
    print("Clicking right language selector to select English (United States)...")
    target_button_y = None
    
    # Find language selector button on right side - be very specific about right side (x > 500)
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if btn.is_displayed() and btn.location['x'] > 500:  # More specific - must be clearly on right side
            btn_text = btn.text.strip().lower()
            # Skip if it's the page title or heading
            if 'translate' in btn_text and 'to' in btn_text:
                continue
            # Look for language selector buttons on right side only
            if any(word in btn_text for word in ['english', 'spanish', 'german', 'french']) and len(btn_text) < 50:
                target_button_y = btn.location['y']
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_btn = wait.until(EC.element_to_be_clickable(btn))
                    clickable_btn.click()
                    time.sleep(2)
                    print(f"Clicked right language selector button (x={btn.location['x']})")
                    break
                except:
                    btn.click()
                    time.sleep(2)
                    print(f"Clicked right language selector button (x={btn.location['x']})")
                    break
    
    # If button not found, try div elements that act as buttons - but only on right side
    if not target_button_y:
        divs = driver.find_elements(By.CSS_SELECTOR, "div[role='button'], div[class*='selector'], div[class*='language']")
        for div in divs:
            if div.is_displayed() and div.location['x'] > 500:  # More specific - must be clearly on right side
                div_text = div.text.strip().lower()
                if any(word in div_text for word in ['english', 'spanish', 'german']) and len(div_text) < 50:
                    target_button_y = div.location['y']
                    try:
                        wait = WebDriverWait(driver, 5)
                        clickable_div = wait.until(EC.element_to_be_clickable(div))
                        clickable_div.click()
                        time.sleep(2)
                        print(f"Clicked right language selector div (x={div.location['x']})")
                        break
                    except:
                        div.click()
                        time.sleep(2)
                        print(f"Clicked right language selector div (x={div.location['x']})")
                        break
    
    # Wait for dropdown to fully open
    time.sleep(2)
    print("Waiting for dropdown to open...")
    
    # Find dropdown container and scroll through it - ONLY right side dropdown
    dropdown_container = None
    try:
        dropdowns = driver.find_elements(By.CSS_SELECTOR, "div[class*='dropdown'], div[class*='menu'], ul[class*='menu'], div[class*='list']")
        for dd in dropdowns:
            if dd.is_displayed() and dd.location['x'] > 500:  # Only right side dropdown
                dropdown_container = dd
                print(f"Found right dropdown container at x={dd.location['x']}")
                break
    except:
        pass
    
    # Wait a bit more to ensure dropdown is fully loaded
    time.sleep(1)
    print("Looking for English (United States) in dropdown...")
    
    english_selected = False
    
    # First, try to find English (United States) without scrolling
    # Only look for English, explicitly skip Spanish
    english_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]")
    
    for opt in english_options:
        if not opt.is_displayed():
            continue
        
        # Skip links
        if opt.tag_name == 'a' or opt.get_attribute('href'):
            continue
        
        location = opt.location
        tag_name = opt.tag_name.lower()
        text_lower = opt.text.strip().lower()
        
        # Explicitly skip Spanish
        if 'spanish' in text_lower:
            continue
        
        # Only consider elements on the right side (x > 500) and in dropdown
        is_in_dropdown = False
        if location['x'] > 500:
            if target_button_y:
                # Must be below the button (in dropdown)
                if location['y'] > target_button_y + 20:
                    is_in_dropdown = True
            else:
                # Must be in dropdown area
                if 500 < location['x'] < 1000 and 300 < location['y'] < 1000:
                    is_in_dropdown = True
        
        # Look for English (United States) specifically - skip all other variants
        if is_in_dropdown and tag_name in ['li', 'button', 'div', 'span']:
            # Only select if it's English (United States) - be very specific
            if ('united states' in text_lower or ('us' in text_lower and 'united' in text_lower)) and 'uk' not in text_lower and 'australia' not in text_lower and 'canada' not in text_lower and 'spanish' not in text_lower:
                try:
                    wait = WebDriverWait(driver, 5)
                    clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                    clickable_opt.click()
                    time.sleep(2)
                    print(f"Selected English (United States) - found: {opt.text}")
                    english_selected = True
                    break
                except:
                    try:
                        opt.click()
                        time.sleep(2)
                        print(f"Selected English (United States) - found: {opt.text}")
                        english_selected = True
                        break
                    except:
                        continue
    
    # If not found, scroll through dropdown to find it
    if not english_selected and dropdown_container:
        print("English (United States) not visible, scrolling dropdown...")
        try:
            # Scroll to find English (United States)
            driver.execute_script("arguments[0].scrollTop = 0;", dropdown_container)
            time.sleep(0.5)
            
            # Search through dropdown by scrolling
            for scroll_pos in range(0, 2000, 100):
                driver.execute_script(f"arguments[0].scrollTop = {scroll_pos};", dropdown_container)
                time.sleep(0.3)
                
                # Re-find English options after scrolling to avoid stale elements
                try:
                    english_options = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]")
                    for opt in english_options:
                        try:
                            if not opt.is_displayed():
                                continue
                            if opt.tag_name == 'a' or opt.get_attribute('href'):
                                continue
                            
                            text_lower = opt.text.strip().lower()
                            
                            # Explicitly skip Spanish
                            if 'spanish' in text_lower:
                                continue
                            
                            # Look for English (United States) - be very specific
                            if ('united states' in text_lower or (text_lower == 'english (united states)' or 'english (us)' in text_lower)) and 'uk' not in text_lower and 'australia' not in text_lower and 'canada' not in text_lower and 'spanish' not in text_lower:
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opt)
                                    time.sleep(0.5)
                                    wait = WebDriverWait(driver, 5)
                                    clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                                    clickable_opt.click()
                                    time.sleep(2)
                                    print(f"Selected English (United States) after scrolling - found: {opt.text}")
                                    english_selected = True
                                    break
                                except Exception as e:
                                    print(f"Error clicking option: {e}")
                                    try:
                                        opt.click()
                                        time.sleep(2)
                                        print(f"Selected English (United States) after scrolling (direct) - found: {opt.text}")
                                        english_selected = True
                                        break
                                    except:
                                        continue
                        except:
                            continue
                except:
                    continue
                
                if english_selected:
                    break
        except Exception as e:
            print(f"Error scrolling dropdown: {e}")
    
    if not english_selected:
        print("ERROR: Could not select English (United States)! Stopping.")
        driver.quit()
        exit(1)
    
    time.sleep(2)
    
    # Find input box - try by ID first, then by tag
    print("Finding input box...")
    input_box = None
    
    try:
        # Try to find by ID first (sourceInputField)
        input_box = driver.find_element(By.ID, "sourceInputField")
        print("Found input box by ID: sourceInputField")
    except:
        try:
            # Try by name
            input_box = driver.find_element(By.NAME, "sourceText")
            print("Found input box by name: sourceText")
        except:
            # Fallback to finding by tag
            textareas = driver.find_elements(By.TAG_NAME, "textarea")
            for ta in textareas:
                if ta.is_displayed() and ta.location['x'] < 500:
                    input_box = ta
                    print("Found input box by tag and position")
                    break
    
    if not input_box:
        contenteditables = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        for ce in contenteditables:
            if ce.is_displayed() and ce.location['x'] < 500:
                input_box = ce
                print("Found input box as contenteditable div")
                break
    
    if not input_box:
        print("Could not find input box")
        driver.quit()
        exit(1)
    
    # Enter Arabic text using Selenium methods
    arabic_text = "مرحبا"
    print(f"Entering Arabic text using Selenium: {arabic_text}")
    
    try:
        # Scroll element into view first to avoid interception
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)
        time.sleep(0.5)
        
        # Wait for input to be present
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, "sourceInputField")))
        
        # Use ActionChains to move to element and click
        actions = ActionChains(driver)
        actions.move_to_element(input_box)
        actions.click()
        actions.perform()
        time.sleep(0.3)
        
        # Clear any existing text
        input_box.clear()
        time.sleep(0.2)
        
        # Send keys using ActionChains
        actions = ActionChains(driver)
        actions.send_keys(arabic_text)
        actions.perform()
        time.sleep(1)
        print("Text entered using Selenium ActionChains")
        
    except Exception as e:
        print(f"ActionChains failed: {e}, trying direct send_keys...")
        try:
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)
            time.sleep(0.5)
            
            # Try direct send_keys without clicking
            input_box.clear()
            input_box.send_keys(arabic_text)
            time.sleep(1)
            print("Text entered using Selenium send_keys (no click)")
        except Exception as e2:
            print(f"Direct send_keys failed: {e2}, trying with focus...")
            try:
                # Use JavaScript to focus, then Selenium to type
                driver.execute_script("arguments[0].focus();", input_box)
                time.sleep(0.3)
                input_box.clear()
                input_box.send_keys(arabic_text)
                time.sleep(1)
                print("Text entered using Selenium after JavaScript focus")
            except Exception as e3:
                print(f"All Selenium methods failed: {e3}")
                raise
    
    # Wait for translation
    print("Waiting for translation...")
    time.sleep(5)
    
    # Find translation output
    translation = None
    
    all_contenteditables = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
    for elem in all_contenteditables:
        if elem.is_displayed():
            location = elem.location
            text = elem.text.strip()
            if location['x'] > 400 and text and text != arabic_text:
                if len(text) < 200 and "translate text" not in text.lower():
                    translation = text
                    break
    
    if not translation:
        translation_elems = driver.find_elements(By.CSS_SELECTOR, "div[class*='translation'], span[class*='translation'], div[class*='target'], div[class*='output']")
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

