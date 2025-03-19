from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
import time


chromeService = webdriver.ChromeService(
    executable_path=r"C:\Users\rodin\Documents\chromedriver-win64\chromedriver.exe"
)
driver = webdriver.Chrome(service=chromeService)


def startService():

    driver.get("https://mvla.instructure.com/login/canvas")


def autoLoginAndSetup():  # Login and navigate to calender on canvas

    driver.find_element(By.XPATH, '//*[@id="login_form"]/div[4]/ul/li/a').click()

    username = "100032385"

    googleUsername = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    googleUsername.send_keys(username)

    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

    mvlaUsername = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    mvlaUsername.send_keys(username)
    mvlaPassword = driver.find_element(By.ID, "password")
    mvlaPassword.send_keys("R0din23!!!")

    driver.find_element(By.ID, "signin").click()

    pin = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "enter_pin"))
    )
    pin.send_keys("623682")

    # bybass human detection?
    time.sleep(1.5)
    try:
        pin.send_keys(Keys.ARROW_LEFT)
    except Exception:
        print("uhoh")

    try:
        confirmButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div/button',
                )
            )
        )

        confirmButton.click()

    except TimeoutException:
        print("Confirmation button not found or clickable within 10 seconds.")

    except Exception as e:
        print(f"An error occured: {e}")
    try:
        dashboardButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="right-side"]/div[1]/div/div/button')
            )
        )
        dashboardButton.click()
    except Exception:
        print("ohwell")

    # loads additional tasks
    driver.find_element(
        By.XPATH, '//*[@id="dashboard-planner"]/div/div[9]/div/button'
    ).click()
    time.sleep(1)


def getTasks():

    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    dayElements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".Day-styles__root.planner-day")
        )
    )

    allTasks = {}

    for dayElement in dayElements:
        dayNameElement = dayElement.find_element(By.CSS_SELECTOR, "h2")
        dayName = dayNameElement.text.strip()

        if "Today\n" in dayName:
            dayName.replace("Today\n", today.strftime("%A") + ", ")
        elif "Tomorrow" in dayName:
            dayName.replace("Tomorrow", tomorrow.strftime("%A"))

        allTasks[dayName] = []

        listElements = dayElement.find_elements(By.CSS_SELECTOR, "li")
        for listElement in listElements:
            individualTaskElement = listElement.find_element(
                By.CSS_SELECTOR, ".PlannerItem-styles__root"
            )
            individualTask = individualTaskElement.text.strip()
            print(individualTask)


startService()
autoLoginAndSetup()
getTasks()

time.sleep(400)
