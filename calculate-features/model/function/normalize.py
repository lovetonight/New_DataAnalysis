import numpy as np

def calculate_features(sub_features):
    sum = sub_features.sum()
    b = (1/sum)*sub_features
    a = sub_features[0]/b[0]
    return(a , b )

def normalize_theta(theta):
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
    final_b[4][-1]= -final_b[4][-1] 
    final_a = final_a/np.array(final_a).sum()
    return final_a, final_b