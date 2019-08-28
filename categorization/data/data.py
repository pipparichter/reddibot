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

# Organizing data ---------------------------------------------

sub_names = load_subs()

training = pd.DataFrame()
training.columns = np.array(["SUB_NAME", "CATEGORY"])

test = pd.DataFrame()
test.columns = np.array(["SUB_NAME"])

