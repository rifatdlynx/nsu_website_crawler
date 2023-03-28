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


### Editing Dataframes of list
# Converting the list to dataframe
links_df = pd.DataFrame(links)
print(links_df.head(2))

# Naming the column
links_df.columns = ['links']
print(links_df.head(2))

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


### Editing the lists of links
# Internal link and External Link seperated into their own list
internal_link_list = []
external_link_list = []

for item in links:
  if "http" in item:
    external_link_list.append(item)
  elif "#" in item:
    continue
  elif "pdf" in item:
    continue
  else:
    internal_link_list.append(item)

# Adding Http to intenal links 
internal_link_list_full = []
for item in internal_link_list:
  temp = "http://www.northsouth.edu/" + item
  internal_link_list_full.append(temp)

print(len(internal_link_list_full))
print(internal_link_list_full)

# Getting links from the links in internal links list
for item in internal_link_list_full:
  print("Accessing URL -------------------------- " + item)
  read_url = urlopen(item)
  nsu_data = soup(read_url.read())
  for link in nsu_data.find_all('a'):
    if 'href' in link.attrs:
      temp = link.attrs['href']
      print("Link Found - " + temp)
      if "http" in temp:
        continue
      elif "#" in temp:
        continue
      elif "pdf" in temp:
        continue
      elif "//" in temp:
        continue
      elif "gmail" in temp:
        continue
      elif ".com" in temp:
        continue
      elif temp in internal_link_list_full:
        continue
      else:
        temp = "http://www.northsouth.edu/" + temp
        print("Appending Link ----- " + temp)
        internal_link_list_full.append(temp)

print(len(internal_link_list_full))



### For getting the data in the list
for data in nsu(['style', 'script', 'a']):
  # Remove tags
  data.decompose()

data = nsu.get_text()
data.replace("\n", " ")

website_data = pd.DataFrame({'address': ['http://www.northsouth.edu/'],
                             'data': [data]})
#website_data[data].replace("\n"," ")
print(website_data)