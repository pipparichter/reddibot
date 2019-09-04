import requests
import random
import pandas as pd
import sys
import time
# Make sure the parent directory is in path so reddibot can be imported
sys.path.append("../")

import reddibot


class SubNamesBot(reddibot.Bot):
    # A list of every unique "advertiser_categories" the bot finds
    advertiser_categories = []

    def get_subs(self):
        # Create an empty DataFrame object to store data
        sub_data = pd.DataFrame({"SUB_NAME":[], "FULLNAME":[], "CATEGORY":[]})
       
        # Keeping track of the total number of items received
        count = 0

        params = {"show_users":False, "sort":"relevance", "include_categories":True, "limit":1}
        
        while True:

            try:
                # The access token expired before the scraping was complete, so self.authenticate()
                # had to be moved inside of the 'while' loop
                self.authenticate()
                headers = {"Authorization":self.token, "User-Agent":self.user_agent}
                
                response = requests.get(
                                        "https://oauth.reddit.com/subreddits", 
                                        headers = headers, 
                                        params = params
                                        )
                response = response.json()["data"]
                # Trying to prevent reddit from ratelimiting me
                # time.sleep(8)

            except requests.ConnectionError:
                print("ConnectionError thrown, subreddit data has been saved.")
                # Break out of 'while' loop and save data
                break

            # raw_sub_data is now a list of dictionaries, each containing data on a different subreddit
            raw_sub = response["children"][0]["data"]
            new = {}

            new["SUB_NAME"] = raw_sub["display_name"]
            new["FULLNAME"] = raw_sub["name"]

            try:
                cat = raw_sub["advertiser_category"]
                new["CATEGORY"] = cat
                # If the category is new, add it to the "advertiser_categories" list
                if cat not in self.advertiser_categories:
                    self.advertiser_categories.append(cat)

            except KeyError:
                new["CATEGORY"] = None
                
            sub_data = sub_data.append(new, ignore_index = True)

            params["after"] = response["before"]

            count += 1
            params["count"] = count
            print(count)

            # Clean up the data
        sub_data = reddibot.Bot.clean(sub_data)
        
        # Shuffle the names (the clean function has put them into alphabetical order)
        for i in range(len(sub_data.index)):
            random_ind = random.randint(0, len(sub_data.index) - 1)
            # REMEMBER TO ASSIGN TMP TO A COPY!!! pd.Series are mutable, so messing with one
            # will mess with the other
            tmp = sub_data.iloc[i].copy()
            sub_data.iloc[i] = sub_data.iloc[random_ind].copy()
            sub_data.iloc[random_ind] = tmp
        # Reset the indices
        sub_data.reindex([n for n in range(len(sub_data.index))])

       # Write the sub data to sub_data.csv
        reddibot.Bot.save_local(sub_data, "sub_data.csv")
        # Upload the sub data to AWS reddibot bucket
        reddibot.Bot.save_aws(sub_data, "sub_data.csv")

        # Also save the categories
        with open("categories.txt", 'w') as f:
            for category in self.advertiser_categories:
                f.write(category)
                f.write('/n')

    # def update_subs():
     
