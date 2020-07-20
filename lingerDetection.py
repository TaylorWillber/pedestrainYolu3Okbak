import sys
import cv2

sys.setrecursionlimit(1000000)
# 保存轨迹坐标
kCollection = []
# 保存轨迹变化点
flag_changer = False
"""
将center的y向下移动20个点
"""
# 坐标连续个数
num_constant = 5
# 在该点处斜率开始发生变化
first_change_point = []
# 图片的下标
imgIndex = 0
# 用来保存基点
base_point = []
#
differ_points = []

zero_one = []


def counterNum(kCollection, img):
    postive = 0
    negstive = 0
    ps_tp = []
    ng_tp = []
    num = 0
    counter_list = []
    for i in range(len(kCollection)):
        if kCollection[i] >= 0:
            postive += 1

            num += 1
            ps_tp.append(kCollection[i])
            if len(ng_tp) > 0:
                counter_list.append([-1, ng_tp, len(ng_tp)])
                negstive = 0
            ng_tp = []
            if kCollection[-1] > 0 and len(kCollection) == num:
                print(postive)
                counter_list.append([1, kCollection[len(kCollection) - postive:], postive])
        else:
            num += 1
            negstive += 1

            ng_tp.append(kCollection[i])
            if len(ps_tp) > 0:
                counter_list.append([1, ps_tp, len(ps_tp)])
                postive = 0
            ps_tp = []

            if kCollection[-1] < 0 and len(kCollection) == num:
                counter_list.append([-1, kCollection[len(kCollection) - negstive:], negstive])

    # print("counter_list",counter_list)
    count_ne = 0
    count_ps = 0
    #
    tp = []
    # for k in range(len(counter_list)):
    #     if counter_list[k][2] > 10:
    #         tp.append([counter_list[k][0],counter_list[k][2]])
    for k in range(len(counter_list)):
        if counter_list[k][2] > 5:
            tp.append([counter_list[k][0],counter_list[k][2]])


    #合并数据
    if len(tp) > 3:
        for k in range(len(tp) - 1):
            if tp[k][0] == tp[k + 1][0]:
                tp[k + 1][1] += tp[k][1]
                tp[k][0] = 0

    # print("tp",tp)
    tp1 = []
    for i in range(len(tp)):
        if tp[i][0] != 0 and tp[i][1] >= 10:
            tp1.append(tp[i])
    # print("tp1",tp1)
    #tp [[-1, 25], [0, 24], [1, 33], [0, 19], [0, 28], [0, 34], [0, 40], [0, 49], [-1, 56], [0, 8], [0, 17], [0, 25], [1, 51], [0, 7], [-1, 51], [0, 14], [1, 27]]
    #tp1 [[-1, 25], [1, 33], [-1, 56], [1, 51], [-1, 51], [1, 27]]
    counter_list = tp1
    global imgIndex
    res_list = []
    # for j in range(len(counter_list)):
    #     if counter_list[j][2] > 10 and counter_list[j][0] == 1:
    #         count_ps += 1
    #     if counter_list[j][2] > 10 and counter_list[j][0] == -1:
    #         count_ne += 1
    #     print(counter_list[j][0], " ", counter_list[j][2])

    # for j in range(len(counter_list)):
    #     if counter_list[j][1] > 10 and counter_list[j][0] == 1:
    #         count_ps += 1
    #     if counter_list[j][1] > 10 and counter_list[j][0] == -1:
    #         count_ne += 1
        # print(counter_list[j][0], " ", counter_list[j][1])
    for j in range(len(counter_list)):
        if counter_list[j][0]==1:
            if counter_list[j][1] > 80:
                count_ne = 0
                count_ps = 0
            count_ps += 1
        else:
            if counter_list[j][1] > 80:
                count_ne = 0
                count_ps = 0
            count_ne += 1
    # print(counter_list)

    global flag_changer, imgIndex
    if (count_ps >= 3 and count_ne >= 2) or (count_ps >= 2 and count_ne >= 3):
        flag_changer = True
        imgIndex += 1


def lingerdetection(center_point, img):
    global kCollection
    # print("center_point", center_point)
    base_point.append(center_point)
    if len(base_point) > 1:
        k = base_point[-1][1] / base_point[-1][0] - base_point[-2][1] / base_point[-2][0]
        kCollection.append(k)
        counterNum(kCollection, img)

    # kCollection.append(center_point[1] / center_point[0])
    # print(kCollection)
    # kCollection.append(float("%.3f" % center_point[1] / center_point[0]))
