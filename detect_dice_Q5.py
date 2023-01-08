import cv2
import random

src = cv2.imread("case5/img5_7.png", cv2.IMREAD_GRAYSCALE)

if src is None:
    print("File load failed!")
    exit()
# 이진화
_, dst = cv2.threshold(src, 200, 255, cv2.THRESH_BINARY)

dst = cv2.erode(dst, None, iterations = 2)

# 레이블링
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
# print(stats)

img, contours, hierarchy = cv2.findContours(dst, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# print(len(contours))
# print(contours)
dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
for i in range(len(contours)):
    c = (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
    cv2.drawContours(dst, contours, i, c, 2)

print(len(contours) - 1)

cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()