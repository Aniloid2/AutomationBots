from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

username = ""
password = ""

def wait_load(driver,parameter):
	element = WebDriverWait(driver, 30).until(
       EC.presence_of_element_located((By.XPATH, parameter))
       )
	pass # if its stuck might want to return to upload screen and reproduce th last action

def get_redbubble(driver):

	driver.set_window_size(1290,900)
	driver.get('https://www.redbubble.com/auth/login?next_action=%2F')

	wait_load(driver, '//*[@id="login-username"]')
	UsernameID = driver.find_element_by_id('login-username')
	PasswordID = driver.find_element_by_id('login-password')
	Login_button = driver.find_element_by_id('login-submit')

	UsernameID.send_keys(username)
	PasswordID.send_keys(password)
	Login_button.click()


def upload_image(driver,counter, counter_list, list_poke):
	print counter , ' uploading: ', counter_list[counter] , ' || ' , list_poke[counter]
	driver.get('http://www.redbubble.com/portfolio/images/new?ref=account-nav-dropdown')
	wait_load(driver, '//*[@id="select-image-single"]')
	time.sleep(1)

	#### upload_image ## 

	image = driver.find_element_by_xpath('//*[@id="select-image-single"]')
	image.send_keys(r'C:\Users\Brian\Desktop\BUSINESS\Empire_fort\PokemonBot\Pokepics\BigPictures\\'+counter_list[counter]+'.png')

def enter_details(driver, counter, list_poke):
	pokemon = list_poke[counter][:-1]
	
	wait_load(driver, '//*[@id="work_title"]')
	TitleID = driver.find_element_by_xpath('//*[@id="work_title"]')

	wait_load(driver, '//*[@id="work_description_en"]')
	DescriptionID = driver.find_element_by_xpath('//*[@id="work_description_en"]')
	
	wait_load(driver, '//*[@id="work_tag_field_en"]')
	TagsID = driver.find_element_by_xpath('//*[@id="work_tag_field_en"]')
	
	TitleID.send_keys(pokemon, ' pokemon sticker' )
	DescriptionID.send_keys('Pokemon Go is now out get ',pokemon, ' sticker now! to attach on your computer, phone or tablet.')
	TagsID.send_keys(pokemon ,','+'Pokemon,' + 'sticker,'+'pokemon go')
	
	print '# Entered Description, title and tags -- sleep 2 seconds'
	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[29]/div/div[3]/img[1]')
	#-----------------check boxes -------------------------#
	time.sleep(14)

	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[9]/div[2]/div[4]/div[2]/div[3]')
	PhoneCaseseSkins = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[9]/div[2]/div[4]/div[2]/div[3]').click()
	
	### add kids clothes###
	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[1]/div[1]/div[4]/div[2]/div[1]')
	Clothing_edit_box = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[1]/div[1]/div[4]/div[2]/div[1]').click()
	time.sleep(1)
	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[2]/div[1]/div[4]/div/div[2]/label/i')
	check_box_clothes = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[2]/div[1]/div[4]/div/div[2]/label/i').click()
	time.sleep(1)
	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[2]/div[1]/div[4]/div/div[2]/div/div/ul/li[8]/div[1]/a[2]/i')
	check_kids_clothes = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[2]/div[1]/div[4]/div/div[2]/div/div/ul/li[8]/div[1]/a[2]/i').click()
	time.sleep(1)
	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[2]/div[1]/div[4]/div/div[3]/button')
	apply_changes_clothes = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[2]/div[1]/div[4]/div/div[3]/button').click()
	time.sleep(1)



	#wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[13]/div[2]/div[4]/div[2]/div[1]')
	#Pillows_edit_box = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[13]/div[2]/div[4]/div[2]/div[1]')

	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[17]/div[2]/div[4]/div[2]/div[3]')
	Mugs_disable_box = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[17]/div[2]/div[4]/div[2]/div[3]').click()

	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[21]/div[2]/div[4]/div[2]/div[3]')
	Mini_skirt_disable_box = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[21]/div[2]/div[4]/div[2]/div[3]').click()

	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[25]/div[1]/div[4]/div[2]/div[3]')
	Table_cases_Disable_box = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[25]/div[1]/div[4]/div[2]/div[3]').click()

	wait_load(driver, '//*[@id="add-new-work"]/section[1]/div/div[25]/div[3]/div[4]/div[2]/div[3]')
	Spiral_note_book_daible_box = driver.find_element_by_xpath('//*[@id="add-new-work"]/section[1]/div/div[25]/div[3]/div[4]/div[2]/div[3]').click()

	wait_load(driver, '//*[@id="media_design"]')
	Design_illustration_box = driver.find_element_by_xpath('//*[@id="media_design"]').click()

	wait_load(driver,'//*[@id="media_digital"]')
	Digital_art_box = driver.find_element_by_xpath('//*[@id="media_digital"]').click()
	
	wait_load(driver,'//*[@id="work_group_ids_558262"]')
	Pokemon_go_box = driver.find_element_by_xpath('//*[@id="work_group_ids_558262"]').click()
	
	wait_load(driver,'//*[@id="work_default_product"]')
	dropdown = Select(driver.find_element_by_xpath('//*[@id="work_default_product"]'))
	dropdown.select_by_value('sticker')
	
	wait_load(driver,'//*[@id="work_safe_for_work_true"]')
	Mature_content_box = driver.find_element_by_xpath('//*[@id="work_safe_for_work_true"]').click()
	print '# clicked all checkboxes -- wait 2 seconds'
	time.sleep(3)

	save_workID = driver.find_element_by_id('submit-work').click()
	wait_load(driver, '//*[@id="add-to-cart"]/span')
	print '# Image uploaded'



def get_names(list_poke):
	poke = open("Pokenames.txt", "r" )

	for line in poke:
		print line
		list_poke.append(line)
	return list_poke

def make_counter(counter, counter_list,list_poke):
	counter = counter + 287  # update if it stops, delete pictures, and names
	for lis in list_poke:
		three_dig_counter = str(counter).zfill(3)
		print three_dig_counter
		counter_list.append(three_dig_counter)
		counter = counter +1

	return counter_list

#chrome_path = r"C:\Program Files (x86)\Google\Chromedriver_win32\chromedriver.exe"

##create driver instance
driver = webdriver.PhantomJS()

## read all pokemon names and create a list
list_poke = []
list_poke = get_names(list_poke)

#create the counter numbers and fill a list with 000+1 to attach to driver.get(http://assets.pokemon.com/assets/cms2/img/pokedex/full/number.png) 
counter = 0
counter_list= []
counter_list = make_counter(counter, counter_list,list_poke)

### login to redbubble
get_redbubble(driver)

for line in list_poke:
	upload_image(driver, counter, counter_list, list_poke)
	enter_details(driver, counter, list_poke)
	counter = counter +1




#TitleID = driver.find_element_by_id('work_title')




