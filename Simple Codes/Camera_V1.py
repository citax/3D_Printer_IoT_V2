import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

print("ret =",ret)
print(frame)
cv2.imwrite('photo.jpg',frame)

cap.release()

