import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score, fbeta_score, precision_score, recall_score


# Su dung sklearn
def transform_x52(value):
    return -value

df = pd.read_csv('./csv_file/new_export_2.csv')
df['x52'] = df['x52'].apply(transform_x52)
X = df[
    [
        "x11",
        "x12",
        "x21",
        "x22",
        "x23",
        "x24",
        "x31",
        "x32",
        "x41",
        "x42",
        "x43",
        "x51",
        "x52",
        "x61",
        "x71",
        "x72",
    ]
].values
y = df["label"].values


def labeling(scores): 
    label = []
    for score in scores:
        if  score < 580:
            label.append(0)
        elif score >=580 and score < 670:
            label.append(1)
        elif score >= 670 and score < 740:
            label.append(2)
        elif score >= 740 and score < 800:
            label.append(3)
        elif score >= 800 and score <=850:
            label.append(4)
    return label
def about(value):
    if value<0:
        return 0
    else:
        return int(value) 
def input(matrices, theta, y):
    # list_score = []
    # for i in range(len(matrices)):
    #     matric = matrices[i]
    #     # print(final_a[0] * np.dot(final_b[0], matric[0:2]), final_a[1] * np.dot(final_b[1], matric[2:6]), final_a[2] * np.dot(final_b[2], matric[6:8]), final_a[3] * np.dot(final_b[3], matric[8:11]), final_a[4] * about(np.dot(final_b[4], matric[11:13])), final_a[5] * np.dot(final_b[5], matric[13:14]), final_a[6] * np.dot(final_b[6], matric[14:16]))
    #     score = (np.dot(matric[0:2], theta[0:2]) + 
    #      np.dot(matric[2:6], theta[2:6]) +  
    #      np.dot(matric[6:8], theta[6:8]) + 
    #      np.dot(matric[8:11], theta[8:11]) + 
    #      about(np.dot(matric[11:13], theta[11:13])) +  
    #      np.dot(matric[13:14], theta[13:14]) +
    #      np.dot(matric[14:16], theta[14:16]))
    #     list_score.append(score)
    list_score = np.dot(matrices, theta)
    label = labeling(list_score)
    return np.array(label)


def valuate_f1_score(theta):  
    count = input(X, theta, y)
    return f1_score(count, y, average='micro')
def valuate_fbeta(theta):  
    count = input(X, theta, y)
    return fbeta_score(count, y, beta = 2, average='micro')
def valuate_precision_score(theta):  
    count = input(X, theta, y)
    return precision_score(count, y, average='micro')
def valuate_recall_score(theta):  
    count = input(X, theta, y)
    return recall_score(count, y, average='micro')


def calculate_accuracy_for_each_label(y_pred, y_true): 
    accuracies = [accuracy_score(y_true == i, y_pred == i) for i in set(y_true)]
    return accuracies
def accuracy_all(theta):
    count = input(X, theta, y)
    return np.array(calculate_accuracy_for_each_label(count, y))