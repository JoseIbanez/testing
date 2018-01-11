# To install the Python client library:
# pip install -U selenium

# Import the Selenium 2 namespace (aka "webdriver")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
import time

# for fresh FF profile
profile = webdriver.FirefoxProfile() 
#profile_path="/path/to/custom/profile/"
#profile = webdriver.FirefoxProfile(profile_path)
# set FF preference to socks proxy
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 8888)
profile.set_preference("network.proxy.socks_version", 5)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile)

driver.get("https://10.108.8.89/ccmadmin/showHome.do")
#print driver.page_source
# sleep if want to show in gui mode. we do print it in cmd
time.sleep(5)

# Enter some text!
text_area = driver.find_element_by_name('j_username')
text_area.send_keys("Admin")
text_area = driver.find_element_by_name('j_password')
text_area.send_keys("T0rtill4")
time.sleep(5)
text_area.submit()

time.sleep(25)


driver.close()
driver.quit()