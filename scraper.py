from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

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
    successful_connections = 0
    failed_connections = 0

    while successful_connections < amount:
        wait = WebDriverWait(driver, 10)
        peopleList = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "reusable-search__result-container")))

        for person in peopleList:
            if successful_connections < amount:
                name_parent = person.find_element(
                    By.CLASS_NAME, "entity-result__title-text")
                name = name_parent.find_element(
                    By.XPATH, ".//span[@dir='ltr']").find_element(
                    By.XPATH, ".//span[@aria-hidden='true']").text
                try:
                    # Find the connect button within the current person's container
                    connect_button = WebDriverWait(person, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//button[contains(@aria-label, 'Invite') or contains(@aria-label, 'Connect')]"))
                    )

                    # Scroll the button into view
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", connect_button)

                    # Wait for a moment to allow any animations to complete
                    time.sleep(1)

                    # Try to click the button using ActionChains
                    ActionChains(driver).move_to_element(
                        connect_button).click().perform()

                    # Wait for the popup to appear
                    wait = WebDriverWait(driver, 10)
                    add_note_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Add a note']")))
                    add_note_button.click()

                    # Type the note
                    note_textarea = wait.until(
                        EC.presence_of_element_located((By.NAME, "message")))
                    note_textarea.send_keys(
                        f'''Hi {name.split()[0]},

I'm Aidan, a junior software engineer seeking full-time work. As someone without a traditional degree, I'd love your insights on navigating the job market. Could we chat briefly about your experience? Thanks!

Best,
Aidan''')
                    time.sleep(1)
                    # Send the connection request
                    send_button = driver.find_element(
                        By.XPATH, "//button[contains(@aria-label, 'Send invitation')]")
                    send_button.click()
                    # print("Send button found", send_button)

                    # Wait for the request to be sent
                    time.sleep(1)
                    status = "✅"
                    successful_connections += 1
                except (ElementClickInterceptedException, TimeoutException) as e:
                    print(f"Error connecting to {name}: {e}")
                    status = "❌"
                    failed_connections += 1

                people.append((name, status))
            else:
                break

        if successful_connections < amount:
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

    print(f"\nFailed connections (❌): {failed_connections}")
    print(f"Successful connections (✅): {successful_connections}")
    print("\n" + "="*50)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
