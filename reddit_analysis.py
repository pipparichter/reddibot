import requests
import re

# For clients using OAuth2 Authentification, the Reddit API ratelimits at 60 requests per second.

clientID = 'qTWe2L0Nkb6xxQ'
clientSecret = '8bilVsLCVjFqlutRgjmnmaaHtDY'
auth = requests.auth.HTTPBasicAuth(clientID, clientSecret)
header = {'User-Agent':'RedditBot (by u/pipparichter)'}
data = {'grant_type':'client_credentials'}
params = {'scope':'*'}

token = requests.post('https://www.reddit.com/api/v1/access_token', headers = header, auth = auth, data = data, params = params).json()['access_token']

tokenAuth = {'Authorization':'bearer ' + token}

print(token)

def getTrending():
    params = {'after':''}
    response = requests.get('https://oauth.reddit.com/r/trendingsubreddits/top/', headers = {**header, **tokenAuth}, params = params).json()
    trendingTitles = response['data']['children'][0]['data']['title']
    splitTitles = re.split(' ', trendingTitles)
    print(splitTitles)
    titleList = [string for string in splitTitles if re.match('/r/+', string) == True]
    
    return titleList


