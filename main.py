import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

string.ascii_letters = 'abcdefghijklmnopqrstuvwxyz' #ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

script = "console.log('Hello, world!');"
HASH = "sha256-8c05bce2a2b29e1a719c0dcb5c52b83a28b0c4bbdf7c4e4f145059b0c291776d"

# Add the CSP header with the HASH value
chrome_options.add_argument("--csp=" + f"script-src '{HASH}'")

driver.get("https://quizlet.com/")
print(driver.title)
driver.execute_script(script)

assert "Quizlet" in driver.title

button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Sign up"]')
button.click()
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')


def login():
       month = Select(driver.find_element(By.CSS_SELECTOR, 'select[aria-label="birth_month"]'))
       month.select_by_index(1)


       day = Select(driver.find_element(By.CSS_SELECTOR, 'select[aria-label="birth_day"]'))
       day.select_by_index(1)


       year = Select(driver.find_element(By.CSS_SELECTOR, 'select[aria-label="birth_year"]'))
       year.select_by_index(1)

       while(True):
              email = driver.find_element(By.ID, 'email')
              email.send_keys(random_char(5)+"@gmail.com")
              email.send_keys(Keys.TAB)
              parent_element = email.find_element(By.XPATH, '..')
              attributes = parent_element.get_attribute('aria-invalid')
              # if attributes == "false":
              break
              email.clear()
       

       password = driver.find_element(By.ID, 'password1')
       password.send_keys(random_char(8))
       password.send_keys(Keys.TAB)

       wait = WebDriverWait(driver, 10)
       disabled = driver.find_element(By.CSS_SELECTOR,'.UIButton.UIButton--fill[type="submit"]')

       if not disabled.get_attribute("disabled") and disabled.is_enabled() and disabled.is_displayed():
              disabled.click()
       else:
              print("Button is disabled.")
       #Signup complete

def parent_login():
       parent_email = driver.find_element(By.ID, 'parent_email')
       parent_email.send_keys(random_char(5)+"@gmail.com")
       parent_password = driver.find_element(By.ID, 'parent_password')
       parent_password.send_keys(random_char(8))

       wait = WebDriverWait(driver, 10)
       disabled = driver.find_element(By.CSS_SELECTOR, "button[class='AssemblyButtonBase AssemblyPrimaryButton--default AssemblyButtonBase--medium AssemblyButtonBase--padding'][aria-label='Sign up']")


       if not disabled.get_attribute("disabled") and disabled.is_enabled() and disabled.is_displayed():
              disabled.click()


if __name__ == "__main__":
       login()
       parent_login()
       clipboard = ''
       lastq = ''
       flag = 0

       while(True):
              if "https://quizlet.com/explanations/textbook-solutions" not in clipboard:
                     outf = os.popen('pbpaste','r')
                     clipboard = outf.read()
                     time.sleep(5)
                     continue

              if flag == 0: #First URL
                     flag = 1      #Not the first question anymore
                     lastq = clipboard
                     #driver.get(clipboard)
                     continue
              
              if os.popen('pbpaste','r').read() == lastq:
                     time.sleep(5*60)
              else:   #Keeps pinging to alert user
                     for i in range(5):
                            print('\a')
                            time.sleep(1)
                     yesORno = input("Press Enter to open new question")  #By this time the clipboard should have changed.
                     driver.get(clipboard)