from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()

amount = int(input("Enter the amount of people to connect to: "))
search_query = input("Enter the search query: ")

try:
    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/login')

    email = driver.find_element(By.ID, 'username')
    email.send_keys(os.getenv('LINKEDIN_EMAIL'))

    password = driver.find_element(By.ID, 'password')
    password.send_keys(os.getenv('LINKEDIN_PASSWORD'))
    password.send_keys(Keys.RETURN)

    time.sleep(15)

    driver.get(f'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords={
               search_query}&origin=FACETED_SEARCH&profileLanguage=%5B%22en%22%5D&sid=WJ)')

    people = []

    while len(people) < amount:
        wait = WebDriverWait(driver, 10)
        peopleList = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "reusable-search__result-container")))

        for person in peopleList:
            if len(people) < amount:
                # driver.find_element(
                #     By.CLASS_NAME, "search-reusables-modal__close-btn").click()
                name_parent = person.find_element(
                    By.CLASS_NAME, "entity-result__title-text")
                name = name_parent.find_element(
                    By.XPATH, ".//span[@dir='ltr']").find_element(
                    By.XPATH, ".//span[@aria-hidden='true']").text
                people.append(name)
            else:
                break

            # next_button = driver.find_element(
            #     By.XPATH, "//button[@aria-label='Next']")

        if len(people) < amount:
            try:
                wait = WebDriverWait(driver, 10)
                next_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.artdeco-pagination__button--next")))
                next_button.click()
            except Exception as e:
                print(
                    f"An error occurred while trying to navigate to the next page: {e}")
                break
    print(people)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
