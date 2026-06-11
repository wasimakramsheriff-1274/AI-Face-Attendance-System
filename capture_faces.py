import cv2
import os

person_name = "Wasim"
folder = f"dataset/{person_name}"

os.makedirs(folder, exist_ok=True)

cam = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cam.read()

    if not ret:
        break

    cv2.putText(
        frame,
        f"Photos: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Capture Faces", frame)

    key = cv2.waitKey(1)

    # SPACE = save image
    if key == 32:
        count += 1

        filename = os.path.join(folder, f"{count}.jpg")

        cv2.imwrite(filename, frame)

        print("Saved:", filename)

    # ESC = exit
    elif key == 27:
        break

cam.release()
cv2.destroyAllWindows()