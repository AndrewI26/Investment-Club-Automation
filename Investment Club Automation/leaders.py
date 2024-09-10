from util import *
from time import sleep

URL = "ENTER_URL"
USERNAME, PASSWORD = "USER", "PASSWORD"
CONTEST_ID = 284570

def getLeaders():
    driver = createDriver()
    driver.get(URL)
    driver.implicitly_wait(0.5)

    click_element(driver, xpath='//*[@id="cookie-banner-btn"]')

    fill_field(driver, USERNAME, field_name="UserName")
    fill_field(driver, PASSWORD, field_name="Password")
    driver.find_element(By.NAME, "Password").submit()
    driver.implicitly_wait(0.5)
    sleep(3)

    driver.get(f"https://www.howthemarketworks.com/accounting/rankings?tournamentID={CONTEST_ID}")
    sleep(5)

    leaders = []
    for i in range(3):
        contestant = driver.find_element(By.XPATH, f'//*[@id="rankings-container"]/table/tbody[2]/tr[{i+2}]/td[3]').get_attribute("innerHTML")
        score = driver.find_element(By.XPATH, f'//*[@id="rankings-container"]/table/tbody[2]/tr[{i+2}]/td[6]/div/div/span').get_attribute("innerHTML")
        leaders.append((contestant, score))

    return leaders


