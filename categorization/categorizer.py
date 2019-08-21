import sys
sys.path.append("./dictionaries")
sys.path.append("../sub_names")

import dicts

import re
import pandas as pd
import numpy as np
import random

random.seed(11092001)

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


# 'combined' is a dictionary in which each key is a letter of the alphabet, and each value is a list containing
# every word from both dictionaries which begins with that letter
combined = dicts.combined


def load_subs():

    with open("../sub_names/sub_names.csv", 'r') as f:
        
        df = pd.read_csv(f)
        # Have to convert the pd.Series object to np.array
        names = np.array(df["SUB_NAMES"])
    # 'names' is a numpy array containing every sub name
    return names


# Class to implement the random forest sorting algorithm
class Subreddit:
    
    category = ''
    name = ''
    # 'profile' is a dictionary in which every key is a word in 'combined' and every value is a 
    # boolean indicating whether or not the word is 'in' the subreddit name
    profile = {}

    def __init__(self, name):
        
        self.name = name


    def build_profile(self):
        
        for letter in self.name:
            # Avoid having to search the entire combined dictionary by looping through only the
            # relevant letters
            for word in combined[letter]:
                
                pattern = re.compile(f"{word}")
                # What is the difference between 'is not' and '!='?
                if pattern.search(self.name) is not None:

                    profile[word] = True

                else:
                    # This may not be worth doing; if this is horrifically slow, remove
                    profile[word] = False



class RandomForest:
    # Is there an enum type equivalent in Python?
    categories = ["Sports", "Gaming", "News", "TV", "Aww", "Memes", "Pics and Gifs", "Travel",
                  "Tech" "Music", "Art and Design", "Beauty", "Books and Writing", "Crypto", "Discussion",
                  "Fashion", "Finance and Business", "Food", "Health and Fitness", "Learning", "Mindblowing",
                  "Outdoors", "Parenting", "Photography", "Relationships", "Science", "Video Games", 
                  "Videos", "Vroom", "Wholesome"]
    sub_names = np.array([])
    # subs is a list of Subreddit objects which have not yet been categorized
    subs = []
    # categorized contains a list of Subreddt objects for which the category attribute is known
    categorized = []
    # training contains a list of Subreddit objects for which the category attribute is known
    # This is the training set (should end up being around a third of the size of subs)
    training = []


    def __init__(self):

        self.sub_names = load_subs()
        # Initialize the sub_profiles dictionary
        for sub_name in sub_names:

            sub = Subreddit(sub_name)
            # Assign the sub.profile attribute
            sub.build_profile()
            self.subs.append(sub)
    
    

    def create_training_subset(self):

    # How am I going to build a training dataset?
    def sort():






        
    
    




