import requests
import time
import pandas as pd
import sys
sys.path.append("../")

import reddibot



class SubNamesBot(reddibot.Bot):
    
    def get_subs(self):
        # Create an empty DataFrame object to store data
        sub_names = pd.DataFrame({"SUB_NAME":[], "FULLNAME":[], "MEMBERS":[]})
       
        # Keeping track of the total number of items received
        count = 0

        params = {"show_users":False, "sort":"relevance", "include_categories":True, "limit":100}
        
        while True:
            # The access token expired before the scraping was complete, so self.authenticate()
            # had to be moved inside of the 'while' loop
            self.authenticate()
            headers = {"Authorization":self.token, "User-Agent":self.user_agent}
                
            response = requests.get("https://oauth.reddit.com/subreddits", headers = headers, params = params)
            response = response.json()["data"]
            
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
            # Sleep for 5 seconds in an attempt to avoid 'Max retries exceeded with URL' Exception
            time.sleep(10)

            # Check to see if the loop has scrolled through the entire listing
            if item_num < 100:

                break
        
        # Clean up the data
        sub_names = reddibot.Bot.clean(sub_names)
        # Write the sub data to sub_names.csv
        reddibot.Bot.save_local(sub_names, "sub_names.csv")
        # Upload the sub data to AWS reddibot bucket
        reddibot.Bot.save_aws(sub_names, "sub_names.csv")


    # def update_subs():





bot = Bot()

bot.get_subs()
