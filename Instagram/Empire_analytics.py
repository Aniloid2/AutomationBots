from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import argparse,os
import urlparse, random
import xlsxwriter
from matplotlib import pyplot as plt

driver = webdriver.Firefox()
print 'Opening PhantomJS...'
driver.set_window_size(1280,800)
driver.get('https://www.instagram.com/')
time.sleep(1)
Login_front = driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[2]/p/a')
Login_front.click()
time.sleep(2)

print 'Logging in Instagram...'

LoginID = driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[1]/div/form/span/button')
UsernameID = driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[1]/div/form/div[1]/input')
PasswordID = driver.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[1]/div/form/div[2]/input')
UsernameID.send_keys('braianforms')
PasswordID.send_keys('Valencyband')
LoginID.click()
time.sleep(2)

Search_static = driver.find_element_by_xpath('/html/body/span/section/nav/div/div/div/div[1]/div/div/span[2]')
Search_static.click()

Search_after_click = driver.find_element_by_xpath('/html/body/span/section/nav/div/div/div/div[1]/input')
Search_after_click.send_keys('empire.fort')
time.sleep(2)
empirefort = driver.find_element_by_xpath('/html/body/span/section/nav/div/div/div/div[1]/div[2]/div[2]/div/a[1]/div/div[1]/span')
empirefort.click()

# we accessed the empirefort page through braianforms, in the ugliest way possible
time.sleep(2)
page = BeautifulSoup(driver.page_source, "html.parser")
print 'Found empre.fort...'
List_folowers = []

for spans in page.findAll('span'):

	title_1_0 = spans.get('title')

	if title_1_0  != None:
		folowers = str (title_1_0)
		List_folowers.append(folowers)
		print folowers

print 'Recived folowers at: '+ folowers 
### Above gets logged into instagram to get follower value
### returned as a string




#####################FILE OPENER#################



###belowe it appends value in a text file
### open the file
print 'Updating database folower file...'
file_folower_nom = open('Graphx.txt','a')
number=[]
### get rif of the thousend comma
for N in folowers:
	if N != ',':
		number.append(N)

###join everithing together
folowers_nocoma = ''.join(number)

Append_folowers = folowers_nocoma + '\n'

file_folower_nom.write(Append_folowers)
file_folower_nom.close()

###Now Detect the number of lines for time axis. 
###declere list of all values found in file
num = 1
list_of_fol_value_y = []
list_time_x = []
num_lines=sum(1 for line in open('Graphx.txt'))

print 'Gatering folowers over time'
###open file
file_to_plot = open('Graphx.txt','r')
while num <= num_lines:
	list_time_x.append(num)
	num +=1
### append the value found in .txt file into an array
num = 0
while num < num_lines :
	yarg = file_to_plot.readline()
	list_of_fol_value_y.append(yarg)
	num += 1



print 'Plotting...\n\n\n\n'
plt.plot(list_time_x,list_of_fol_value_y)

plt.show()

print list_of_fol_value_y
print 'Number of folows recorded:' , num_lines
file_to_plot.close()

### actualy add a timed x axis
