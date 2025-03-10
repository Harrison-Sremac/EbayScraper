import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def scrape_craigslist(item, location):
    """
    Scrape Craigslist
    """

    # Craigslist search URL 
    SEARCH_URL = "https://"+location+".craigslist.org/search/sss?purveyor=owner&query="+ item+ "&sort=date#search=2~list~0" 

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

    # Find all listings
    listings = soup.find_all("li", class_="cl-static-search-result")

    data = []
    for listing in listings:
        # Extract title
        title = listing.find("div", class_="title").text.strip()

        # Extract price
        price_tag = listing.find("div", class_="price")
        price = price_tag.text.strip() if price_tag else "N/A"

        # Extract location
        location_tag = listing.find("div", class_="location")
        location = location_tag.text.strip() if location_tag else "Unknown"

        # Extract URL from <a> tag
        url_tag = listing.find("a", href=True)
        if url_tag:
            url = url_tag["href"]
        else:
            continue  # Skip listings without URLs

        # goes to the listing page to get more details
        time.sleep(1)  #to avoid getting blocked
        listing_response = requests.get(url, headers=headers)
        if listing_response.status_code != 200:
            print(f"Failed to fetch listing: {url}")
            continue

        listing_soup = BeautifulSoup(listing_response.text, "html.parser")

        # Extract description
        description_tag = listing_soup.find("section", {"id": "postingbody"})
        description = description_tag.text.strip() if description_tag else "No description available"

        # Extract date posted
        date_tag = listing_soup.find("time", {"class": "date timeago"})
        date_posted = date_tag["datetime"] if date_tag else "Unknown"

        # Append data
        data.append({"Title": title, "Price": price, "Location": location, "Date Posted": date_posted, "Description": description, "URL": url})

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data)
   
    return df
    