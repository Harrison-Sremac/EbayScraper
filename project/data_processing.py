import pandas as pd



# Common words to remove from titles (optional)
IGNORED_WORDS = {"great", "good", "like new", "working", "condition", "vintage", "best", "cheap", "nice",
    "used", "perfect", "clean", "excellent", "fair", "poor", "damaged", "restored", "pristine",
    "functional", "tested", "untested", "for parts", "as is", "repair", "refurbished",
    "broken", "scratched", "mint", "flawless", "worn", "wear", "barely used", "old", "retro",
    "antique", "classic", "new", "never used", "unused", "almost new", "open box", "pre-owned",
    "original", "authentic", "real", "replica", "fake", "replacement", "aftermarket",
    "high quality", "low quality", "top quality", "best quality", "amazing", "cool", "awesome",
    "must see", "must sell", "bargain", "steal", "obo", "firm", "negotiable", "cash only",
    "pickup only", "shipping available", "fast shipping", "free shipping", "local only",
    "limited edition", "hard to find", "one of a kind", "special edition", "collectible",
    "rare", "custom", "handmade", "professional", "hobbyist", "standard", "heavy duty",
    "lightweight", "durable", "heavy", "light", "compact", "portable", "small", "big",
    "large", "medium", "full size", "mini", "micro", "macro", "industrial", "commercial",
    "consumer", "entry level", "high end", "low end", "basic", "advanced", "beginner",
    "expert", "gaming", "business", "home use", "office use", "studio", "professional use",
    "powerful", "efficient", "energy efficient", "eco-friendly", "green", "modern", "trendy",
    "stylish", "fashionable", "sleek", "elegant", "simple", "fancy", "exclusive", "high tech",
    "upgraded", "newest", "latest", "previous version", "older model", "discontinued"}

def generate_ebay_query(title, description):
    # Remove common words from the title
    words = title.lower().split()
    filtered_words = [word for word in words if word not in IGNORED_WORDS]

    # Join the important words back into a phrase
    query = " ".join(filtered_words)

    # Add important details from the description if available
    if "brand" in description.lower():
        query += " " + description.split()[0]  # Example: Add first word from description if it mentions a brand
    if "model" in description.lower():
        query += " " + description.split()[1]

    if "size" in description.lower():
        query += " " + description.split()[2]
    

    # Format query for eBay search
    ## adding -parts -repair to exclude parts and repair itemss
    ebay_query = f'"{query}" -parts -repair'
    
    return ebay_query.strip()




def process_craigslist_data(input_csv: str, output_csv: str):
    """
    Loads Craigslist data from a CSV file, generates eBay search queries,
    and saves the results to a new CSV file.
    """
    try:
        # Load data
        df = pd.read_csv(input_csv)

        # Ensure required columns exist
        if "Title" not in df.columns or "Description" not in df.columns:
            raise ValueError("CSV file must contain 'Title' and 'Description' columns.")

        # Apply the function to generate eBay queries
        df["eBay Search Query"] = df.apply(lambda row: generate_ebay_query(row["Title"], row["Description"]), axis=1)

        # Save the updated DataFrame to a new CSV
        df.to_csv(output_csv, index=False)
        print(f"Data saved to {output_csv}")
    
    except Exception as e:
        print(f"Error processing data: {e}")

# Example usage:
input_file = "craigslist_listings_with_details.csv"
output_file = "craigslist_with_ebay_queries.csv"
process_craigslist_data(input_file, output_file)