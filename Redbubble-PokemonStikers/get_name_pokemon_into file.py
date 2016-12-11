from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import urllib



counter = 0
counter_list = []
#driver = webdriver.Chrome()
#driver.set_window_size(1024,900)



#driver.get('http://www.pokemon.com/us/pokedex/001')
#the_url_sting = driver.current_url

#print the_url_sting
#array_lastelement_pokemon = the_url_sting.split("/")
#print array_lastelement_pokemon
#name_of_pokemon = array_lastelement_pokemon[-1]
#print name_of_pokemon


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

driver = webdriver.PhantomJS()
driver.set_window_size(1024,900)

for pokemon_number in counter_list:
	driver.get('http://www.pokemon.com/us/pokedex/'+pokemon_number)
	the_url_sting = driver.current_url
	print the_url_sting
	array_lastelement_pokemon = the_url_sting.split("/")
	name_of_pokemon = array_lastelement_pokemon[-1]
	print name_of_pokemon
	with open("Pokenames.txt", "a") as pokenames:
		pokenames.write(name_of_pokemon+"\n")