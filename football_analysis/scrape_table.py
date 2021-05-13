import requests
from bs4 import BeautifulSoup
import csv
output_file = csv.writer(open('prem_table_bs.csv', 'w'))

output_file.writerow(['Position', 'Team', 'Played', 
					  'Won', 'Drawn', 'Lost', 
					  'For', 'Against', 'GD', 'Points'])

result = requests.get("https://www.bbc.co.uk/sport/football/tables")
src = result.content
# set a new BeautifulSoup HTML parser variable called “soup” that uses the “src” contents
soup = BeautifulSoup(src, 'html.parser')

# selecting the <table> HTML element, extracting the <tr> (table rows) and then gathering each <td> (table data) from each row
table = soup.find_all("table")
league_table = table[0]

teams = league_table.find_all("tr")

for team in teams[1:21]:

    stats = team.find_all("td")

    position = stats[0].text
    team_name = stats[2].text
    played = stats[3].text
    won = stats[4].text
    drawn = stats[5].text
    lost = stats[6].text
    for_goals = stats[7].text
    against_goals = stats[8].text
    goal_diff = stats[9].text
    points = stats[10].text
    
    output_file.writerow([position, team_name, played, 
    					  won, drawn, lost, 
    					  for_goals, against_goals, goal_diff, points])

