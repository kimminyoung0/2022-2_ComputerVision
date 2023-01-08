import cv2

def question1():
    src = cv2.imread("case1/dice_5.png", cv2.IMREAD_GRAYSCALE)

    if src is None:
        print("File load failed!")
        exit()

    # 이진화
    _, dst = cv2.threshold(src, 128, 255, cv2.THRESH_BINARY)

    # 외곽선 검출
    img, contours, hierarchy = cv2.findContours(dst, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    dice_cnt = 0
    for i in range(len(contours)):
        if hierarchy[0][i][3] == 0:
            dice_cnt += 1

    print(dice_cnt)
    cv2.imshow('src', src)
    cv2.imshow('dst', dst)
    cv2.waitKey()
    cv2.destroyAllWindows()


def question2():
    src = cv2.imread("case2/dice_ques2.png", cv2.IMREAD_GRAYSCALE)

    if src is None:
        print("File load failed!")
        exit()

    # 이진화
    _, dst = cv2.threshold(src, 128, 255, cv2.THRESH_BINARY)

    # 외곽선 검출
    img, contours, hierarchy = cv2.findContours(dst, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    dice_lst = []
    dice_cnt = 0
    for i in range(1, len(contours)):
        if hierarchy[0][i][3] != -1:
            dice_cnt += 1
            if i == len(contours) - 1:
                dice_lst.append(dice_cnt)
        elif hierarchy[0][i][3] == -1:
            dice_lst.append(dice_cnt)
            dice_cnt = 0

    print(sorted(dice_lst))

    cv2.imshow('dst', dst)
    cv2.waitKey()
    cv2.destroyAllWindows()



#question1()
question2()





