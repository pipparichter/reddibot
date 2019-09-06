import sys
sys.path.append("./data/")
sys.path.append("./dictionaries/")
sys.path.append("../sub_names/")


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

# Class definitions -----------------------------------------------------------------------

# This is basically the replacement class for 'item,' which will populate a node of the tree
class Subreddit:
    
    category = None
    name = None
    # 'attributes' is a dictionary in which every key is a word in 'combined' and every value is a 
    # boolean indicating whether or not the word is 'in' the subreddit name
    attributes = {}

    def __init__(self, name, category = None):
        
        self.name = name
        print(name)
        self.category = category
    
        self.build_attributes()

    # The attributes contains the attributes of an item, on which the splits will be made
    # This part of the process will probably need to be sped up
    def build_attributes(self):
        
        for word in combined:
                
            pattern = re.compile(f"{word}")
            # What is the difference between 'is not' and '!='?
            if pattern.search(self.name) is not None:
                self.attributes[word] = True
            else:
                self.attributes[word] = False

# Class for implementing a node in the decision tree
class Node:
    
    # Apparently all member data which are assigned a value in the class (not in init) are by default
    # static, no keyword needed!
    
    # If the Node is terminal, then this attribute is assigned 
    category = None
    # This is marked True if the Node is terminal
    is_terminal = False
    # The criterion upon which the node was split (assigned by the DecisionTree.generate_tree function)
    split_criterion = None
    # A list of all of the attributes (i.e. words) that could be used for splitting
    criteria = combined[:]
    # 'data' is a list of Subreddit objects contained by the Node
    data = []
    # The children attribute is a list of Nodes objects (i.e. the 0, 1, or 2 nodes branching from the Node)
    children = [None, None]

    def __init__(self, data):

        self.data = data

    # Returns the possible left and right children of 'node' (a Node object) when split with respect 
    # to a certain attribute, where attribute is a possible substring in the Subreddit name
    def split_node(node, attribute):
        # Data for the Node for which the attribute is False
        left_child_data = []
        # Data for the Node for which the attribute is True
        right_child_data = []

        for sub in node.data:
            # Reminder that 'sub.attributes' is a dictionary in which the keys are every
            # word in combined, and the values are Bools      
            if (sub.attributes[attribute] == False):
                left_child_data.append(sub)
            else:
                right_child_data.append(sub)
        # Use the data to initialize left and right child Nodes
        right_child = Node(right_child_data)
        left_child = Node(left_child_data)
        # Return two child Nodes in the form of a tuple 
        return [left_child, right_child]
    
    # Selects the best attribute on which to split the dataset, and applies the split to self
    def split_node_optimized(self):
        # The highest possible Gini impurity index is 1.0
        lowest_gini = 1.0
        # 'best_split' will eventually be a list of two Node objects representing left and
        # right children
        best_split_children = None
        best_split_criterion = None
        # Test each criterion by splitting the Node with respect to every possible word
        for criterion in Node.criteria:
            
            poss_children = Node.split_node(self, criterion)
            gini = DecisionTree.get_gini(poss_children)

            if gini < lowest_gini:
                best_split_criterion = criterion
                best_split_children = poss_children

        # If no split exists that's more efficient than 1.0, then the current Node object is a terminal Node
        if (lowest_gini == 1.0):
            self.is_terminal = True
            # Assign the terminal Node a category
            self.category = max([sub.category for sub in self.data], key = list.count)
        else:
            # Apply the split to self
            self.children = best_split_children
            self.split_criterion = best_split_criterion


# Class for implementing a decision tree
class DecisionTree:
    
    max_depth = 100
    # 'tree' is a Node object instance
    root = None
    
    # Initialize the decision tree with training data by inputting a list of Subreddit objects
    def __init__(self, training_data):

        self.root = Node(training_data)
        self.generate_tree()
        
    # This calculates the Gini impurity of a given split (used only for training set
    # Subreddit objects)
    # The input is a list containing a left and right child nodes
    def get_gini(nodes):
        
        gini = 0
        total_size = len(nodes[0].data) + len(nodes[1].data)

        for node in nodes:
            # 'node_sum' is the sum of all 'proportion's for a given Node (see below)
            node_sum = 0
            node_size = len(node.data)
            # 'cats' is a dictionary containing every category present in a node as a key, and the number
            # of instances of each category (an int) as values
            cats = {}
        
            for sub in node.data:
                if sub.category in cats:
                    cats[sub.category] += 1
                else:
                    cats[sub.category] = 1
            
            for category in cats:
                proportion = cats[category]/node_size
                node_sum += proportion**2
            
            # 'g_node' is the Gini impurity for a single node; this value is then weighted according
            # to the relative size of the node
            node_gini = 1 - s
            node_gini_weighted = node_gini*(node_size/total_size)
            # gini is the total Gini index for the split, to which the weighted indices for each node are added
            gini += node_gini_weighted
        
        return gini
   
    # If this doesn't work, then it's not mutating the child Nodes inplace
    
    # Creates the decision tree; it takes a root node as input, and grows the tree
    def generate_tree(self, node = None, count = 0):
        
        if node is None:
            node = self.root

        # Populates the 'children' attibute of 'node'
        node.split_node_optimized()
        count += 1
        
        # If the node is terminal, stop growing the branch
        if node.is_terminal:
            return

        # If the max depth has been reached, stop growing the branch
        if (count == self.max_depth):
            return

        left_child, right_child = node.children[0], node.children[1]
        # If branch growth can continue, call generate_tree on each child node
        self.generate_tree(left_child, count)
        self.generate_tree(right_child, count)
    
    # Returns the inputted Subreddit object with an assigned category; the first Node
    # object plugged into the function should be the root node
    def predict_sub(self, sub, node = None):
        
        if node is None:
            node = self.root

        criterion = node.split_criterion
        
        # If a terminal Node is reached, assign the Subreddit 'category' attribute
        if node.is_terminal:
            sub.category = node.category
            return

        if sub.criteria[criterion] == True:
            # If the sub has this attribute, then it gets sorted into the 'true' branch
            next_node = node.children[1]
        else:
            # If the sub does not have this attribute, then it gets sorted into the 'false' branch
            next_node = node.children[0]
        
        DecisionTree.predict_sub(next_node, sub)

    # Returns a list of Subreddit objects which have been assigned categories, and takes a list of 
    # unpredicted Subreddit objects as input
    def predict(self, test_data):
    
        predicted = []
        
        for sub in test_data:
            sub = sub.copy()
            self.predict_sub(sub)
            predicted.append(sub)
        
        return predicted




class RandomForest:
    # 'trees' is a list of DecisionTree objects
    trees = None    
    categories = None
    # 'results' contains a list of Subreddit objects for which the category attribute is known
    results = None
    # 'training' contains a list of Subreddit objects for which the category attribute is known
    # This is the training set (should end up being around a third of the size of subs)
    training = [] 
    # 'N' is the size of the training dataset
    N = len(training)
    # 'test' contains a list of Subreddit objects for which the category attribute is not
    # known. 
    test = None

    def __init__(self):
        # Initialize the 'test' and 'training' attributes
        training_info = pd.read_csv("./data/training_data.csv", index_col = 0)[0:1]
        self.training = [Subreddit(t[0], t[1]) for t in training_info.itertuples(index = False)]
        
        test_info = list(pd.read_csv("./data/test_data.csv")["SUB_NAME"])[0:1]
        self.test = [Subreddit(name) for name in test_info]

        with open("./data/categories.txt", 'r') as f:
            categories = f.read().split('\n')
            self.categories = categories
    
    # Returns a list of Subreddit objects from the training dataset (i.e. with known
    # categories)
    def bootstrap(self):
        # 'subbag' is a subset of the training set selected randomly with replacement
        bag = []
        # Around 80 percent of the total training data is the recommended size for a
        # without-replacement bag (see random_forest_notes.md)
        for i in range(int(0.8*self.N)):
            bag.append(random.choice(self.training))
        
        return subbag


    def generate_forest(self):
       
        trees = []
        # How many decision trees should there be?
        for i in range(50):
            training_set = self.bootstrap()
            # Initialize a decision tree with the training data
            tree = DecisionTree(training_set)
            trees.append(tree)
        self.trees = trees
