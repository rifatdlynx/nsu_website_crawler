from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd

url = urlopen("http://www.northsouth.edu/")
nsu = soup(url.read())
#Examples of how to find by tag
#links = nsu.find_all('a')
#scripts = nsu.find_all('script')

# A list for all the links in homepage
links = []

# Appending all the links in the list
for link in nsu.find_all('a'):
  if 'href' in link.attrs:
    links.append((link.attrs['href']))

# Converting the list to dataframe
links_df = pd.DataFrame(links)

# Naming the column
links_df.columns = ['links']

# Removing empty links from the dataframe
links_df = links_df[links_df["links"].str.contains("#") == False]

# Removing external links from the data frame
internal_links = links_df[links_df["links"].str.contains("http") == False]

# Adding Https infront of all the addresses
internal_links['links'] = 'http://www.northsouth.edu/' + internal_links['links'].astype(str)

# Creating new dataframe for external links
external_links = links_df[links_df["links"].str.contains("http") == True]

print("Links")
print(links_df.head(2))
print("Internal Links")
print(internal_links.head(2))
print("External Links")
print(external_links.head(2))



for data in nsu(['style', 'script', 'a']):
  # Remove tags
  data.decompose()

data = nsu.get_text()
data.replace("\n", " ")