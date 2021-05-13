import requests
from bs4 import BeautifulSoup
import csv

output_file = csv.writer(open('prem_matches.csv', 'w'))

output_file.writerow(['Date', 'HomeTeam', 'AwayTeam'])

url = "https://www.fotmob.com/leagues/47/matches/premier-league" 
# html = urlopen(url)
# soup = BeautifulSoup(html, 'html.parser')
date_time=[]
team_home=[]
team_away=[]
result = requests.get(url)
src = result.content
# set a new BeautifulSoup HTML parser variable called “soup” that uses the “src” contents
soup = BeautifulSoup(src, 'html.parser')

def pick_tags(tag):
    if tag.name == "span":
        classes = tag.get("class", [])
        return lambda x: 'css-hekth7-MatchCSS' in x.split()
    # if tag.name == "a":
    #     classes = tag.get("class", [])
    #     return lambda x: 'css-be2o5n-TLMatchCSS e1nlzfsz0' in x.split()
full=soup.find_all(pick_tags)
print(full)
full=full[7:]
# tag_span=full.span
# tag_span['']
for i, row in enumerate(full):
    if i%4 == 1:
        team_home=row.get_text()
    elif i%4 == 2:
        date_time=row.get_text()
    elif i%4 == 3:
        team_away=row.get_text()
    output_file.writerow([date_time, team_home, team_away])
    
# print(len(full))
# elements = [x.get_text() for x in full]
# text = ",".join(elements)
# print(text)


# # create a new Firefox session
# path = '/Users/wingyanma/Documents/others/chromedriver' #introduce your file's path inside '...'

# driver = webdriver.Chrome(path)
# driver.get(url)
# time.sleep(5) #w ait for 5 seconds for loading time

# # elem = driver.find_element_by_link_text("MATCHES") #  find the link with MATCHES as text
# # elem.click() # click that button
# # time.sleep(5) # wait for 5 seconds for loading time

# matchesall = driver.find_elements_by_xpath("//*[@class='fm-fixture__team__name']") # grab all instances of fm-fixture__team__name elements
# table = soup.find_all("table")

# teamlist = [] # create empty list
# for i in matchesall: # for loop for every element found by fm-fixture__team__name
#     teamlist.append(i.text) # append to new list the name of the team

# cleanteamlist = [] # create another empty list
# for x,y in zip(teamlist[0::2], teamlist[1::2]): # since they are in pairs take every two elements
#     cleanteamlist.append(str(x) +":" + str(y)) # append them to another clean list 
    
# print(cleanteamlist) # print results

# driver.close() # close driver