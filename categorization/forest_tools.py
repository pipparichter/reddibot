import sys
sys.path.append("./dictionaries")
sys.path.append("../sub_names")

import dicts

import re
import pandas as pd
import numpy as np
import random

# random library will be used for generating test data subsets
random.seed(11092001)


# Combined is a dictionary in which every key is a letter and every value is a list of 
# every word from both dictionaries which begins with that letter
combined = dicts.combined

# ----------------------------- Loading sub names -------------------------------------------

def load_subs():

    with open("../sub_names/sub_names.csv", 'r') as f:
        
        df = pd.read_csv(f)
        # Have to convert the pd.Series object to np.array
        names = np.array(df["SUB_NAMES"])
    # 'names' is a numpy array containing every sub name
    return names

# -------------------------------- Class definitions -----------------------------------------

# This is basically the replacement class for 'item,' which will populate a node of the tree
class Subreddit:
    
    category = ''
    name = ''
    # 'profile' is a dictionary in which every key is a word in 'combined' and every value is a 
    # boolean indicating whether or not the word is 'in' the subreddit name
    profile = {}

    def __init__(self, name):
        
        self.name = name

    # The profile contains the attributes of an item, on which the splits will be made
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
    # Note that profile does not contain a 'False' value for every word the Subreddit name does not contain;
    # it does have a true value for every name it does contain

# Class for implementing a node in the decision tree
class Node:
    
    # The children attribute is a list of Nodes objects (i.e. the 0, 1, or 2 nodes branching from the Node)
    children = []



# Class for implementing the decision tree itself
class DecisionTree:
    
    # The decision tree will essentially be a list of lists of lists of lists... and so on... of Nodes. Pointers
    # would make my life so much easier, thanks a lot Python
    tree = []

    # Initialize the decision tree with a root node, i.e. a list of Subreddit objects
    def __init__(root):

        tree[0] = root
        
    # This calculates the Gini impurity of a given split
    # The input is a list containing a left and right child nodes
    def get_gini(nodes):
        
        gini = 0
        total_size = len(nodes[0]) + len(nodes[1])

        for node in nodes:
            s = 0
            size = len(node)

            # cats is a dictionary containing every category present in a node as a key, and the number
            # of instances of each category (an int) as values
            cats = {}
        
            for sub in node:
            
                if sub.category in left_cats:
                    left_cats[sub.category] += 1
                else:
                    left_cats[sub.category] = 1
            
            for category in cats:
                proportion = cats[category]/size
                s += proportion**2
            
            # g_node is the Gini impurity for a single node; this value is then weighted according
            # to the relative size of the node
            g_node = 1 - s
            g_weighted = g_node*(size/total_size)
            # gini is the total Gini index for the split, to which the weighted indices for each node are added
            gini += g_weighted
        
        return gini


    def generate_tree()
      

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
    # categorized contains a list of Subreddit objects for which the category attribute is known
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
        
        # How big do I want each training subset to be? How big does the entire training set need to be?
        # I think it should be around one-third of the entire training dataset. 
        for i i 

    # How am I going to build a training dataset?
    def sort():






        
    
    




