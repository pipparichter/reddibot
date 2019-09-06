import forest_tools

forest = forest_tools.RandomForest()

for tree in forest.trees:
    print(tree.root.data[0].name)
