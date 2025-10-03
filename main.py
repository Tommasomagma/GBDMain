from getFeatures import stringFeatures
import pandas as pd
from helpers import *
import joblib
import numpy as np
import json

def run_tree(features: dict, tree: dict) -> int:

    node = tree
    path = []

    while node['type'] != 'leaf':
        feature = node['feature']
        threshold = node['threshold']
        if features[feature] <= threshold:
            path.append(f"{feature}({features[feature]}) <= {threshold} -> left")
            node = node['left']
        else:
            path.append(f"{feature}({features[feature]}) > {threshold} -> right")
            node = node['right']

    output = 0 if int(node['value']) == 1 else 1
    path.append(f"leaf value: {node['value']}")

    # At leaf, return 0 if floor(value) == 1 else 1 (invert)
    return output, path

if __name__ == "__main__":

    problemDescription = 'Whats $3\\cdot 4$?'
    answer = '["12"]'
    solutionString = '5*6=12'

    features = stringFeatures(solutionString, answer, problemDescription)
    features, featureNames = getFeaturesOrder(features)

    for j,k in enumerate(features.keys()):
        print(f'{k} // {featureNames[k]} // {features[k]}')
    
    # Load the JSON file containing your tree structure
    with open('drawingClassTree.json', 'r') as f:
        tree_structure_data = json.load(f)

    output, path = run_tree(features, tree_structure_data)

    print(path)
    print(output)


#REMOVE FEATURES:
#uniqueDigits
#ratioMath
#feature_11
#feature_19
#feature_24