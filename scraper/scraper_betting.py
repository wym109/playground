from selenium import webdriver
import time

web = 'https://sports.tipico.de/en/top-competitions/1101/1201/1301' #you can choose any other league
path = '/Users/wingyanma/Documents/others/chromedriver' #introduce your file's path inside '...'

driver = webdriver.Chrome(path)
driver.get(web)

time.sleep(5) #add implicit wait, if necessary
accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
accept.click()

teams = []
x12 = [] #3-way
odds_events = []

#select only upcoming matches box
box = driver.find_element_by_xpath('//div[contains(@testid, "Program_SELECTION")]')

sport_title = box.find_elements_by_class_name('SportTitle-styles-sport')

for sport in sport_title:
    # selecting only football
    if sport.text == 'Football':
        parent = sport.find_element_by_xpath('./..')
        grandparent = parent.find_element_by_xpath('./..')