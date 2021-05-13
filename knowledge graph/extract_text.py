import requests 
from bs4 import BeautifulSoup as bs 

INPUTURL="https://www.hsbc.co.uk/wealth/articles/what-is-a-stocks-and-shares-isa/"
TXTFILE="sample_isa.txt"


# Load page content
r = requests.get(INPUTURL)

# Convert to a beautiful soup object
page = bs(r.content,'html.parser')

# Print out our html
# print(page.prettify())

def pick_tags(tag):
    if tag.name == "h3":
        classes = tag.get("class", [])
        return lambda x: 'heading A-TYP28L-RW-ALL' in x.split()
    elif tag.name == "p":
        classes = tag.get("class", [])
        return lambda x: 'A-PAR16R-RW-ALL' in x.split()
#         return "A-PAR16R-RW-ALL" in classes 

# full=page.find_all(pick_tags)

body = page.select("p.A-PAR16R-RW-ALL")

elements = [x.get_text() for x in body]
text = "\n".join(elements)
# print(text)

# Write text to output
file = open(TXTFILE, "wt")
n = file.write(text)
file.close()
