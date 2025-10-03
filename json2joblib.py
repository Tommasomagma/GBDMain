from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
import json

def synthesize_data_from_json(json_tree, feature_names=None):
    features = set()
    paths = []

    # Walk all paths, collecting constraints-to-leaf and their assigned value
    def walk(node, conditions):
        if node['type'] == 'leaf':
            paths.append((conditions.copy(), node['value']))
            return
        feature = node['feature']
        threshold = node['threshold']
        # left: feature <= threshold
        walk(node['left'], conditions + [(feature, '<=', threshold)])
        # right: feature > threshold
        walk(node['right'], conditions + [(feature, '>', threshold)])

    walk(json_tree, [])
    all_features = {c[0] for path, _ in paths for c in path}
    X, y = [], []
    feature_index = {f: i for i, f in enumerate(all_features)}
    for conds, label in paths:
        x = [0.5] * len(all_features)  # Default all features
        for feat, op, thresh in conds:
            idx = feature_index[feat]
            if op == '<=':
                x[idx] = thresh - 0.01
            else:
                x[idx] = thresh + 0.01
        X.append(x)
        y.append(label)
    return np.array(X), np.array(y)


if __name__ == "__main__":

    featureNames = [f'feature_{i}' for i in range(27)]

    # Load JSON
    with open('drawingClassTree.json', 'r', encoding='utf-8-sig') as f:
        json_tree = json.load(f)

    # Rebuild synthetic data
    X, y = synthesize_data_from_json(json_tree, featureNames)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Fit a new scikit-learn DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    clf.fit(X, y_encoded)

    joblib.dump(clf, "drawingClassTree.joblib")
