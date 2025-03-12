from openai import OpenAI


import os
import pandas as pd

# Load OpenAI API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def batch_generate_ebay_queries_gpt(dataframe: pd.DataFrame) -> list:
    """
    Uses OpenAI's GPT model to generate eBay search queries in bulk for all Craigslist listings.
    Returns a list of optimized eBay search queries.
    """
    try:
        # Convert listings into a structured prompt
        listings = "\n".join([
            f"{i+1}. Title: {row['Title']} | Description: {row['Description']}"
            for i, row in dataframe.iterrows()
        ])

        prompt = f"""
        You are an eBay search optimization assistant. Your job is to generate 
        concise but specific eBay search queries based on Craigslist listings.

        Here are the listings:

        {listings}

        Generate an optimized eBay search query for each listing.
        Rules:
        - Extract key features (brand, model, size, type).
        - Remove unnecessary words (e.g., "great condition", "like new").
        - Format the query like: "brand model type" -parts -repair.
        - Keep it short but specific for best eBay results.
        
        for example: a listing containing 
        "Custom build gaming PC built by a professional. I have been building, selling and repairing computers since the late 90’s This PC is flawless. It is a multi-purpose PC built with love and care. It has an Asus ROG STRIX Z590-E motherboard, an Intel I7 11700K 8-core 16-thread CPU. Corsair Vengeance RGB DDR4 4000 PC4 32000 RAM. A Samsung M.2 NVMe 512GB 980 Pro SSD. A Western Digital 2TB SATA Hard Drive for games and storage. A Deepcool Captain 240PRO V2 RGB AIO Cooler. I used Kingpin Thermal Paste which is a long-lasting high quality thermal paste. A Nvidia GeForce EVGA GTX 1080Ti FTW3 Hybrid GPU. A EVGA Supernova 750 G5 80+Gold PSU. It’s all in a beautiful Darkflash DLX 22 PC Mid Tower Case. It has 8 Addressable RGB fans. It has Windows 11 Pro and Office. Is has some other software on it also. It will play any game on ultra-settings @1080p .I will trade for an good brand RTX 5080 like Asus.

I WILL NOT ACCEPT ANY CASHIERS CHECKS DO NOT CONTACT ME AND ASK ME TO EMAIL YOU. DO NOT TRY TO SCAM ME WITH CASHAPP, VENMO, or ZELLE. I KNOW ALL THE SCAMS SO DO NOT TRY!!"

        should be optimized to:
        Custom Gaming PC Intel i7-11700K GTX 1080Ti 16GB+ RAM SSD HDD 

        Return a list where each line contains:
        eBay Search Query

        Output only the list, no extra text.
        """

        response = client.chat.completions.create(model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000)

        # Parse response into a list
        response_text = response.choices[0].message.content.strip()
        ebay_queries = response_text.split("\n")  # Split by newlines

        return ebay_queries

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []