import matplotlib.pyplot as plt
from function.valuate import precision_score, recall_score
import numpy as np

def visualize_precision(y_pred, y_true):
    
    # Tính precision và recall
    precision = precision_score(y_pred, y_true,average=None)
    recall = recall_score(y_pred, y_true,average=None)

    labels = np.unique(y_true)
    width = 0.35
    
    
    # Tạo biểu đồ cột cho precision và recall
    fig, ax = plt.subplots()
    precision_bars = ax.bar(labels - width/2, precision, width, label='Precision')
    recall_bars = ax.bar(labels + width/2, recall, width, label='Recall')

    # Hiển thị giá trị đã có trực tiếp trên biểu đồ
    ax.bar_label(precision_bars, fmt='%.2f', label_type='edge', fontsize=8)
    ax.bar_label(recall_bars, fmt='%.2f', label_type='edge', fontsize=8)

    ax.set_xlabel('Class Label')
    ax.set_ylabel('Score')
    ax.set_title('Precision and Recall for Each Class')
    ax.set_xticks(labels)
    ax.legend()
    plt.show()
    
def change_value(values):
    plt.plot(values, linestyle='-')
    plt.xlabel('Gia tri fitness')
    plt.ylabel('Values')
    plt.title('Biểu đồ biến đổi của fitness')
    last_value = values[-1]
    plt.text(len(values) - 1, last_value, f'   {last_value}', verticalalignment='bottom')
    plt.show()
    
def ratio_chart_true_label(accuracy_list):
    label_name = ['label_0','label_1', 'label_2','label_3', 'label_4']
    indices = list(range(1, len(accuracy_list) + 1))

    # Vẽ biểu đồ cột
    plt.bar(indices, accuracy_list, color='blue')

    plt.title('Biểu đồ tỉ lệ gán nhãn đúng')
    plt.xlabel('Nhãn')
    plt.ylabel('Giá trị điểm tín dụng')

    for i, v in enumerate(accuracy_list):
        plt.text(i + 1, v + 0.01, f'\n{v*100:.2f}%', ha='center', va='bottom', color='black')

    # Đặt nhãn trục x
    plt.xticks(indices, label_name)
    plt.grid(True)
    plt.show()
    
def confuse_chart(confuse):
    for key1, inner_dict in confuse.items():
        labels = list(inner_dict.keys())
        values = list(inner_dict.values())

        # Tạo biểu đồ cột cho từng key1
        plt.bar(labels, values)
        
        # Ghi số lượng trên từng cột
        for label, value in zip(labels, values):
            plt.text(label, value + 5, str(value), ha='center', va='bottom')
        
        plt.xlabel(f'Label {key1}')
        plt.ylabel('So luong gan sai nhan')
        plt.title(f'Bieu do label bi sai (true label = {key1})')
        plt.xticks([0, 1, 2, 3, 4])
        plt.show()