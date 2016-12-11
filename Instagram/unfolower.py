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


Username = 'empire.fort'
Password = 'testing6'


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
	wait_load(driver, '//*[@id="react-root"]/section/nav/div/div/div/div[2]/div[3]/a')
	driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[2]/div[3]/a').click()

	wait_load(driver, '//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a')
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a').click()

	pass

def wait_load(driver,parameter):
	element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.XPATH, parameter))
       )
	pass

def unflow(driver):
	wait_load(driver, '/html/body/div[2]/div/div[2]/div/div[2]/ul/li[1]/div/div[2]/span/button')
	i = 1
	while i < 6:
		driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li['+ str(i) +']/div/div[2]/span/button').click()
		time.sleep(3)
		i +=1
	driver.refresh()
	wait_load(driver, '//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a')
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a').click()
	print 'done'


driver = webdriver.Chrome()

get_instagram(driver)
l = 0
while l < 100:
	unflow(driver)
