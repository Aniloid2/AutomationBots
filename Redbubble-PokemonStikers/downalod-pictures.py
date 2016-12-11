from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import urllib

counter = 0
counter_list = []

def make_counter(counter, counter_list):
	counter = counter + 1
	while counter <= 720:
		three_dig_counter = str(counter).zfill(3)
		print three_dig_counter
		counter_list.append(three_dig_counter)
		counter = counter +1

	return counter_list

counter_list = make_counter(counter, counter_list)
print counter_list
#-----------------------------------------------------------------------------------------------#



def determine_poke_to_download(counter):
	while counter <=720:
		poke_number= counter_list[counter]
		picture = 'http://assets.pokemon.com/assets/cms2/img/pokedex/full/'+poke_number+'.png'
		urllib.urlretrieve(picture, poke_number+".png")
		counter = counter+1
		print 'done'





driver = webdriver.Chrome()

driver.set_window_size(1024,900)

determine_poke_to_download(counter)




