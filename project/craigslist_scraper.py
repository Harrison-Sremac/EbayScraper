import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define Craigslist search URL (Modify based on your city)
BASE_URL = "https://ithaca.craigslist.org/search/sss?query=speaker&sort=date#search=2~list~0"

# Send HTTP request to Craigslist
response = requests.get(BASE_URL)
if response.status_code != 200:
    print("Error fetching page")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all listings
listings = soup.find_all('li', class_='result-row')

# Extract data from each listing
data = []
for listing in listings:
    title = listing.find('a', class_='result-title').text
    price_tag = listing.find('span', class_='result-price')
    price = price_tag.text if price_tag else "N/A"
    link = listing.find('a', class_='result-title')['href']
    
    data.append({"Title": title, "Price": price, "URL": link})

# Convert to Pandas DataFrame
df = pd.DataFrame(data)

# Display results
print(df)
df.to_csv("craigslist_listings.csv", index=False)
print("Data saved to craigslist_listings.csv")
    