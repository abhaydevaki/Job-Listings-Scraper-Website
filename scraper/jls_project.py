from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc


def scrape_jobs(required_role, required_location):
    linkedin_data = []
    indeed_data = []
    glassdoor_data = []

    # Set up Chrome options
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\abhay\\AppData\\Local\\Google\\Chrome\\User Data")  # Adjust path
    options.add_argument("--profile-directory=Profile 2") # Change if needed
    options.add_argument("--disable-blink-features=AutomationControlled") # Helps bypass detection
    options.add_argument("--start-maximized") # Opens browser maximized

    # Initialize undetected ChromeDriver
    driver = uc.Chrome(options=options)
    time.sleep(5)

    # LinkedIn
    required_role_linkedin = required_role.replace(" ", "%20")
    driver.get(f"https://www.linkedin.com/jobs/search/?keywords={required_role_linkedin}&location={required_location}")
    time.sleep(5)

    for _ in range(5):
        try:
            elems = driver.find_elements(By.CSS_SELECTOR, ".flex-grow-1.artdeco-entity-lockup__content.ember-view")
        except NoSuchElementException:
            print("No LinkedIn jobs found")
            break

        for elem in elems:
            linkedin_data.append(elem.get_attribute("outerHTML"))

        time.sleep(5)

        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='View next page']")
            next_button.click()
        except NoSuchElementException:
            break
        time.sleep(3)

    try:
        # Indeed
        for i in range(3):
            required_role_indeed = required_role.replace(" ", "+")
            driver.get(f"https://in.indeed.com/jobs?q={required_role_indeed}&l={required_location}&start={i*15}")
            time.sleep(5)

            elems = driver.find_elements(By.CLASS_NAME, "resultContent")
            for elem in elems:
                indeed_data.append(elem.get_attribute("outerHTML"))

        # Glassdoor
        required_role_glassdoor = required_role.replace(" ", "-")
        driver.get(f"https://www.glassdoor.co.in/Job/{required_role_glassdoor}-jobs-SRCH_KO0,{len(required_role_glassdoor)}.htm")
        time.sleep(5)

        more_button = driver.find_element(By.CSS_SELECTOR, '[data-test="load-more"]')
        more_button.click()
        driver.implicitly_wait(5)
        cross_button_glassdoor = driver.find_element(By.CLASS_NAME, "CloseButton")
        cross_button_glassdoor.click()
        
        for _ in range(4):
            time.sleep(5)
            more_button = driver.find_element(By.CSS_SELECTOR, '[data-test="load-more"]')
            more_button.click()

        elems = driver.find_elements(By.CLASS_NAME, "JobCard_jobCardWrapper__vX29z")
        for elem in elems:
            glassdoor_data.append(elem.get_attribute("outerHTML"))

    except IndexError:
        pass
    
    driver.quit()
    return linkedin_data, indeed_data, glassdoor_data
