import cv2
# 导入OpenCV库

def get_each_frame(video_path):
    # 定义抽帧函数
    videoCapture = cv2.VideoCapture(video_path)
    success, frame = videoCapture.read()
    i = 0
    timeF = 300
    # 设定抽帧间隔
    j = 0
    while success:
        i += 1
        if (i % timeF == 0):
            j += 1
            address = str(j) + '.jpg'
            # 设置路径
            cv2.imwrite(address, frame)
            # 保存图片
            print('save images:', i)
        success, frame = videoCapture.read()

get_each_frame(r"F:\FFOutput\第26話 新たなる任務.mp4")