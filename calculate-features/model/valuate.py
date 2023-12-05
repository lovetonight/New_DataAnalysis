from collections import defaultdict
import numpy as np
import pandas as pd



def about(value, _min=300, _max=850):
    if value < _min:
        value = _min
    elif value > _max:
        value = _max
    return int(value)


def check_acc(label, score):
    if label == 1:
        if score >= 300 and score <= 580:
            return True
        else:
            return False
    if label == 2:
        if score > 580 and score <= 670:
            return True
        else:
            return False
    if label == 3:
        if score > 670 and score <= 740:
            return True
        else:
            return False
    if label == 4:
        if score > 740 and score <= 800:
            return True
        else:
            return False
    if label == 5:
        if score > 800 and score <= 850:
            return True
        else:
            return False


def input(matrices, final_a, final_b, y):
    count = defaultdict(int)
    list_score = []
    for i in range(len(matrices)):
        matric = matrices[i]
        score = (
            final_a[0] * np.dot(final_b[0], matric[0:2])
            + final_a[1] * np.dot(final_b[1], matric[2:6])
            + final_a[2] * np.dot(final_b[2], matric[6:8])
            + final_a[3] * np.dot(final_b[3], matric[8:11])
            + final_a[4] * about(np.dot(final_b[4], matric[11:13]))
            + final_a[5] * np.dot(final_b[5], matric[13:14])
            + final_a[6] * np.dot(final_b[6], matric[14:16])
        )
        if check_acc(y[i], score):
            count[y[i]] += 1
    return count


def fn_combined_features(features):
    combined = []
    for items in features:
        tmp = []
        for index, item in enumerate(items):
            for _ in item:
                tmp.append(_)
        combined.append(tmp)
    return np.array(combined, dtype=object)


def calculate_features(sub_features):
    sum = sub_features.sum()
    b = (1 / sum) * sub_features
    a = sub_features[0] / b[0]
    return (a, b)


def valuate(theta):
    
    
    df = pd.read_csv(f"../export.csv")
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
    theta = theta.reshape(-1, 1)
    ab1 = theta[0:2]
    ab2 = theta[2:6]
    ab3 = theta[6:8]
    ab4 = theta[8:11]
    ab5 = theta[11:13]
    ab6 = theta[13:14]
    ab7 = theta[14:16]
    ab_all = [ab1, ab2, ab3, ab4, ab5, ab6, ab7]
    final_a = []
    final_b = []
    for ab in ab_all:
        a, b = calculate_features(ab)
        final_a.append(a)
        final_b.append(b)
        # print(calculate_features(ab))
    final_b[4][-1] = -final_b[4][-1]
    final_a = final_a / np.array(final_a).sum()
    final_b = fn_combined_features(final_b)
    count = input(X, final_a, final_b, y)
    
    count_label = {}
    # Đếm số lần xuất hiện của mỗi label trong y
    for label in y:
        if label in count_label:
            count_label[label] += 1
        else:
            count_label[label] = 1
    accuracy_list = [count[tmp]/count_label[tmp] for tmp in count_label]
    return accuracy_list