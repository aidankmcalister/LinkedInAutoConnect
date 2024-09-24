from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 50)
print(" " * 10 + "Welcome to the LinkedIn Scraper!")
print("=" * 50 + "\n")
print("\nThis script will help you scrape LinkedIn profiles and automatically connect with them.")
print("Please put your LinkedIn credentials in the .env file\n")
print("="*50)

northeast_geourns = "%2C".join([
    "104597301",  # Maine
    "103506248",  # New Hampshire
    "105677329",  # Vermont
    "100506914",  # Massachusetts
    "104150334",  # Rhode Island
    "100448276",  # Connecticut
    "105080838"   # New York
])

while True:
    try:
        amount = int(input("\nEnter the amount of people to connect to: "))
        break
    except ValueError:
        print("Please enter a valid number.")

search_query = input("Enter the search query: ")
print("\n" + "=" * 50)

try:
    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/login')

    email = driver.find_element(By.ID, 'username')
    email.send_keys(os.getenv('LINKEDIN_EMAIL'))

    password = driver.find_element(By.ID, 'password')
    password.send_keys(os.getenv('LINKEDIN_PASSWORD'))
    password.send_keys(Keys.RETURN)

    time.sleep(15)

    search_url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B{
        northeast_geourns}%5D&keywords={search_query}&origin=FACETED_SEARCH&sid=!.@'

    driver.get(search_url)

    people = []
    current_page = 1

    while len(people) < amount:
        wait = WebDriverWait(driver, 10)
        peopleList = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "reusable-search__result-container")))

        for person in peopleList:
            if len(people) < amount:
                name_parent = person.find_element(
                    By.CLASS_NAME, "entity-result__title-text")
                name = name_parent.find_element(
                    By.XPATH, ".//span[@dir='ltr']").find_element(
                    By.XPATH, ".//span[@aria-hidden='true']").text
                try:
                    # Click the "Connect" button
                    # connect_button = driver.find_element(
                    #     (By.XPATH, ".//div[contains(@class, 'entity-result__actions')]//button[contains(text(), 'Connect')]"))
                    connect_container = person.find_element(
                        By.CLASS_NAME, "entity-result__actions")
                    print("connect_container", connect_container)

                    connect_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "button.artdeco-button--secondary"))
                    )
                    connect_button.click()
                    print("connect_button", connect_button)

                    time.sleep(10)
                    connect_button.click()

                    # Wait for the popup to appear
                    wait = WebDriverWait(driver, 10)
                    add_note_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Add a note']")))
                    add_note_button.click()

                    # Type the note
                    note_textarea = wait.until(
                        EC.presence_of_element_located((By.NAME, "message")))
                    note_textarea.send_keys(
                        f'''Hi {name},

                        I hope you're doing well. My name is Aidan, and I'm a junior software engineer with some part-time and contract experience. I'm currently looking to transition into a full-time role and would love to hear your thoughts on navigating the job market, especially as someone without a traditional degree.

                        If you have a few moments to chat, I'd really appreciate the chance to learn from your experience. Looking forward to hearing from you!

                        Best,
                        Aidan''')
                    time.sleep(30)

                    # Send the connection request
                    # send_button = driver.find_element(
                    #     By.XPATH, "//button[contains(@aria-label, 'Send invitation')]")
                    # send_button.click()

                    # Wait for the request to be sent
                    time.sleep(2)
                    status = "✅"
                except Exception as e:
                    status = "❌"
                    print(f"Error: {e}")
                people.append((name, status))
            else:
                break

        if len(people) < amount:
            try:
                current_page += 1
                next_page_url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B{
                    northeast_geourns}%5D&keywords={search_query}&origin=FACETED_SEARCH&sid=!.@&page={current_page}'
                driver.get(next_page_url)
                time.sleep(3)
            except Exception as e:
                print(
                    f"NEXT BUTTON ERROR: {e}")
                break
    print("\n")
    print("Results:\n")
    max_name_length = max(len(name) for name, _ in people) + 4
    for index, (name, status) in enumerate(people, start=1):
        print(f"{index}. {name:<{max_name_length}} {status}")
    print("\n" + "="*50)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
