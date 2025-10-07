from getFeatures import stringFeatures
import pandas as pd
from helpers import *
import joblib
import numpy as np
import json

def run_tree(features: dict, featureNames: list, tree: dict) -> int:

    node = tree
    path = []

    while node['type'] != 'leaf':
        feature = node['feature']
        threshold = node['threshold']
        if features[feature] <= threshold:
            path.append(f"{featureNames[feature]} ({features[feature]}) <= {threshold} -> left")
            node = node['left']
        else:
            path.append(f"{featureNames[feature]} ({features[feature]}) > {threshold} -> right")
            node = node['right']

    output = 0 if int(node['value']) == 1 else 1
    path.append(f"leaf value: {node['value']}")

    return output, path

def addBonusFeatures(features, tools):

    if features['feature_14'] < 3:
        print('DIGITS BONUS')
        features['feature_14'] = 3
        if features['feature_20'] == 1 and features['feature_22'] < 0.055:
            features['feature_22'] = 0.1
        if features['feature_20'] == 1 and features['feature_16'] == 0:
            features['feature_16'] = 1
        return features
    if features['feature_22'] < 0.055:
        print('RATIO DIGITS BONUS')
        features['feature_22'] = 0.1
        return features
    if features['feature_16'] == 0:
        print('OPS BONUS')
        features['feature_16'] = 1
        return features

    return features

if __name__ == "__main__":

    df = pd.read_csv('dataFigure/inData.csv')

    for i in df.index[20:]:

        problemDescription = df['problem'][i]
        answer = df['answer'][i]
        solutionString = df['solString'][i]
        tools = eval(df['tools'][i])
        label = df['label'][i]

        features = stringFeatures(solutionString, answer, problemDescription)
        features, featureNames = getFeaturesOrder(features)

        features = addBonusFeatures(features, tools)

        # for j,k in enumerate(features.keys()):
        #     print(f'{k} // {featureNames[k]} // {features[k]}')
        
        # Load the JSON file containing your tree structure
        with open('drawingClassTree.json', 'r') as f:
            tree_structure_data = json.load(f)

        output, path = run_tree(features, featureNames, tree_structure_data)
        
        print(problemDescription)
        print(answer)
        print(solutionString)
        print(tools)
        print(path)
        print(f'Pred:{output}/True:{label}')
        show_img(f'https://cdn.magmamath.com/solutions/{df['drawing_image_name'][i]}')




# feature_0 // mean_t // 300.0
# feature_1 // mean_diff_t // 0.0
# feature_2 // std_t // 1000.0
# feature_3 // std_diff_t // 30000.0
# feature_4 // t_total // 0.0
# feature_5 // mean_w // 0.0
# feature_6 // mean_h // 50.0
# feature_7 // std_w // 0.0
# feature_8 // std_h // 50.0
# feature_9 // dense // 0.1
# feature_10 // free // 10.0
# feature_11 // erase // 0.0
# feature_12 // clear // 0.0
# feature_13 // strokeCount // 10.0
# feature_14 // digits // 2.0
# feature_15 // singleDigits // 4.0
# feature_16 // ops // 1.0
# feature_17 // ratioFormat // 1.0
# feature_18 // varsProblem // 0.0
# feature_19 // ratioVars // 0.0
# feature_20 // ans // 0.0
# feature_21 // problemExpected // 0.0
# feature_22 // ratioDigits // 1.0
# feature_23 // ratioSingleDigits // 1.0
# feature_24 // ratioOps // 1.0
# feature_25 // ratioProblem // 1.0
# feature_26 // mathRatio // 0.0
# feature_27 // digitsProblem // 0.0
# feature_28 // opsProblem // 0.0