import cv2
import numpy as np
import time
import requests  # Required to control ESP8266

face_cascade = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml")

# ESP8266 URLs
ESP_ON_URL = "http://192.168.43.177/start"   # Replace with your ESP IP
ESP_OFF_URL = "http://192.168.43.177/stop"

cap = cv2.VideoCapture(0)

prev_x = prev_y = None
gesture_cooldown = 2  # seconds
last_trigger_time = time.time()

def send_to_esp(action):
    try:
        if action == "on":
            requests.get(ESP_ON_URL)
            print("🔆 Light ON")
        elif action == "off":
            requests.get(ESP_OFF_URL)
            print("🔅 Light OFF")
    except:
        print("❌ ESP not reachable")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_flipped = cv2.flip(frame, 1)  # mirror effect
    gray = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        center_x = x + w // 2
        center_y = y + h // 2

        cv2.rectangle(frame_flipped, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.circle(frame_flipped, (center_x, center_y), 5, (0, 255, 255), -1)

        if prev_x is not None and prev_y is not None:
            dx = center_x - prev_x
            dy = center_y - prev_y

            # Threshold to detect movement
            if abs(dx) > 25 and abs(dx) > abs(dy):  # Horizontal Shake
                if time.time() - last_trigger_time > gesture_cooldown:
                    send_to_esp("on")
                    last_trigger_time = time.time()

            elif abs(dy) > 25 and abs(dy) > abs(dx):  # Vertical Shake
                if time.time() - last_trigger_time > gesture_cooldown:
                    send_to_esp("off")
                    last_trigger_time = time.time()

        prev_x, prev_y = center_x, center_y

    cv2.imshow("Head Gesture Light Control", frame_flipped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
