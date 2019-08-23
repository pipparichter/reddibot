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
    # This part of the process will probably need to be sped up
    def build_profile(self):
        
        for word in combined[letter]:
                
            pattern = re.compile(f"{word}")
            # What is the difference between 'is not' and '!='?
            if pattern.search(self.name) is not None:

                profile[word] = True

            else:
                profile[word] = False

# Class for implementing a node in the decision tree
class Node:
    
    # Apparently all member data which are assigned a value in the class (not in init) are by default
    # static, no keyword needed!
    
    split_criterion = None
    # A list of all of the attributes (i.e. words) that could be used for splitting
    attributes = [word for word in letter in combined]
    # 'data' is a list of Subreddit objects contained by the Node
    data = []
    # The children attribute is a list of Nodes objects (i.e. the 0, 1, or 2 nodes branching from the Node)
    children = [None, None]

    def __init__(self, data):

        self.data = data

    # Splits a node with respect to a certain attribute, where attribute is a possible substring in the
    # Subreddit name
    def split_node(node, attribute):
        # Node for which the attribute is False
        left_child = Node([])
        # Node for which the attribute is True
        right_child = Node([])

        for sub in node:
            
            if sub.profile[attribute] == False:

                left_child.data.append(sub)

            else:

                right_child.data.append(sub)

        node.children[0], node.children[1] = left_child, right_child
    
    # Selects the best attribute on which to split the dataset, and applies the split to self
    def split_node_optimized(self):
        # The highest possible Gini impurity index is 1.0
        lowest_gini = 1.0
        # 'best_split' will eventually be a Node object with two children
        best_split = None

        for attribute in Node.attributes:
            # Create a new Node object so testing the plits won't screw with self
            new_node = Node(self.data)
            new_node.split_criterion = attribute
            # Remember that this function is inplace
            Node.split(new_node, attribute)
            gini = DecisionTree.get_gini(new_node.children)

            if gini < lowest_gini:

                best_split = new_node
        
        # Apply the best split to self
        self.children = best_split.children


# Class for implementing the decision tree itself
class DecisionTree:
    
    max_depth = 100
    # 'tree' is a Node object instance
    tree = None 
    
    def __repr__(self):

        
    
    # Initialize the decision tree with a root node, by inputting a list of Subreddit objects
    def __init__(self, root_data):

        self.tree = DecisionTree.generate_tree(Node(root_data))
        
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
   
    # Creates the decision tree; it takes a root node as input, and grows the tree
    def generate_tree(node, count = 0):
        # Populates the 'children' attibute of 'node'
        node.split_node_optimized()
        count += 1
        
        left_child = node.children[0]
        right_child = node.children[1]
        # Prevent the tree from exceeding the set max_depth 
        if count == self.max_depth:
            return
        elif (left_child == None) and (right_child == None):
            return

        elif (left_child == None):
            DecisionTree.generate_tree(right_child, count)
        elif (right_child == None):
            DecisionTree.generate_tree(left_child, count)
        # If neither the left or right child nodes are None, call generate_tree on each
        else:
            DecisionTree.generate_tree(left_child, count)
            DecisionTree.generate_tree(right_child, count)
    
    
    def tree_predict(self, node):

        for sub in node.data:

            if 



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
         

    # How am I going to build a training dataset?
    def sort():






        
    
    




