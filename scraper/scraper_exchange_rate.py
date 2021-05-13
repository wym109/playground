from bs4 import BeautifulSoup
import urllib2

url = "http://bog.gov.gh/data/bankindrate.php"
page = urllib2.urlopen(url)

soup = BeautifulSoup(page.read())

td = soup.find_all('td')

another_soup = BeautifulSoup(td[:-3])

print another_soup

currencies = {}
trs = soup.find_all('tr') # find rows
for tr in trs[1:-3]: # skip first and last 3 (or whatever)
    text = list(tr.strings) # content of all text stuff in tr (works in this case)
    # [u'U.S Dollar', u'USDGHS', u'1.8673', u'1.8994']
    currencies[text[1]] = [float(text[2]), float(text[3])]