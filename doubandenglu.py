from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
#driver.get("https://www.douban.com")
driver.get("https://accounts.douban.com/login?alias=")

driver.find_element_by_name("form_email").send_keys("15*******")
driver.find_element_by_name("form_password").send_keys("********")

#driver.find_element_by_xpath("//input[@class='bn-submit']").click()

driver.find_element_by_xpath("//input[@type='submit']").click()


#driver.save_screenshot("douban.png")

#driver.quit()