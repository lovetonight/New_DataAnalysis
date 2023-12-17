from collections import defaultdict
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
y_true = df["label"].values


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
        elif score >= 800:
            label.append(4)
    return label
def about(value):
    if value<0:
        return 0
    else:
        return int(value) 
def predict(matrices, theta):
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

#f1_score
def valuate_f1_score(theta):  
    y_pred = predict(X, theta)
    return f1_score(y_pred, y_true, average='micro')

#fbeta
def valuate_fbeta(theta):  
    y_pred = predict(X, theta)
    return fbeta_score(y_pred, y_true, beta = 2, average='micro')

#precision
def valuate_precision_score(theta):  
    y_pred = predict(X, theta)
    return precision_score(y_pred, y_true, average='micro')

#recall
def valuate_recall_score(theta):  
    y_pred = predict(X, theta)
    return recall_score(y_pred, y_true, average='micro')

def precision_recall(theta):  
    y_pred = predict(X, theta)
    return precision_recall(y_pred, y_true, average='micro'), recall_score(y_pred, y_true, average='micro')


def calculate_accuracy_for_each_label(y_pred, y_true): 
    y_pred1 = defaultdict(int)
    y_pred2 = defaultdict(int)
    confuse = defaultdict(dict)
    acurracy = []
    for y_p, y_t in zip(y_pred, y_true):
        y_pred2[y_t] +=1
        if y_p == y_t:
            y_pred1[y_t] +=1
        else:
            if confuse[y_t].get(y_p) is None:
                confuse[y_t][y_p] = 1
            else:
                confuse[y_t][y_p] +=1
    for i in range(0, 5):
        acurracy.append(y_pred1[i]/y_pred2[i])
    return np.array(acurracy), confuse

def get_yp_yt(theta):
    y_pred = predict(X, theta)
    return y_pred, y_true
      
def accuracy_all(theta):
    y_pred = predict(X, theta)
    acurracy, confuse = calculate_accuracy_for_each_label(y_pred, y_true)
    return acurracy, confuse

def get_max_confuse_label(theta):
    y_pred = predict(X, theta)
    acurracy, confuse = calculate_accuracy_for_each_label(y_pred,y_true)
    max_values_per_key = {}

    for outer_key, inner_dict in confuse.items():
        max_inner_key = max(inner_dict, key=inner_dict.get)
        max_values_per_key[outer_key] = {max_inner_key: inner_dict[max_inner_key]}
    return max_values_per_key



    