import pandas as pd
import numpy as np
import sys
sys.path.append("../../sub_names/")

# Loading sub names -------------------------------------------

def load_subs():

    with open("../../sub_names/sub_names.csv", 'r') as f:
        
        df = pd.read_csv(f)
        # Have to convert the pd.Series object to np.array
        names = np.array(df["SUB_NAMES"])
    # 'names' is a numpy array containing every sub name
    return names


# Creating DataFrames ---------------------------------------------

sub_names = load_subs()

training = pd.DataFrame()
training.columns = np.array(["SUB_NAME", "CATEGORY"])

test = pd.DataFrame()
test.columns = np.array(["SUB_NAME"])

# All of the items in sub_names.csv have been shuffled (when the file was initially
# written), so indexing directly is fine

# For deciding a useful training dataset size, this post is helpful: 
# https://www.researchgate.net/post/Is_there_an_ideal_ratio_between_a_training_set_and_
# validation_set_Which_trade-off_would_you_suggest

# For now, I'll probably ignore the validation set and just see how to first
# part turns out

# The entire dataset is probably around 300,000 subreddits


# Creating the training data (ugh) -----------------------------------

training_subs = np.array(sub_names[:10000])

categories = {  
                1:"Sports",                 2:"Gaming", 
                3:"News",                   4:"TV", 
                5:"Aww",                    6:"Memes", 
                7:"Pics and Gifs",          8:"Travel", 
                9:"Tech",                   10:"Music", 
                11:"Art and Design",        12:"Beauty", 
                13:"Books and Writing",     14:"Crypto", 
                15:"Discussion",            16:"Fashion", 
                17:"Finance and Business",  18:"Food", 
                19:"Health and Fitness",    20:"Learning", 
                21:"Mindblowing",           22:"Outdoors",
                23:"Parenting",             24:"Photography", 
                25:"Relationships",         26:"Science", 
                27:"Video Games",           28:"Videos", 
                29:"Vroom",                 30:"Wholesome"
                
            }

i = 0
while i < len(training_subs):
    
    sub = training_subs[i]
    
    try:
        num = int(input(f"{sub}: "))
        print('\n')
        
        # If zero is entered to std in, then re-do the categorization for the previous
        # subreddit. 
        if (num == 0):
            i -= 1
            training.drop()

        else:
            category = categories[num]
            training.append({"SUB_NAME":sub, "CATEGORY":category})
            
            i += 1
    
    # If something other than an integer is passed to std in, then repeat the prompt for
    # the same subreddit name
    except ValueError:
        
        pass


