# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import time

# website = "https://www.ouedkniss.com"  
# path = r"C:\Users\Hp\Desktop\Data Collection\Business Analysis\chromedriver.exe"
# service = Service(path)
# driver = webdriver.Chrome(service=service)
# driver.get(website)

# def get_all_pages():
#     urls=[]
#     page_number=1
#     for i in range(105):
#         i=f"https://www.ouedkniss.com/s/{page_number}?keywords=formation"
#         page_number +=1
#         urls.append(i)
#     return urls


# def scroll_incrementally(driver):
#     unique_schools = set()
#     last_height = driver.execute_script("return document.body.scrollHeight")
    
#     while True:
#         # Calculate current scroll height
#         current_height = driver.execute_script("return document.body.scrollHeight")
        
#         # Scroll in smaller increments (20 steps per screen height)
#         scroll_increment = current_height // 20
#         view_height = driver.execute_script("return window.innerHeight")
#         current_position = driver.execute_script("return window.pageYOffset")
        
#         # Scroll to next position
#         next_position = min(current_position + scroll_increment, current_height - view_height)
#         driver.execute_script(f"window.scrollTo(0, {next_position});")
#         time.sleep(1)  # Short pause between scrolls
        
#         # Find all school elements currently visible
#         school_elements = driver.find_elements(By.CLASS_NAME, 'o-announ-card-title')
        
#         for element in school_elements:
#             school_name = element.text.strip()
#             if school_name and school_name not in unique_schools:
#                 try:
#                     # Click on the element to go to its page
#                     element.click()
#                     time.sleep(2)  # Wait for page to load
                    
#                     # Add to set and print
#                     unique_schools.add(school_name)
#                     print("School:", school_name)

#                     price_elements = driver.find_elements(By.XPATH, "//div[@class='mr-1']")
#                     # Check if price is available
#                     if price_elements:
#                         print("Price:", price_elements[0].text)
#                     else:
#                         print("Price: Missing")  # Handle missing price

#                     # Scroll down a bit before getting contacts
#                     driver.execute_script("window.scrollBy(0, 1200);")  # Scroll down 300 pixels
#                     time.sleep(1)  # Wait for scroll to complete      

#                                         # Initialize contact list
#                     contacts = []
                    
#                     # Look specifically for the phone number links with the correct classes
#                     contact_elements = driver.find_elements(
#                         By.XPATH, 
#                         "//a[contains(@class, 'v-btn') and contains(@class, 'bg-primary')]"
#                     )
                    
#                     for contact in contact_elements:
#                         href = contact.get_attribute('href')
#                         if href:
#                             # Extract the phone number from the href
#                             phone_number = href.replace('tel:', '').strip()
#                             contacts.append(phone_number)
                    
#                     if contacts:
#                         print("Contacts:", ", ".join(contacts))
#                     else:
#                         print("Contacts: Missing")

#                     school_name = driver.find_elements(By.XPATH, "//h4[contains(@class,'text-h6') and contains(@class, 'text-capitalize')]")
#                     # Check if price is available
#                     if school_name:
#                         print("School_Name:", school_name[0].text)
#                     else:
#                         print("School_Name: Missing")  # Handle missing price
                          
#                     # Find elements by XPath
#                     details = driver.find_elements(
#                         By.XPATH, 
#                         "//div[contains(@class, 'align-left')]"    
#                     )

#                     if details:
#                         # Extract text from each element and join them
#                         detail_texts = [detail.text for detail in details]
#                         print("Details:", ", ".join(detail_texts))
#                     else:
#                         print("Details: Missing")
#                     # Go back to main page
#                     driver.back()
#                     time.sleep(1)  # Wait for main page to reload
#                 except:
#                     print(f"Failed to process school: {school_name}")
#                     continue
        
#         # Check if we've reached the bottom
#         if next_position >= current_height - view_height:
#             # Double check if there's new content
#             time.sleep(2)  # Wait for potential dynamic content
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break  # Exit if no new content loaded
#             last_height = new_height
        
#         current_position = next_position

#     return unique_schools    

# search_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.NAME, 'searchField'))
# )
# search_box.click()
# search_box.send_keys("formation")
# search_box.send_keys(Keys.RETURN)

# try:
#     # Wait for initial content to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'o-store-card-title'))
#     )
    
#     # Perform incremental scrolling
#     scroll_incrementally(driver)

# except Exception as e:
#     print("Error occurred:", str(e))
# finally:
#     driver.quit()

# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from scraper import search_and_scrape

# # # Configuration du navigateur
# # website = "https://www.ouedkniss.com"
# # path = r"C:\Users\Hp\Desktop\Data Collection\Business Analysis\chromedriver.exe"

# # service = Service(path)
# # driver = webdriver.Chrome(service=service)
# # driver.get(website)

# # try:
# #     search_and_scrape(driver, "formation")
# # except Exception as e:
# #     print("Error occurred:", str(e))
# # finally:
# #     driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import spacy
import time
from typing import Dict, Any
import re

class SpacyTextAnalyzer:
    def __init__(self):
        """Initialize the SpacyTextAnalyzer with French language model."""
        self.nlp = spacy.load("fr_core_news_md")
        
    def extract_structured_info(self, text: str) -> Dict[str, Any]:
        doc = self.nlp(text)
        structured_data = {
            'objectives': [],
            'modules': [],
            'duration': None
        }

        # Split text into sections
        sections = self._split_into_sections(text)
        
        # Extract objectives
        if 'objectif' in sections:
            objective_doc = self.nlp(sections['objectif'])
            objectives = [sent.text.strip() for sent in objective_doc.sents
                        if ('o ' in sent.text or '- ' in sent.text)
                        and len(sent.text.strip()) > 10]
            
            if not objectives:
                objectives = [sent.text.strip() for sent in objective_doc.sents
                            if len(sent.text.strip()) > 10]
            
            structured_data['objectives'] = objectives

        # Extract modules/program content
        if 'programme' in sections:
            modules = re.findall(r'\d+\.\s+([^.]+)', sections['programme'])
            if modules:
                structured_data['modules'] = [module.strip() for module in modules]
            else:
                program_doc = self.nlp(sections['programme'])
                modules = [sent.text.strip() for sent in program_doc.sents
                         if len(sent.text.strip()) > 10]
                structured_data['modules'] = modules

        # Extract duration
        duration_patterns = [
            r'\d+\s*(?:heures?|h|jours?|j|semaines?|mois)',
            r'durée\s*:?\s*\d+\s*(?:heures?|h|jours?|j|semaines?|mois)'
        ]
        
        for pattern in duration_patterns:
            duration_match = re.search(pattern, text.lower())
            if duration_match:
                structured_data['duration'] = duration_match.group(0)
                break

        return structured_data

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        text_lower = text.lower()
        
        markers = {
            'objectif': ['objectif', 'objectifs', 'but'],
            'programme': ['programme', 'modules', 'contenu'],
            'prerequis': ['prerequis', 'prérequis'],
            'duration': ['durée', 'duration']
        }
        
        positions = []
        for section_type, marker_list in markers.items():
            for marker in marker_list:
                pos = text_lower.find(marker)
                if pos != -1:
                    positions.append((pos, section_type))
        
        positions.sort()
        
        for i, (pos, section_type) in enumerate(positions):
            start = pos
            end = positions[i + 1][0] if i < len(positions) - 1 else len(text)
            sections[section_type] = text[start:end].strip()
            
        return sections

def get_all_pages():
    urls = []
    page_number = 1
    for i in range(105):
        i = f"https://www.ouedkniss.com/s/{page_number}?keywords=formation"
        page_number += 1
        urls.append(i)
    return urls

def scroll_incrementally(driver):
    # Initialize the SpaCy analyzer
    analyzer = SpacyTextAnalyzer()
    
    unique_schools = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        current_height = driver.execute_script("return document.body.scrollHeight")
        scroll_increment = current_height // 20
        view_height = driver.execute_script("return window.innerHeight")
        current_position = driver.execute_script("return window.pageYOffset")
        
        next_position = min(current_position + scroll_increment, current_height - view_height)
        driver.execute_script(f"window.scrollTo(0, {next_position});")
        time.sleep(1)
        
        school_elements = driver.find_elements(By.CLASS_NAME, 'o-announ-card-title')
        
        for element in school_elements:
            school_name = element.text.strip()
            if school_name and school_name not in unique_schools:
                try:
                    element.click()
                    time.sleep(2)
                    
                    unique_schools.add(school_name)
                    print("\n" + "="*50)
                    print("School:", school_name)

                    price_elements = driver.find_elements(By.XPATH, "//div[@class='mr-1']")
                    if price_elements:
                        print("Price:", price_elements[0].text)
                    else:
                        print("Price: Missing")

                    driver.execute_script("window.scrollBy(0, 1200);")
                    time.sleep(1)

                    contacts = []
                    contact_elements = driver.find_elements(
                        By.XPATH, 
                        "//a[contains(@class, 'v-btn') and contains(@class, 'bg-primary')]"
                    )
                    
                    for contact in contact_elements:
                        href = contact.get_attribute('href')
                        if href:
                            phone_number = href.replace('tel:', '').strip()
                            contacts.append(phone_number)
                    
                    if contacts:
                        print("Contacts:", ", ".join(contacts))
                    else:
                        print("Contacts: Missing")

                    school_name = driver.find_elements(By.XPATH, "//h4[contains(@class,'text-h6') and contains(@class, 'text-capitalize')]")
                    if school_name:
                        print("School_Name:", school_name[0].text)
                    else:
                        print("School_Name: Missing")
                          
                    details = driver.find_elements(
                        By.XPATH, 
                        "//div[contains(@class, 'align-left')]"    
                    )

                    if details:
                        detail_texts = [detail.text for detail in details]
                        raw_text = " ".join(detail_texts)
                        
                        # Use SpaCy analyzer to extract structured information
                        structured_info = analyzer.extract_structured_info(raw_text)
                        
                        print("\nStructured Details:")
                        if structured_info['objectives']:
                            print("\nObjectives:")
                            for obj in structured_info['objectives']:
                                print(f"- {obj}")
                                
                        if structured_info['modules']:
                            print("\nModules:")
                            for i, module in enumerate(structured_info['modules'], 1):
                                print(f"{i}. {module}")
                                
                        if structured_info['duration']:
                            print(f"\nDuration: {structured_info['duration']}")
                        
                        print("\nRaw Details:", raw_text)
                    else:
                        print("Details: Missing")
                        
                    driver.back()
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Failed to process school: {school_name}")
                    print(f"Error: {str(e)}")
                    continue
        
        if next_position >= current_height - view_height:
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        current_position = next_position

    return unique_schools

def main():
    website = "https://www.ouedkniss.com"
    path = r"C:\Users\Hp\Desktop\Data Collection\Business Analysis\chromedriver.exe"
    service = Service(path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'searchField'))
        )
        search_box.click()
        search_box.send_keys("formation")
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'o-store-card-title'))
        )
        
        scroll_incrementally(driver)

    except Exception as e:
        print("Error occurred:", str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

    