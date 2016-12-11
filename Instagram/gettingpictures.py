from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import argparse,os,sys
import urlparse, random
import xlsxwriter
from matplotlib import pyplot as plt
import urllib

ids_from_wall_counter = []
picture_scr_to_visit = []

Username = 'jcockblocker'
Password = 'Thisismypassword'

# always place counter addition at end of loop (Y)

def get_instagram(driver):
	driver.set_window_size(1280,800)
	driver.get('https://www.instagram.com/')
	wait_load(driver, '/html/body/span/section/main/article/div[2]/div[2]/p/a')
	driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[2]/p/a').click() # Get to login
	wait_load(driver, '/html/body/span/section/main/article/div[2]/div[1]/div/form/div[1]/input')
	print 'Logging in Instagram...'

	UsernameID = driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[1]/div/form/div[1]/input')
	PasswordID = driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[1]/div/form/div[2]/input')
	UsernameID.send_keys(Username)
	PasswordID.send_keys(Password)
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button').click() #Login Button
	print 'Waiting on instagram wall...'

	wait_load(driver, '//*[@id="react-root"]/section/nav/div/div/div/div[1]/div/div/span[2]')
	page = BeautifulSoup(driver.page_source, "html.parser")
	detect_image(page, ids_from_wall_counter)


	number_of_pictures_already = len(ids_from_wall_counter) #get how many pictures are on initial wall, to set counter
	#print number_of_pictures_already

	#print 'In user wall'
	return number_of_pictures_already;

def detect_image(page, lis):
	for img in page.findAll('img'):
		id_main_page_pic = img.get('src')
		id_of_img = img.get('id')
		if id_of_img == None:
			print 'Profile picture detected: Not interested --> igonore'
		else:
			print 'This is the id: '+ str(id_of_img)
			lis.append(id_main_page_pic)

def download(num):
	for all_items_in_ids in picture_scr_to_visit:
		urllib.urlretrieve(all_items_in_ids, 'pImage_' + str(num) +".jpg")
		num +=1
	return num;

def wait_load(driver,parameter):
	element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.XPATH, parameter))
       )
	pass

def search(driver, Page_to_scrape):
	driver.get(Page_to_scrape)
	time.sleep(4)
	'''driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[1]/div/div/span[2]').click() #Search bar click
	wait_load(driver, '//*[@id="react-root"]/section/nav/div/div/div/div[1]/input')
	driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[1]/input').clear()
	driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[1]/input').send_keys(Page_to_scrape) #Search bar Enter keys
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[1]/div[2]/div[2]/div/a[1]').click() # Click on first item
	print 'waiting...'
	time.sleep(4)'''
	pass


def scrap(driver,name,counter):
	search(driver, name)
	page = BeautifulSoup(driver.page_source, "html.parser")
	detect_image(page,picture_scr_to_visit)
	for l in picture_scr_to_visit:
		print 'Pictures download:' + l
	counter = download(counter)
	print counter
	del picture_scr_to_visit[:]
	return counter;




############################################MAIN######################################################
driver = webdriver.Chrome()
print 'Opening chrome...'
counter = get_instagram(driver)
infinity = 1
while infinity == 1:
	name = raw_input('# Enter Instagram name to download some pictures from: ')
	Page_to_scrape = 'https://www.instagram.com/'+name +'/'
	counter = scrap(driver,Page_to_scrape,counter)
	print '# Finished downloadind some pictures'
	again = raw_input('Would you like to download from another page? [y/n] :')
	if again == 'n':
		driver.quit()
		sys.exit()
######################################################################################################