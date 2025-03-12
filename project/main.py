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
    item = 'speaker'
    location = 'syracuse'
    output_csv = "craigslist_with_ebay_queries.csv"
    final_csv = "final_prices_and_descriptions.csv"

    print("Searching for: ", item, " in ", location)
    print("This will take a while, please be patient...")

    #scrape from craigslist this is the large one that will take a while
    craigslist_data = craiglist.scrape_craigslist(item, location)

   
    print("Craigslist data saved to 'craigslist_data.csv'")


   # Generate eBay search queries using OpenAI
    print("Generating eBay queries in bulk...")
    ebay_queries = gpt.batch_generate_ebay_queries_gpt(craigslist_data)

    # Fill missing queries and trim excess queries
    while len(ebay_queries) < len(craigslist_data):
        ebay_queries.append("")  # Fill missing queries with empty string
    if len(ebay_queries) > len(craigslist_data):
        ebay_queries = ebay_queries[:len(craigslist_data)]  # Trim excess queries

    # Add queries to dataframe
    craigslist_data["eBay Search Query"] = ebay_queries

    # Save Craigslist data with eBay search queries
    craigslist_data.to_csv(output_csv, index=False)
    print(f"Craigslist Data saved to {output_csv}")

    # Save final cleaned dataset with only prices and descriptions
    final_df = craigslist_data[["Price", "eBay Search Query"]]

    final_df.to_csv(final_csv, index=False)

    print(f"Prices and ebay titles saved to {final_csv}")





if __name__ == "__main__":
    main()
