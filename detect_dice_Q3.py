import cv2
import random

def on_trackbar(pos):
    bsize = pos
    if bsize % 2 == 0:
        bsize = bsize - 1
    if bsize < 3:
        bsize = 3

    dst = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, bsize, 5)

    cv2.imshow('dst', dst)


src = cv2.imread("case3/img3_2.png", cv2.IMREAD_GRAYSCALE)

if src is None:
    print("File load failed!")
    exit()

# cv2.namedWindow('dst')
# cv2.createTrackbar('Block Size', 'dst', 0, 200, on_trackbar)
# cv2.setTrackbarPos('Block Size', 'dst', 11)

# 적응형 이진화 81
dst = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 65, 5) #63~199
# 모폴로지 열기 연산, 4번 진행해서 배경 없앰
dst2 = cv2.morphologyEx(dst, cv2.MORPH_OPEN, None, iterations= 5)
dst2 = cv2.dilate(dst2, None)
dst2 = cv2.morphologyEx(dst2, cv2.MORPH_CLOSE, None, iterations= 4)

# 레이블링
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(dst2)
# print(cnt)
# print(stats)

for i in range(1, cnt):
    (x, y, w, h, area) = stats[i]

cv2.imshow('dst', dst)
cv2.imshow('dst2', dst2)

# 외곽선 검출 RETR_CCOMP로 해서 2단계 계층정보 알 수 있도록 했음.
img, contours, hierarchy = cv2.findContours(dst2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

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
cv2.waitKey()
cv2.destroyAllWindows()