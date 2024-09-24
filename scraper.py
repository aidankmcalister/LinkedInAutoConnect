from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

with open('info.json', 'r') as f:
    info = json.load(f)

print("\n" + "=" * 50)
print(" " * 10 + "Welcome to the LinkedIn Scraper!")
print("=" * 50 + "\n")
print("\nThis script will help you scrape LinkedIn profiles and automatically connect with them.\n")
print("--"*50)

northeast_geourns = "%2C".join(info['geourns']['northeast'])

amount = info['amount_to_connect']
search_query = info['search_query']

print(f"\nConnecting to {amount} people with search query: {search_query}")
print("\n" + "-" * 50)

try:
    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/login')

    email = driver.find_element(By.ID, 'username')
    email.send_keys(info['linkedin_credentials']['email'])

    password = driver.find_element(By.ID, 'password')
    password.send_keys(info['linkedin_credentials']['password'])
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
                    connect_button = WebDriverWait(person, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//button[contains(@aria-label, 'Invite') or contains(@aria-label, 'Connect')]"))
                    )

                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", connect_button)

                    time.sleep(1)

                    ActionChains(driver).move_to_element(
                        connect_button).click().perform()

                    wait = WebDriverWait(driver, 10)
                    add_note_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Add a note']")))
                    add_note_button.click()

                    note_textarea = wait.until(
                        EC.presence_of_element_located((By.NAME, "message")))
                    note_textarea.send_keys(
                        info['connection_message'].format(first_name=name.split()[0]))
                    time.sleep(1)

                    send_button = driver.find_element(
                        By.XPATH, "//button[contains(@aria-label, 'Send invitation')]")
                    send_button.click()

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
                print(f"NEXT BUTTON ERROR: {e}")
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
