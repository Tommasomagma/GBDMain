# pip3 install matplotlib pillow requests numpy
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import requests

def show_img(url):

    url = url
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show(block=False)
    go = input('close')
    plt.close()


def getFeaturesOrder(features):

    featuresOrder = [
    'mean_t',
    'mean_diff_t',
    'std_t',
    'std_diff_t',
    't_total',
    'mean_w',
    'mean_h',
    'std_w',
    'std_h',
    'dense',
    'free',
    'erase',
    'clear',
    'strokeCount',
    'digits',
    'singleDigits',
    'ops',
    'ratioFormat',
    'varsProblem',
    'ratioVars',
    'ans',
    'problemExpected',
    'ratioDigits',
    'ratioSingleDigits',
    'ratioOps',
    'ratioProblem',
    'mathRatio',
    'digitsProblem',
    'opsProblem',
    ]

    featureNames = {}

    for i in range(len(featuresOrder)):
        featureNames[f'feature_{i}'] = featuresOrder[i]

    featureValues = {
    "mean_t": features["mean_t"],
    "mean_diff_t": features["mean_diff_t"],
    "std_t": features["std_t"],
    "std_diff_t": features["std_diff_t"],
    "t_total": features["max_min_diff"],
    "mean_w": features["mean_w"],
    "mean_h": features["mean_h"],
    "std_w": features["std_w"],
    "std_h": features["std_h"],
    "dense": features["dense"],
    "free": features["free"],
    "erase": features["erase"],
    "clear": features["clear"],
    "strokeCount": features["free"] + features["erase"],
    "digits": features["digits"],
    "singleDigits": features["singleDigits"],
    "ops": features["ops"],
    "ratioFormat": features["ratioFormat"],
    "varsProblem": features["varsProblem"],
    "ratioVars": features["ratioVars"],
    "ans": features["ans"],
    "problemExpected": features["problemExpected"],
    "ratioDigits": features["ratioDigits"],
    "ratioSingleDigits": features["ratioSingleDigits"],
    "ratioOps": features["ratioOps"],
    "ratioProblem": features["ratioProblem"],
    "mathRatio": features["mathRatio"],
    "digitsProblem": features["digitsProblem"],
    "opsProblem": features["opsProblem"],
    }

    orderedFeatures = {}

    for key in featureNames:
        orderedFeatures[key] = float(featureValues[featureNames[key]])

    return orderedFeatures, featureNames
