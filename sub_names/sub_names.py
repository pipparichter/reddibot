import requests
import random
import pandas as pd
import sys
# Make sure the parent directory is in path so reddibot can be imported
sys.path.append("../")

import reddibot


class SubNamesBot(reddibot.Bot):
    
    def get_subs(self):
        # Create an empty DataFrame object to store data
        sub_names = pd.DataFrame({"SUB_NAME":[], "FULLNAME":[]})
       
        # Keeping track of the total number of items received
        count = 0

        params = {"show_users":False, "sort":"relevance", "include_categories":True, "limit":100}
        
        while True:

            try:
                # The access token expired before the scraping was complete, so self.authenticate()
                # had to be moved inside of the 'while' loop
                self.authenticate()
                headers = {"Authorization":self.token, "User-Agent":self.user_agent}
                
                response = requests.get("https://oauth.reddit.com/subreddits", headers = headers, params = params)
                response = response.json()["data"]

            except requests.ConnectionError:

                print("ConnectionError thrown, subreddit data has been saved.")
                # Break out of 'while' loop and save data
                break

            # raw_sub_names is now a list of dictionaries, each containing data on a different subreddit
            raw_sub_names = response["children"]

            for sub in raw_sub_names:

                new = {}

                new["SUB_NAME"] = sub["data"]["display_name"]
                new["FULLNAME"] = sub["data"]["name"]
                    
                sub_names = sub_names.append(new, ignore_index = True)

            params["after"] = response["before"]

            item_num = len(raw_sub_names)
            count += item_num
            params["count"] = count
                
            print(count)

            # Check to see if the loop has scrolled through the entire listing
            if item_num < 100:

                break
        
        # Shuffle the names
        for i in range(len(sub_names.index)):
            random_ind = random.randint(0, len(sub_names.index) - 1)
            # REMEMBER TO ASSIGN TMP TO A COPY!!! pd.Series are mutable, so messing with one
            # will mess with the other
            tmp = sub_names.iloc[i].copy()
            sub_names.iloc[i] = sub_names.iloc[random_ind].copy()
            sub_names.iloc[random_ind] = tmp
        # Reset the indices
        sub_names.reindex([n for n in range(len(sub_names.index))])

        # Clean up the data
        sub_names = reddibot.Bot.clean(sub_names)
        # Write the sub data to sub_names.csv
        reddibot.Bot.save_local(sub_names, "sub_names.csv")
        # Upload the sub data to AWS reddibot bucket
        reddibot.Bot.save_aws(sub_names, "sub_names.csv")


    # def update_subs():
     
