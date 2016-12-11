from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.set_window_size(1024,900)
driver.get('https://badoo.com/')


Main_window = driver.window_handles[0]

LoginButtonID = driver.find_element_by_xpath('//*[@id="homepage-header"]/div/div[2]/div/div/div[1]/a')
LoginButtonID.click()

Popup_window = driver.window_handles[1]
driver.switch_to_window(Popup_window)

EmailID = driver.find_element_by_id('email')
PasswordID = driver.find_element_by_id('pass')
LoginPopupID = driver.find_element_by_id('u_0_2')

EmailID.clear()
PasswordID.clear()
EmailID.send_keys("brianformento@hotmail.co.uk")
PasswordID.send_keys("")
LoginPopupID.click()

driver.switch_to_window(Main_window)
time.sleep(10)

driver.refresh()
driver.back()

App = driver.find_element_by_id('app_c')

var = 1
while var == 1:

	App.send_keys(Keys.NUMPAD1)


'''
People_nearby = driver.find_element_by_id('js-sidebar-search-link')
People_nearby.click()

second_page = driver.find_element_by_xpath('/html/body/div[2]/div[1]/main/section/div[2]/div[3]/a')
second_page.click()
'''
'''
var = 1
while var == 1:
	Yes_vote = driver.find_element_by_xpath('/html/body/div[2]/div[1]/main/div/div/header/div/div[1]')
	Yes_vote.click
#Popup1 = find_element_by_xpath('/x:html/x:body/x:div[8]/x:div[1]/x:div[1]/x:div/x:div[3]/x:i')
#Popup1.click()
'''



'''

Like = driver_find_element_by_xpath('//*[@id="mm_cc"]/div/header/div/div[1]/div[1]/span')
Like.click()



''''''
element = driver.find_element_by_xpath('//*[@id="lst-ib"]')
element.send_keys('Facebook')
element.send_keys(Keys.ENTER)

login_time = driver.find_elements_by_link_text('Facebook - Log In or Sign Up')
login_time.click()
'''
