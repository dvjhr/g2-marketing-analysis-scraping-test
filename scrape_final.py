from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from datetime import datetime
import json
import pandas as pd

def screenshot(name=None):
    """screenshot funciton to take and save screenshot of the viewport (useful when doing headless operation)"""
    driver.current_url
    if name:
        name = "_" + name
    driver.save_screenshot(f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png")
    print("Screen Shot!")
    return True

# set up selenium driver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# create new dataframe to save dataframe into csv
df = pd.DataFrame(columns=["Title", "Page URL", "Img"])

# base url
base_url = "https://www.g2.com/categories/marketing-analytics"

# define each element's node with XPATH
card_base = "//div[@id='product-cards']"
card_list = "//div[@class='product-card__head']"
card_header_img = ".//img"
card_header_attrib = ".//a[@itemprop='url']"
card_header_title = ".//div[@class='product-card__product-name']//div[@itemprop='name']"

db = {}

# define number of page to be scraped
num_page = 2

for page in range(num_page):
    print(f"PAGE {page + 1}")
    driver.get(f"{base_url}?page={page + 1}")
    driver.implicitly_wait(5)
    # screenshot()

    # Waiting until page fully loaded and desired element is exist
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, card_list)))

    # iterate trough list of elements
    for elem in driver.find_elements(By.XPATH, card_list):
        driver.implicitly_wait(2)

        elem_attrib = json.loads(
            elem.find_element(By.XPATH, card_header_attrib).get_attribute(
                "data-event-options"
            )
        )
        print(elem_attrib)
        elem_title = elem.find_element(By.XPATH, card_header_title).text
        elem_img = elem.find_element(By.XPATH, card_header_img).get_attribute("data-deferred-image-src")
        elem_url = elem.find_element(By.XPATH, card_header_attrib).get_attribute("href")

        # append new data to dictionary (for json purpose)
        db[elem_attrib["product_id"]] = {
            "title": elem_title,
            "url": elem_url,
            "image": elem_img,
            "attribute": elem_attrib,
        }

        # append data to dataframe (for csv purpose)
        df = df._append({"Title": elem_title, "Page URL": elem_url, "Img": elem_img}, ignore_index=True)
        # break

# dump result
# json
with open('result.json', 'w') as fp:
    json.dump(db, fp)

# csv
df.to_csv("data.csv", index=False)

# clean up
driver.close()
driver.quit()
