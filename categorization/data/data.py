import pandas as pd
import sys
sys.path.append("../../sub_data/")

# Loading sub names -------------------------------------------

def load_subs():
    with open("../../sub_data/sub_data.csv", 'r') as f:
        df = pd.read_csv(f)
    return df

sub_data = load_subs()
 

# For deciding a useful training dataset size, this post is helpful: 
# https://www.researchgate.net/post/Is_there_an_ideal_ratio_between_a_training_set_and_
# validation_set_Which_trade-off_would_you_suggest

# For now, I'll probably ignore the validation set and just see how to first
# part turns out

# The entire dataset is probably around 3,000 subreddits (why so few?)


# Creating the training and test data -----------------------------------------------

# Create lists to hold the data 
test_subs = []
training_subs = [[], []]
print(sub_data)
for i in range(len(sub_data.index)):
    print(i)
    sub = sub_data.iloc[i]
    # Testing if the value in the CATEGORY column is NaN
    if sub["CATEGORY"] != sub["CATEGORY"]:
        test_subs.append(sub["SUB_NAME"])
    else:
        training_subs[0].append(sub["SUB_NAME"])
        training_subs[1].append(sub["CATEGORY"])

test = pd.DataFrame({"SUB_NAME":test_subs})
test.to_csv("./test_data.csv")

training = pd.DataFrame({"SUB_NAME":training_subs[0], "CATEGORY":training_subs[1]})
training.to_csv("./training_data.csv")

