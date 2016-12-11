from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import urlparse, random
import argparse,os
key = "badoo.com"
driver = webdriver.PhantomJS()

driver.set_window_size(1280,800)
driver.get('https://badoo.com/')


Main_window = driver.window_handles[0]
LoginButtonID = driver.find_element_by_xpath('//*[@id="homepage-header"]/div/div[2]/div/div/div[1]/a')
LoginButtonID.click()
print 'Arrived at BADOO.com'
Popup_window = driver.window_handles[1]
driver.switch_to_window(Popup_window)
print 'Login with facebook...'



EmailID = driver.find_element_by_id('email')
PasswordID = driver.find_element_by_id('pass')
LoginPopupID = driver.find_element_by_id('u_0_2')
print 'Facebook parameters entered...'
EmailID.clear()
PasswordID.clear()
EmailID.send_keys('brianformento@hotmail.co.uk')
PasswordID.send_keys('')
LoginPopupID.click()
print 'Facebook Authorized...'
driver.switch_to_window(Main_window)
time.sleep(5)
print "###login Successful###"

driver.refresh()
driver.back()

App = driver.find_element_by_id('app_c')
var = 0
time.sleep(5)
page = BeautifulSoup(driver.page_source,"html.parser")

print 'brute force enabled...'
while var < 15:
	url = driver.page_source
	page = BeautifulSoup(url, "html.parser")
	headis = page.h1
	time.sleep(0.5)
	#a = headis.span
	#in_html =  a.contents
	#time.sleep(0.5)
	### detect popup nad refresh
	if page.findAll('i', {'class',('icon icon--white js-ovl-close')}) in page:
		print 'ALUUHABARR'
	#under_h1 = page.findAll("span",{'class': 'flex__item flex__item--dynamic ellipsis'})
	#print under_h1

	place = 0
	for all_in_header in headis.findAll('span'):
		if place == 0:
			name = all_in_header.text
		if place == 1:
			age = all_in_header.text
		place +=1

	print 'likeing:', name, 'Age:', age
	App.send_keys(Keys.NUMPAD1)
	var +=1
	if var == 14:
		driver.quit()
		var = 0



''' to get a content in position after header i use a LoginPopupID
should be a better way, but didnt find it, probs with contents[1]''' 



		#for span in all_span_elements.findAll('span'):
			#print span
			#driver.quit()

print "END"
driver.quit()
'''
	print driver.current_url, 'likeing:'
	App.send_keys(Keys.NUMPAD1)
	var+=1
	if var == 9:
		driver.refresh()

print driver.current_url + "alukabar"
#driver.quit()
'''