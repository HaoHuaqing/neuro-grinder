# -*- coding:utf-8 -*-

import os.path
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
EMG_folder = os.listdir('C:\\code\\EEG_Motion\\FES_S05_FR\\')
Motion_folder = os.listdir('C:\\code\\EEG_Motion\\Motion_S05\\')

def loadEMG(EMG_file):
    EMG_columns = [i * 8 + 1 for i in range(8)]
    EMG_filename = 'C:\\code\\EEG_Motion\\FES_S05_FR\\' + EMG_file
    EMG_data = np.loadtxt(EMG_filename,  # 文件名
                          delimiter=',',  # 分隔符
                          skiprows=(36),
                          dtype=float,  # 数据类型
                          usecols=EMG_columns)  # 指定读取的列索引号
    return EMG_data

def loadMotion(Motion_file):
    Motion_columns = [i for i in range(1, 16)]
    Motion_filename = 'C:\\code\\EEG_Motion\\Motion_S05\\' + Motion_file
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
        ['Time', 'PECTORALIS MAJOR: EMG 1', 'POSTERIOR DELTOID: EMG 2', 'ANTERIOR BRACHII: EMG 3', 'BICEPS BRACHII: EMG 4',
         'TRICEPS BRACHII LATERAL: EMG 5', 'TRICEPS BRACHII LONG: EMG 6', 'BRACHIORADIALIS: EMG 7',
         'EVENT MARKER: EMG 16'])
    Motion_title = np.array(
        ['Left Shoulder Flex / Time', 'Left Shoulder Rotation / Time', 'Left Shoulder Abduction / Time',
         'Left Elbow Flex / Time', 'Left Wrist Flex / Time', 'Left_acro_x', 'Left_acro_y', 'Left_acro_z',
         'Left_olec_x', 'Left_olec_y', 'Left_olec_z', 'Left_hand_x', 'Left_hand_y', 'Left_hand_z', 'Trigger	'])
    Merged_title = np.append(EMG_title, Motion_title)
    return Merged_title


def process(EMG_data, Motion_data, count):

    trigger1 = EMG_data[:, -1]
    trigger2 = Motion_data[:, -1]

    # capture data [trigger on - 0.5s, trigger off + 1s]
    EMG_trigger_list = [i for i, v in enumerate(trigger1) if v >= 0.005]
    Motion_trigger_list = [i for i, v in enumerate(trigger2) if v >= 2]
    # print(EMG_trigger_list[0],EMG_trigger_list[-1],Motion_trigger_list[0],Motion_trigger_list[-1])
    EMG_data = EMG_data[EMG_trigger_list[0]:EMG_trigger_list[-1]]
    Motion_data = Motion_data[Motion_trigger_list[0]:Motion_trigger_list[-1]]

    # visual trigger of EMG and Motion
    # plt.subplot(2, 1, 1)
    # plt.plot(trigger1)
    # plt.scatter(EMG_trigger_list[0], 0, c='red')
    # plt.scatter(EMG_trigger_list[-1], 0, c='red')
    # plt.title('EMG Trigger ' + str(count))
    # plt.subplot(2, 1, 2)
    # plt.plot(trigger2)
    # plt.scatter(Motion_trigger_list[0], 0, c='red')
    # plt.scatter(Motion_trigger_list[-1], 0, c='red')
    # plt.title('Motion Trigger')
    # plt.show()



    # EMG:1927HZ  Motion:120HZ  1927/120 = 16
    # resample Motion to 1000hz
    EMG_processed_data = np.array([[v for i, v in enumerate(EMG_data[:, 7]) if i % 2 == 0]])
    for count in range(1,8):
        x = np.array([[v for i, v in enumerate(EMG_data[:, 7 - count]) if i % 2 == 0]])
        EMG_processed_data = np.concatenate((EMG_processed_data, x), axis=0)
    Time_data = np.array([[i / 1000.0 for i in range(EMG_processed_data.shape[1])]])
    EMG_processed_data = np.concatenate((EMG_processed_data, Time_data), axis=0)
    EMG_processed_data = np.rot90(EMG_processed_data, 3)

    # Motion data interpolation
    x = np.linspace(0, len(Motion_data[:, 14]), len(Motion_data[:, 14]))
    y = Motion_data[:, 14]
    f = interpolate.interp1d(x, y, kind='linear')
    xnew = np.linspace(0, len(Motion_data[:, 14]), int(len(Motion_data[:, 14]) / 120 * 1000))
    Motion_processed_data = np.array([f(xnew)])
    for count in range(1,15):
        x = np.linspace(0, len(Motion_data[:, 14 - count]), len(Motion_data[:, 14 - count]))
        y = Motion_data[:, 14 - count]
        f = interpolate.interp1d(x, y, kind='linear')
        xnew = np.linspace(0, len(Motion_data[:, 14 - count]), int(len(Motion_data[:, 14 - count]) / 120 * 1000))
        ynew = np.array([f(xnew)])
        Motion_processed_data = np.concatenate((Motion_processed_data, ynew), axis=0)
    Motion_processed_data = np.rot90(Motion_processed_data, 3)
    Motion_processed_data = Motion_processed_data[:EMG_processed_data.shape[0]]
    # if not 0, something may be wrong.
    print(Motion_processed_data.shape[0] - EMG_processed_data.shape[0])

    EMG_processed_data = EMG_processed_data[:Motion_processed_data.shape[0]]
    Merged_data = np.concatenate((EMG_processed_data, Motion_processed_data), axis=1)
    return Merged_data

def mkdir(path):
    # make new folder for FR, LR
    import os

    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)
    if not isExists:
        print(path + ' success created')
        os.makedirs(path)
        return True
    else:
        print(path + ' already exist')
        return False

if __name__ == "__main__":
    FR_num = 13
    FR_folder = 'C:\\code\\EEG_Motion\\FR\\'
    mkdir(FR_folder)
    LR_folder = 'C:\\code\\EEG_Motion\\LR\\'
    mkdir(LR_folder)
    if len(EMG_folder) == len(Motion_folder):
        # data belong to FR and LR
        for count in range(FR_num):
            EMG_data = loadEMG(EMG_folder[count])
            print(EMG_folder[count])
            Motion_data = loadMotion((Motion_folder[count]))
            print(Motion_folder[count])
            Merged_title = title()
            Merged_data = process(EMG_data, Motion_data, count)
            with open('C:\\code\\EEG_Motion\\FR\\EMG_Motion_FR' + str(count) + '.csv', 'w', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(Merged_title)
                f_csv.writerows(Merged_data)
            print('FR '+ str(count) + ' of ' + str(FR_num) + ' completed')

        for count in range(FR_num, len(EMG_folder)):
            EMG_data = loadEMG(EMG_folder[count])
            print(EMG_folder[count])
            Motion_data = loadMotion((Motion_folder[count]))
            print(Motion_folder[count])
            Merged_title = title()
            Merged_data = process(EMG_data, Motion_data, count)
            with open('C:\\code\\EEG_Motion\\LR\\EMG_Motion_LR' + str(count - FR_num) + '.csv', 'w', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(Merged_title)
                f_csv.writerows(Merged_data)
            print('LR ' + str(count - FR_num) + ' of ' + str(len(EMG_folder) - FR_num) + ' completed')
    else:
        print('EMG files number is not equal to Motion files number.')








