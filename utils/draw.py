from kafka import KafkaProducer
import cv2

import linger

point_of_line = []
# 2048-1    32768-1       1048576-1
palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


"""
在draw_boxes中img是帧
"""

point_of_line_bottom = []
imgIndex = 0


# def draw_boxes(img, bbox, identities=None, offset=(0, 0)):
def draw_boxes(img, bbox, identities=None, detection_numbers=0, tracking_numbers=0, offset=(0, 0)):
    global imgIndex,path, img1
    imgIndex += 1
    path = ''
    # cv2.imwrite("/home/rc/Desktop/Project/pedestrainYolu3/output/img1.jpg", img)
    # print("detection_numbers ", detection_numbers," tracking_numbers ",tracking_numbers )
    global flage, point_of_line_bottom
    flage = False

    # 视频帧率
    video_fps = 24
    time_delay = 2

    # 遍历获得框和标号

    for i, box in enumerate(bbox):
        # 获取框的2个坐标点
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        centerx = int((x1 + x2) / 2)
        centery = int((y1 + y2) / 2)

        # 当发生跟踪的情况下才保存中心点
        if detection_numbers > 0 and tracking_numbers > 0:
            point_of_line.append([centerx, centery])
            point_of_line_bottom.append([centerx, y2 + 1])
            # print(len(point_of_line))
            # lingerDetection.lingerdetection([centerx, y2 + 1],img)
            flage = linger.lingerdetection([centerx, y2 + 1])
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        color = compute_color_for_labels(id)
        label = '{}{:d}'.format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        # cv2.circle(img, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 5, color)

        # if len(point_of_line_bottom) > 4 and flage :
        #     for k in range(len(point_of_line_bottom) - 1):
        #         if  i % 3 == 0:
        #         # cv2.circle(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]), 2, color=(0,0,255))
        #             cv2.line(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]),
        #                  (point_of_line_bottom[k + 1][0], point_of_line_bottom[k + 1][1]), (0, 45, 150), 2)
        #
        #         # print("linger")
        #
        #         img1 = cv2.circle(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]), 2,
        #                           color=(0, 0, 255))
        #         path = "/home/xd/Desktop/pedestrainYolu3Okbak/output/img" + \
        #                str(k) + ".jpg"
        #         cv2.imwrite(path, img1)
        #         print("linger111111")
        cv2.rectangle(img, (x1, y1), (x1 + t_size[0] + 1, y1 + t_size[1] + 1), color, -1)
        cv2.putText(img, label, (x1, y1 + t_size[1] + 2), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)

    if len(point_of_line_bottom) > 4 and flage:
        for k in range(len(point_of_line_bottom) - 1):
            # cv2.circle(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]), 2, color=(0,0,255))
            cv2.line(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]),
                            (point_of_line_bottom[k + 1][0], point_of_line_bottom[k + 1][1]), (0, 100, 150), 2)
        # if imgIndex % (time_delay * video_fps) == 0 :
        #     # for k in range(len(point_of_line_bottom) - 1):
        #     #     # cv2.circle(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]), 2, color=(0,0,255))
        #     #     img1 = cv2.line(img, (point_of_line_bottom[k][0], point_of_line_bottom[k][1]),
        #     #                     (point_of_line_bottom[k + 1][0], point_of_line_bottom[k + 1][1]), (0, 45, 150), 1)
        #         path = "./output/img" + str(imgIndex) + ".jpg"
        #         cv2.imwrite(path, img1)

    if path:
        producer = KafkaProducer(bootstrap_servers=["192.168.6.153:9092"])
        msg = path.encode('utf-8')
        producer.send('test', msg)
        print(msg,"*******************************************************")
        producer.close()
    return img





if __name__ == '__main__':
    for i in range(82):
        print(compute_color_for_labels(i))

"""
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=["192.168.6.153:9092"])
msg = 'hello first1'.encode('utf-8')
producer.send('test', msg)
# producer.send("first",b"Hello world")
producer.close()
"""
