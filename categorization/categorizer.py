import re

# Categories:
#   Sports                  Beauty                      Parenting
#   Gaming                  Books and Writing           Photography
#   News                    Crypto                      Relationships
#   TV                      Discussion                  Science
#   Aww                     Fashion                     Video Games
#   Memes                   Finance and Business        Videos
#   Pics and Gifs           Food                        Vroom
#   Travel                  Health and Fitness          Wholesome
#   Tech                    Learning
#   Music                   Mindblowing
#   Art and Design          Outdoors


def remove_duplicates(lst):

    lst = sorted(lst)

    for i in range(len(lst) - 1):
        
        if lst[i] == lst[i + 1]:

            lst[i + 1] = ''

    return [word for word in lst if word != '']


# 'combined' is a dictionary in which each key is a letter of the alphabet, and each value is a list containing
# every word from both dictionaries which begins with that letter
combined = {}

# Load and clean dictionaries
with open("./urban_dict.txt", 'r') as ud, open("./dict.txt", 'r') as d:
    
    alph = "abcdefghijklmnopqrstuvwxyz"
    
    ud = ud.read().split('\n')
    d = d.read().split('\n')

    ud_index = 0
    d_index = 0

    for letter in alph:
       
        words = []
        pattern = re.compile(f"^[{letter}{letter.upper()}].*$")
        # Subreddit names can only contain letters, numbers, and underscores, and no more than
        # 21 characters
        subreddit_rules = re.compile("^[\w]{1,21}$")
        
        while pattern.match(ud[ud_index]):

            if subreddit_rules.match(ud[ud_index]):
                
                words.append(ud[ud_index].lower())
            
            ud_index += 1
            print(ud[ud_index])

        while pattern.match(d[d_index]):

            if (subreddit_rules.match(d[d_index])):

                words.append(d[d_index].lower())

            d_index += 1

        words = remove_duplicates(words)
        combined[letter] = words


