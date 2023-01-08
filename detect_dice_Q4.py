import cv2
import random
from math import sqrt

# 유클리디안 거리 구하기
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)


src = cv2.imread("case4/img4_5.png", cv2.IMREAD_GRAYSCALE)

if src is None:
    print("File load failed!")
    exit()

# 적응형 이진화 81
dst = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 5) #63~199

# 모폴로지 열기 연산, 4번 진행해서 배경 없앰
dst2 = cv2.erode(dst, None, iterations= 1)
dst2 = cv2.morphologyEx(dst2, cv2.MORPH_CLOSE, None, iterations= 1)
dst2 = cv2.erode(dst2, None, iterations= 1)
dst2 = cv2.morphologyEx(dst2, cv2.MORPH_OPEN, None, iterations= 1)
dst2 = cv2.dilate(dst2, None, iterations= 2)
dst2 = cv2.erode(dst2, None, iterations= 1)

# 레이블링
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(dst2)
centroids = centroids.astype(int)
dnum = 0
dice_cnt = 0
dice_lst = []
dnum_lst = []
dst2 = cv2.cvtColor(dst2, cv2.COLOR_GRAY2BGR)
for i in range(1, cnt):
    (x, y, w, h, area) = stats[i]
    if area < 500: #작은 원들만 dice_lst에 넣기
        dice_lst.append(stats[i])

for i in range(1, cnt):
    (x, y, w, h, area) = stats[i]
    pt1 = (x,y)
    pt2 = (x+w, y+h)
    # cv2.drawMarker(dst2, pt1, (255, 0, 0), cv2.MARKER_STAR) #BLUE
    # if area > 7000: # 주사위 하나
    #     cv2.rectangle(dst2, pt1, pt2, (0,255,255)) #YELLOW
    # elif area < 7000: #주사위 안 동그라미
    #     cv2.rectangle(dst2, pt1, pt2, (0,0,255))  #RED
    if area > 7000:
        # print(stats[i], "일 때")
        for j in range(len(dice_lst)):
            if euclidean_distance([x,y], [dice_lst[j][0], dice_lst[j][1]]) < 133:
                # print(dice_lst[j][0], dice_lst[j][1])
                dnum += 1
                dice_lst[j] = [0,0,0,0,0]
        dnum_lst.append(dnum)
        dnum = 0


print(dnum_lst)
print(sorted(dnum_lst))



# #1 = 6인 주사위
# cv2.rectangle(dst2, (350, 150), (502, 310), (255, 0, 0))
#
# #2 = 2인 오른쪽 주사위 492, 323, 150, 145, 10237
# cv2.rectangle(dst2, (492, 323), (642, 468), (255, 100, 0))
#
# #3 = 2인 왼쪽 주사위 164, 334, 143, 142, 8662
# cv2.rectangle(dst2, (165, 335), (310, 480), (255, 0, 90))
#
# cv2.rectangle(dst2, (242, 357), (265, 381), (200, 200, 100))
# cv2.rectangle(dst2, (206, 431), (230, 454), (200, 200, 100))
# #cv2.rectangle(dst2, (), (), (200, 200, 100))
#
# #4 = 3인 주사위 340, 425, 149, 141, 9385
# cv2.rectangle(dst2, (350, 430), (490, 570), (255, 255, 20))
# print(dice_lst)


# # 외곽선 검출 RETR_CCOMP로 해서 2단계 계층정보 알 수 있도록 했음.
# img, contours, hierarchy = cv2.findContours(dst2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# print(len(contours))
# print(hierarchy)
# dst2 = cv2.cvtColor(dst2, cv2.COLOR_GRAY2BGR)
# for i in range(len(contours)):
#     c = (random.randint(0,255), random.randint(0, 255), random.randint(0, 255))
#     cv2.drawContours(dst2, contours, i, c, 2)
# dice_lst = []
# dice_cnt = 0
# for i in range( 1, len(contours)):
#
#     if hierarchy[0][i][3] != -1:
#         dice_cnt += 1
#         if i == len(contours) - 1:
#             dice_lst.append(dice_cnt)
#
#     elif hierarchy[0][i][3] == -1:
#         dice_lst.append(dice_cnt)
#         dice_cnt = 0
#
# print(sorted(dice_lst))
cv2.imshow('dst', dst)
cv2.imshow('dst2', dst2)
cv2.waitKey()
cv2.destroyAllWindows()