# -*- coding:utf-8 -*-

import os.path
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
EMG_folder = os.listdir('C:\\code\\EEG_Motion\\Subject_16_EXP1\\FES_Subject_16\\')
Motion_folder = os.listdir('C:\\code\\EEG_Motion\\Subject_16_EXP1\\Subject16_e1\\')

def loadEMG(EMG_file):
    EMG_columns = [i * 8 + 1 for i in range(8)]
    EMG_filename = 'C:\\code\\EEG_Motion\\Subject_16_EXP1\\FES_Subject_16\\' + EMG_file
    EMG_data = np.loadtxt(EMG_filename,  # 文件名
                          delimiter=',',  # 分隔符
                          skiprows=(36),
                          dtype=float,  # 数据类型
                          usecols=EMG_columns)  # 指定读取的列索引号
    return EMG_data

def loadMotion(Motion_file):
    Motion_columns = [i for i in range(1, 16)]
    Motion_filename = 'C:\\code\\EEG_Motion\\Subject_16_EXP1\\Subject16_e1\\' + Motion_file
    Motion_data = np.loadtxt(Motion_filename,  # 文件名
                             skiprows=(9),
                             dtype=float,  # 数据类型
                             usecols=Motion_columns)  # 指定读取的列索引号
    return Motion_data

# Motion data has lots of spaces, cant recognize delimiters
# EMG encoded mode problem
# EMG_title = np.loadtxt(EMG_filename,      # 文件名
#                             delimiter=',', # 分隔符
#                             skiprows=(35),
#                             dtype=str,     # 数据类型
#                             usecols=EMG_columns) # 指定读取的列索引号
# EMG_title = EMG_title[0]
def title():
    EMG_title = np.array(
        ['PECTORALIS MAJOR: EMG 1', 'POSTERIOR DELTOID: EMG 2', 'ANTERIOR BRACHII: EMG 3', 'BICEPS BRACHII: EMG 4',
         'TRICEPS BRACHII LATERAL: EMG 5', 'TRICEPS BRACHII LONG: EMG 6', 'BRACHIORADIALIS: EMG 7',
         'EVENT MARKER: EMG 16'])
    Motion_title = np.array(
        ['Left Shoulder Flex / Time', 'Left Shoulder Rotation / Time', 'Left Shoulder Abduction / Time',
         'Left Elbow Flex / Time', 'Left Wrist Flex / Time', 'Left_acro_x', 'Left_acro_y', 'Left_acro_z',
         'Left_olec_x', 'Left_olec_y', 'Left_olec_z', 'Left_hand_x', 'Left_hand_y', 'Left_hand_z', 'Trigger	'])
    Merged_title = np.append(EMG_title, Motion_title)
    return Merged_title


def process(EMG_data, Motion_data):
    # visual data
    trigger1 = EMG_data[:, -1]
    trigger2 = Motion_data[:, -1]
    # plt.subplot(2, 1, 1)
    # plt.plot(trigger1)
    # plt.subplot(2, 1, 2)
    # plt.plot(trigger2)
    # plt.show()

    # capture data
    EMG_trigger_list = [i for i, v in enumerate(trigger1) if v >= 0.005]
    Motion_trigger_list = [i for i, v in enumerate(trigger2) if v >= 2]
    EMG_data = EMG_data[EMG_trigger_list[0]:EMG_trigger_list[-1]]
    Motion_data = Motion_data[Motion_trigger_list[0]:Motion_trigger_list[-1]]
    # print(EMG_trigger_list[-1])

    # EMG:1927HZ  Motion:120HZ  1927/120 = 16
    # Sample EMG every 16 points
    EMG_processed_data = np.array([[v for i, v in enumerate(EMG_data[:, 7]) if i % 16 == 0]])
    for count in range(1, 8):
        x = np.array([[v for i, v in enumerate(EMG_data[:, 7 - count]) if i % 16 == 0]])
        EMG_processed_data = np.concatenate((EMG_processed_data, x), axis=0)
    EMG_processed_data = np.rot90(EMG_processed_data, 3)
    EMG_processed_data = EMG_processed_data[:Motion_data.shape[0]]

    Merged_data = np.concatenate((EMG_processed_data, Motion_data), axis=1)
    return Merged_data


if __name__ == "__main__":
    if len(EMG_folder) == len(Motion_folder):
        for count in range(len(EMG_folder)):
            EMG_data = loadEMG(EMG_folder[count])
            Motion_data = loadMotion((Motion_folder[count]))
            Merged_title = title()
            Merged_data = process(EMG_data, Motion_data)
            with open('EMG_Motion' + str(count) + '.csv', 'w', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(Merged_title)
                f_csv.writerows(Merged_data)
            print(str(count + 1) + ' of ' + str(len(EMG_folder)) + ' completed')
    else:
        print('EMG files number is not equal to Motion files number.')








