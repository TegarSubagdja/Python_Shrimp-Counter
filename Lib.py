import cv2
import numpy as np

def detect_black_dots_in_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Optional: tambahkan blur untuk mengurangi noise jika perlu
    # thresh = cv2.GaussianBlur(thresh, (3, 3), 0)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    valid_contours = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))
            valid_contours.append(cnt)
    return centers, valid_contours

def draw_detected_dots(frame, centers, contours):
    for idx, (center, cnt) in enumerate(zip(centers, contours)):
        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 1)
        cv2.circle(frame, center, 3, (0, 0, 255), -1)
        cv2.putText(frame, f"ID {idx}", (center[0] + 5, center[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
    cv2.putText(frame, f"Total Detected: {len(centers)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    return frame

def detect_black_dots(source, source_type="image"):
    if source_type == "image":
        frame = cv2.imread(source)
        if frame is None:
            raise ValueError("Gambar tidak ditemukan atau tidak bisa dibaca.")
        centers, contours = detect_black_dots_in_frame(frame)
        print(f"Total titik hitam terdeteksi: {len(centers)}")
        result = draw_detected_dots(frame, centers, contours)

        cv2.namedWindow("Detected Black Dots", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Detected Black Dots", 1920-100, 1080-100)
        cv2.imshow("Detected Black Dots", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif source_type in ["video", "realtime"]:
        cap = cv2.VideoCapture(0 if source_type == "realtime" else source)
        if not cap.isOpened():
            raise ValueError("Video/Webcam tidak bisa dibuka.")

        cv2.namedWindow("Detected Black Dots", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Detected Black Dots", 1920, 1080)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            centers, contours = detect_black_dots_in_frame(frame)
            print(f"Total titik hitam terdeteksi: {len(centers)}")
            result = draw_detected_dots(frame, centers, contours)
            cv2.imshow("Detected Black Dots", result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

