import os
import pandas as pd
import openai
import craigslist_scraper as craiglist
import openAI_processing as gpt
import data_processing as data
import ebay_scraper    as ebay

def main():
    """ Main function that loads API key, processes Craigslist data, and saves eBay queries. """
    print("Starting the search...")

    #scrape from craigslist
    item = 'piano'
    location = 'ithaca'
    output_csv = "craigslist_with_ebay_queries.csv"
    final_csv = "final_prices_and_descriptions.csv"

    print("Searching for: ", item, " in ", location)
    print("This will take a while, please be patient...")

    #scrape from craigslist this is the large one that will take a while
    craigslist_data = craiglist.scrape_craigslist(item, location)


    print("Craigslist data saved to 'craigslist_data.csv'")

    craigslist_data["eBay Search Query"] = craigslist_data.apply(
        lambda row: data.generate_ebay_query(row["Title"], row["Description"]), axis=1
    )

    craigslist_data.to_csv(output_csv, index=False)
    print(f"✅ Data saved to {output_csv}")

    
    final_df = craigslist_data[["Price", "Description"]]
    final_df.to_csv(final_csv, index=False)




    print(f"✅ Final cleaned data saved to {final_csv}")





if __name__ == "__main__":
    main()
