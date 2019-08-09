import requests
import time
import pandas as pd


class Bot():

    client_secret = "RgGPOYSqMh7lp3P3kHcj9QMLrvM"
    client_id = "LCcJRjCModPBww"

    token = ''

    username = "pipparichter"
    password = "Granola99356095"
    user_agent = "reddibot by u/pipparichter"
    
    # Eventually make it so all sensitive info is stored in environment variables
    # def __init__(self):

    def authenticate(self):
        
        data = {"grant_type":"password", "username":self.username, "password":self.password}
        auth = (self.client_id, self.client_secret)
        headers = {"User-Agent":self.user_agent}

        response = requests.post("https://www.reddit.com/api/v1/access_token", 
                                    data = data, 
                                    auth = auth, 
                                    headers = headers
                                )

        if response.status_code == 200:
        
            response = response.json()
            self.token = "bearer " + response["access_token"]
            
            return True

        else:

            return False
    
    # Takes a pandas DataFrame as input and organizes it
    def clean(sub_data):
        
        sub_data.sort_values("SUB_NAME", inplace = True)
        sub_data.drop_duplicates(subset = "FULLNAME", inplace = True)
        sub_data.reset_index(drop = True, inplace = True)

        return sub_data

    # Writes the sub data to a file in CSV format
    def save_local(sub_data):

        with open("../sub_data.csv", 'w') as f:

            sub_data.to_csv(f)


    def save_aws(sub_data):
        
        import boto3
        s3 = boto3.client("s3")
        
        filename = "sub_data.csv"
        bucket_name = "reddibot"

        s3.upload_file(filename, bucket_name, filename)


    def get_subs(self):
        # Create an empty DataFrame object to store data
        sub_data = pd.DataFrame({"SUB_NAME":[], "FULLNAME":[], "MEMBERS":[]})
       
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
            
            # raw_sub_data is now a list of dictionaries, each containing data on a different subreddit
            raw_sub_data = response["children"]

            for sub in raw_sub_data:

                new = {}

                new["SUB_NAME"] = sub["data"]["display_name"]
                new["FULLNAME"] = sub["data"]["name"]
                    
                sub_data = sub_data.append(new, ignore_index = True)

            params["after"] = response["before"]

            item_num = len(raw_sub_data)
            count += item_num
            params["count"] = count
                
            print(count)
            # Sleep for 5 seconds in an attempt to avoid 'Max retries exceeded with URL' Exception
            time.sleep(5)

            # Check to see if the loop has scrolled through the entire listing
            if item_num < 100:

                break
        
        # Clean up the data
        sub_data = Bot.clean(sub_data)
        # Write the sub data to sub_data.csv
        Bot.save_local(sub_data)
        # Upload the sub data to AWS reddibot bucket
        Bot.save_aws(sub_data)


    def update_subs():





bot = Bot()

bot.get_subs()
