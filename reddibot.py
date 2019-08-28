import requests


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
    def save_local(sub_data, filename):

        path = "./" + filename

        with open(path, 'w') as f:

            sub_data.to_csv(f)


    def save_aws(sub_data, filename):
        
        import boto3
        s3 = boto3.client("s3")
        
        bucket_name = "reddibot"

        s3.upload_file(filename, bucket_name, filename)

    # Sends a specified report to me if anything goes wrong with the bot 
    def send_report(self, report):
        
        print(self.authenticate())

        headers = {"Authorization":self.token, "User-Agent":self.user_agent}
        params = {
                    "api_type":"json", 
                    "subject":"reddibot Alert", 
                    "text":report,
                    "to":"pipparichter"
                }
        
        requests.post("https://oauth.reddit.com/api/compose", params = params, headers = headers)
        



