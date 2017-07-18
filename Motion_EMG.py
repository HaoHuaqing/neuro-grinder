# -*- coding:utf-8 -*-

import os.path
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def loadEMG(EMG_file, Subject_num):
    EMG_columns = [i * 8 + 1 for i in range(8)]
    EMG_filename = 'C:\\data\\data\\s' + Subject_num + '\\EMG\\' + EMG_file
    EMG_data = np.loadtxt(EMG_filename,  # 文件名
                          delimiter=',',  # 分隔符
                          skiprows=(36),
                          dtype=float,  # 数据类型
                          usecols=EMG_columns)  # 指定读取的列索引号
    return EMG_data

def loadMotion(Motion_file, Subject_num):
    Motion_columns = [i for i in range(1, 16)]
    Motion_filename = 'C:\\data\\data\\s' + Subject_num + '\\Motion\\' + Motion_file
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

    # capture data [trigger on - 0.3s, trigger off + 1s]
    EMG_trigger_list = [i for i, v in enumerate(trigger1) if v >= 0.005]
    Motion_trigger_list = [i for i, v in enumerate(trigger2) if v >= 2]
    global glob_EMG_s
    glob_EMG_s = EMG_trigger_list[0]
    global glob_EMG_e
    glob_EMG_e = EMG_trigger_list[-1]
    global glob_Motion_s
    glob_Motion_s = Motion_trigger_list[0]
    global glob_Motion_e
    glob_Motion_e = Motion_trigger_list[-1]
    # visual trigger of EMG and Motion
    # EMG start
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(trigger1)
    rects = ax.bar(EMG_trigger_list[0], 0.01, width=500, color='r')
    drs = []
    for rect in rects:
        dr = DraggableRectangleEMGS(rect, trigger1)
        dr.connect()
        drs.append(dr)
    plt.title('EMG Trigger ' + str(count) + ' Start')
    plt.show()

    # EMG end
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(trigger1)
    rects = ax.bar(EMG_trigger_list[-1], 0.01, width=500, color='r')
    drs = []
    for rect in rects:
        dr = DraggableRectangleEMGE(rect, trigger1)
        dr.connect()
        drs.append(dr)
    plt.title('EMG Trigger ' + str(count) + ' End')
    plt.show()

    # Motion start
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(trigger2)
    rects = ax.bar(Motion_trigger_list[0], 2.5, width=50, color='r')
    drs = []
    for rect in rects:
        dr = DraggableRectangleMotionS(rect, trigger2)
        dr.connect()
        drs.append(dr)
    plt.title('Motion Trigger ' + str(count) + ' Start')
    plt.show()

    # Motion end
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(trigger2)
    rects = ax.bar(Motion_trigger_list[-1], 2.5, width=50, color='r')
    drs = []
    for rect in rects:
        dr = DraggableRectangleMotionE(rect, trigger2)
        dr.connect()
        drs.append(dr)
    plt.title('Motion Trigger ' + str(count) + ' End')
    plt.show()


    print(glob_EMG_s)
    EMG_data = EMG_data[glob_EMG_s-578:glob_EMG_e+1927]
    Motion_data = Motion_data[glob_Motion_s-36:glob_Motion_e+120]
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

class DraggableRectangleEMGS:
    def __init__(self, rect, trigger):
        self.rect = rect
        self.press = None
        self.trigger = trigger
        self.x = 0
        self.emg_trigger_list = 0

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.x = x0+dx
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.emg_trigger_list = [i for i, v in enumerate(self.trigger[int(self.x):]) if v >= 0.005]
        self.rect.set_x(self.emg_trigger_list[0] + self.x)
        self.rect.set_y(0)
        self.rect.figure.canvas.draw()
        global glob_EMG_s
        glob_EMG_s = int(self.emg_trigger_list[0] + self.x)


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

class DraggableRectangleEMGE:
    def __init__(self, rect, trigger):
        self.rect = rect
        self.press = None
        self.x = 0
        self.trigger = trigger
        self.emg_trigger_list = 0

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.x = x0+dx
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.emg_trigger_list = [i for i, v in enumerate(self.trigger[:int(self.x)]) if v >= 0.005]
        self.rect.set_x(self.emg_trigger_list[-1])
        self.rect.set_y(0)
        self.rect.figure.canvas.draw()
        global glob_EMG_e
        glob_EMG_e = int(self.emg_trigger_list[-1])


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

class DraggableRectangleMotionS:
    def __init__(self, rect, trigger):
        self.rect = rect
        self.press = None
        self.trigger = trigger
        self.x = 0
        self.emg_trigger_list = 0

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.x = x0+dx
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.motion_trigger_list = [i for i, v in enumerate(self.trigger[int(self.x):]) if v >= 2]
        self.rect.set_x(self.motion_trigger_list[0] + self.x)
        self.rect.set_y(0)
        self.rect.figure.canvas.draw()
        global glob_Motion_s
        glob_Motion_s = int(self.motion_trigger_list[0] + self.x)


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

class DraggableRectangleMotionE:
    def __init__(self, rect, trigger):
        self.rect = rect
        self.press = None
        self.x = 0
        self.trigger = trigger
        self.emg_trigger_list = 0

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.x = x0+dx
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.motion_trigger_list = [i for i, v in enumerate(self.trigger[:int(self.x)]) if v >= 2]
        self.rect.set_x(self.motion_trigger_list[-1])
        self.rect.set_y(0)
        self.rect.figure.canvas.draw()
        global glob_Motion_e
        glob_Motion_e = int(self.motion_trigger_list[-1])


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)


if __name__ == "__main__":
    Subject_num = '20'
    EMG_folder = os.listdir('C:\\data\\data\\s' + Subject_num + '\\EMG\\')
    Motion_folder = os.listdir('C:\\data\\data\\s' + Subject_num + '\\Motion\\')
    FR_num = 10
    FR_folder = 'C:\\data\\pro_data2\\FR\\'
    mkdir(FR_folder)
    LR_folder = 'C:\\data\\pro_data2\\LR\\'
    mkdir(LR_folder)
    if len(EMG_folder) == len(Motion_folder):
        # data belong to FR and LR
        for count in range(FR_num):
            EMG_data = loadEMG(EMG_folder[count], Subject_num)
            print(EMG_folder[count])
            Motion_data = loadMotion(Motion_folder[count], Subject_num)
            print(Motion_folder[count])
            Merged_title = title()
            Merged_data = process(EMG_data, Motion_data, count)
            with open('C:\\data\\pro_data2\\FR\\EMG_Motion_FR' + str(count) + '.csv', 'w', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(Merged_title)
                f_csv.writerows(Merged_data)
            print('FR '+ str(count) + ' of ' + str(FR_num) + ' completed')

        for count in range(FR_num, len(EMG_folder)):
            EMG_data = loadEMG(EMG_folder[count], Subject_num)
            print(EMG_folder[count])
            Motion_data = loadMotion(Motion_folder[count], Subject_num)
            print(Motion_folder[count])
            Merged_title = title()
            Merged_data = process(EMG_data, Motion_data, count)
            with open('C:\\data\\pro_data2\\LR\\EMG_Motion_LR' + str(count - FR_num) + '.csv', 'w', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(Merged_title)
                f_csv.writerows(Merged_data)
            print('LR ' + str(count - FR_num) + ' of ' + str(len(EMG_folder) - FR_num) + ' completed')
    else:
        print('EMG files number is not equal to Motion files number.')








