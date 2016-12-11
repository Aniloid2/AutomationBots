from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import argparse,os
import urlparse, random

key = "badoo.com"
driver = webdriver.Firefox()

driver.set_window_size(1280,800)
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
EmailID.send_keys('brianformento@hotmail.co.uk')
PasswordID.send_keys('')
LoginPopupID.click()

driver.switch_to_window(Main_window)
time.sleep(10)

driver.refresh()
driver.back()

time.sleep(7)

Find_people = driver.find_element_by_id('js-sidebar-search-link')
Find_people.click()



time.sleep(7)



page = BeautifulSoup(driver.page_source, "html.parser")




print "----------------------------------"
links = []
page_ids = []

var = 1
page_counter = 1

while var ==1 :

	del page_ids[:]
	page_counter = 1
	while page_counter < 7 :

		if page_counter == 1:
			for a_from_people_nb in page.findAll('a'):
				href = a_from_people_nb.get('href')
				if "/search?page=" in href:
					print "updating page list..."
					page_ids.append(href)
		for a_from_people_nb in page.findAll('a'):
					href = a_from_people_nb.get('href')
					if "/profile/" in href:
						if "from_search" in href:
							print "updating profile list..."
							links.append(href)

		for link in links:
			driver.get(key + link)
			time.sleep(random.uniform(15,20))
			print key + link

		del links[:]

		next_page = page_ids[page_counter]
		print "Im printing this" + next_page
		page_counter = page_counter + 1
		driver.get(key + next_page)
		print key + next_page
	


		print "finished"
		time.sleep(3)
		page = BeautifulSoup(driver.page_source, "html.parser")




#links []
#for link in page.findAll('a'):
#	url = link.get('href')
#	print link.get('href')


	#head = page.contents[0].contents[1]
	#print head





booton = browser.find_element_by_xpath('//*[@id="selenium.webdriver.remote.webdriver.WebDriver.find_element_by_xpath"]/a')



