import re

# 'combined' is a merged list of the Urban Dictionary and regular dictionary words
# All words match the subreddit naming rules
combined = None

def remove_duplicates(lst):

    lst = sorted(lst)

    for i in range(len(lst) - 1): 
        if lst[i] == lst[i + 1]:
            lst[i + 1] = None

    return [word for word in lst if word != None]


# Load and clean dictionaries
with open("./dictionaries/urban_dict.txt", 'r') as ud, open("./dictionaries/dict.txt", 'r') as d:
    
    words = []

    ud = ud.read().split('\n')
    d = d.read().split('\n')
   
    # Subreddit names can only contain letters, numbers, and underscores, and no more than
    # 21 characters
    subreddit_rules = re.compile("^\w{1,21}$")

    for word in d + ud:

        if subreddit_rules.match(word): 
            words.append(word.lower())

    words = remove_duplicates(words)
    combined = words

