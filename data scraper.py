import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from math import nan
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors')
driver.maximize_window()

#10 second pause to allow user to complete captcha
time.sleep(10)
driver.find_element(by=By.XPATH, value='//*[@id="onetrust-close-btn-container"]/button').click() #deny cookies

newdf_dict = {'Major':[],'Early Career Pay':[], 'Mid-Career Pay':[], '% High Meaning':[]}

for _ in range(int(driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[1]/article/div[3]/a[6]/div').text)):
    all_rows = driver.find_elements(by=By.CSS_SELECTOR, value='tr.data-table__row')
    for row in all_rows:
        rw_text = row.find_elements(by=By.CSS_SELECTOR, value='span.data-table__value')

        try: newdf_dict['Major'].append(rw_text[1].text)
        except ValueError:
            newdf_dict['Major'].append(nan)

        try: newdf_dict['Early Career Pay'].append(float(rw_text[3].text.replace('$','').replace(',','')))
        except ValueError:
            newdf_dict['Early Career Pay'].append(nan)

        try: newdf_dict['Mid-Career Pay'].append(float(rw_text[4].text.replace('$','').replace(',','')))
        except ValueError:
            newdf_dict['Mid-Career Pay'].append(nan)

        try: newdf_dict['% High Meaning'].append(float(rw_text[5].text.replace('%','')))
        except ValueError:
            newdf_dict['% High Meaning'].append(nan)
    driver.find_element(by=By.CSS_SELECTOR, value='a.pagination__btn.pagination__next-btn').click()
    time.sleep(1)

df_updated = pd.DataFrame(data=newdf_dict)
df_updated.to_csv('data/PayScale Bachelors 2025.csv', index=False)