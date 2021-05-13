from selenium import webdriver
import time
import pandas as pd

# web = 'https://sports.tipico.de/en/top-competitions/1101/1201/1301' #you can choose any other league
web = 'https://sports.tipico.de/en/all/football/england/premier-league'
path = '/Users/wingyanma/Documents/others/chromedriver' #introduce your file's path inside '...'

driver = webdriver.Chrome(path)
driver.get(web)

time.sleep(2) #add implicit wait, if necessary
accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
accept.click()

date_time = []
teams = []
x12 = [] #3-way
over_under = []
# odds_events = []
#select only upcoming matches box
# box = driver.find_element_by_xpath('//div[contains(@testid, "Program_SELECTION")]') #update 3

sport_title = driver.find_elements_by_class_name('SportTitle-styles-sport')

for sport in sport_title:
    # selecting only football
    if sport.text == 'Football':
        parent = sport.find_element_by_xpath('./..')
        grandparent = parent.find_element_by_xpath('./..')

        #Single row event
        single_row_events = grandparent.find_elements_by_class_name('EventRow-styles-event-row')
    # print(len(single_row_events))
    for count, match in enumerate(single_row_events):
        odds_event = match.find_elements_by_class_name('EventOddGroup-styles-odd-groups')
        # odds_events.append(odds_event)

        # date_time
        date_time.append(match.find_element_by_xpath('//*[@id="app"]/main/main/section/div/div/div/div/div/a[%s]/div[1]/div'%(count+1)).text)
        # teams
        for team in match.find_elements_by_class_name('EventTeams-styles-titles'):
            teams.append(team.text)

        # for odds_event in odds_events:
        for n, box in enumerate(odds_event):
            rows = box.find_elements_by_xpath('.//*')
            if n == 0:
                x12.append(rows[0].text)
            elif n == 1:
                over_under.append(rows[0].text)
driver.quit()
team_home=[]
team_away=[]
odd_home=[]
odd_draw=[]
odd_away=[]
odd_over=[]
odd_under=[]
for i in teams:
    team_home.append(i.split("\n")[0])
    team_away.append(i.split("\n")[1])
for j in x12:
    odd_home.append(j.split("\n")[0])
    odd_draw.append(j.split("\n")[1])  
    odd_away.append(j.split("\n")[2])
for k in over_under:
    odd_over.append(k.split("\n")[0])
    odd_under.append(k.split("\n")[1])  
df = pd.DataFrame({
    'date_time': date_time,
    'team_home': team_home,
    'team_away': team_away,
    'odd_home': odd_home,
    'odd_draw': odd_draw,
    'odd_away': odd_away,
    'odd_over': odd_over,
    'odd_under': odd_under,    
    # 'Teams': teams,
    # '1x2': x12,
    # 'over_under': over_under
    })
print(df)

