import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

item = 'speaker'
# Craigslist search URL 
SEARCH_URL = "https://ithaca.craigslist.org/search/sss?query=" + item

# Send request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(SEARCH_URL, headers=headers)
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the script tag containing JSON-LD data
script_tag = soup.find("script", {"id": "ld_searchpage_results"})

if not script_tag:
    print("Could not find JSON data in the Craigslist page please try again.")
    exit()

# Extract and parse the JSON data
json_data = json.loads(script_tag.string)

# Extract 
listings = json_data.get("itemListElement", [])

data = []
for listing in listings:
    item = listing.get("item", {})
    title = item.get("name", "No title")
    price = item.get("offers", {}).get("price", "N/A")
    url = item.get("offers", {}).get("availableAtOrFrom", {}).get("@type", "N/A")
    location = item.get("offers", {}).get("availableAtOrFrom", {}).get("address", {}).get("addressLocality", "Unknown")
    
    # Extract item URL from href
    listing_url  = listing.get("item", {}).get("offers", {}).get("url", "No URL")

    
    data.append({"Title": title, "Price": f"${price}", "Location": location, "URL": listing_url})

# Convert to Pandas DataFrame
df = pd.DataFrame(data)

# Display or save the data
print(df)  # Print listings to console
df.to_csv("craigslist_listings.csv", index=False)  # Save to CSV
print("Data saved to craigslist_listings.csv")