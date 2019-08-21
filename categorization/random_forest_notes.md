# Random forest notes

## Creating a binary decision tree

Note that binary decision trees are usually preferable to a decision tree created by multiway splitting, as it is less
likely to result in **overfitting**. Overfitting is "the production of an analysis that corresponds too closely or exactly to
a particular set of data, and may therefore fail to fit additional data or predict future observations reliably"
([Wikipedia][1]). This is because it breaks the dataset into too many subsets too quickly.  

### 1. Splitting the dataset
*Note that for k classes, there are 2^(k-1) - 1 possible splits ([Hoare][3]), which is terrible. My k value 
is however many categories I am trying to sort the subreddits into.* <br/>
<br/>
Each split of the dataset is made with respect to a single attribute (i.e. whether or not a word is present in the 
subreddit name). Then, how 'useful' each split is is determined using the Gini index (see below). The 'best'
split is the one used in the tree ([Brownlee][2]). <br/>
<br/>
All of my predictor variables are categorical, and have only two possible states (true/false), which is nice because 
that's conducive to creating a BINARY decision tree (as opposed to multiway). 

### 2. Calculate the Gini index
The Gini index is used to evaluate how effective each split of the dataset was at categorizing the data. It is calculated
using the following formula: <br/>

<p align="center"> `# proportion = count(category_n)/count() 
                    proportion1 = `

[1]: https://en.wikipedia.org/wiki/Overfitting
[2]: https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
[3]: https://www.displayr.com/how-is-splitting-decided-for-decision-trees/

## Creating a random forest
