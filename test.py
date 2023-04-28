import requests
from bs4 import BeautifulSoup

num = int(BeautifulSoup(requests.get(url = 'https://bewell.ese.syr.edu/FacilityOccupancy').text, "html.parser").find_all("strong")[2].contents[0].strip("%"))

print(num)


