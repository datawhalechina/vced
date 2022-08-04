import cv2

IN_DIR = './Demon Slayer/'
OUT_DIR = './Demon Slayer Re/'

for i in range(1, 114):
    # 也可以读取文件夹内所有图片
    IN_PATH = IN_DIR + str(i)+'.jpg'
    IN_IMG = cv2.imread(IN_PATH, 1)
    # 定义输入路径
    if IN_IMG is None:
        print(IN_PATH +'is not exist!')

    OUT_IMG = cv2.resize(IN_IMG, (160, 90))
    OUT_PATH = OUT_DIR + str(i) + '.jpg'
    cv2.imwrite(OUT_PATH, OUT_IMG)
    # 定义输出路径，生成图片