import cv2
import time
import datetime
import requests

# Load Haar cascades
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# ESP8266 URLs
ESP_LIGHT_ON = "http://192.168.43.177/light/on"
ESP_LIGHT_OFF = "http://192.168.43.177/light/off"
ESP_MOTOR_ON = "http://192.168.43.177/motor/on"
ESP_MOTOR_OFF = "http://192.168.43.177/motor/off"
ESP_BUZZER_ON = "http://192.168.43.177/buzzer/on"
ESP_BUZZER_OFF = "http://192.168.43.177/buzzer/off"

# Alarm Time (24-hour format)
ALARM_HOUR = 11
ALARM_MINUTE = 32


# Track states
alarm_triggered = False
buzzer_off = False
last_action = None

def send_to_esp(url):
    try:
        requests.get(url)
        print(f"✅ Triggered: {url}")
    except:
        print(f"❌ Failed to connect to: {url}")

# Before alarm: DC Motor ON, Light OFF, Buzzer OFF
send_to_esp(ESP_LIGHT_OFF)
send_to_esp(ESP_MOTOR_ON)
send_to_esp(ESP_BUZZER_OFF)

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    # Check current time
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    # Trigger alarm actions
    if not alarm_triggered and current_hour == ALARM_HOUR and current_minute == ALARM_MINUTE:
        alarm_triggered = True
        print("⏰ Alarm Time Reached!")

        send_to_esp(ESP_LIGHT_ON)
        send_to_esp(ESP_MOTOR_OFF)
        send_to_esp(ESP_BUZZER_ON)

    # After alarm: start eye detection
    if alarm_triggered and not buzzer_off:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        eyes_detected = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)

            if len(eyes) >= 1:
                eyes_detected = True
                break

        # If eyes are open, turn off buzzer
        if eyes_detected:
            print("👁️ Eyes Detected - Stopping Buzzer")
            send_to_esp(ESP_BUZZER_OFF)
            buzzer_off = True

        cv2.imshow("Wakeup Eye Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if not alarm_triggered:
        print(f"Waiting... Current Time: {now.strftime('%H:%M:%S')}", end='\r')
        time.sleep(1)

cap.release()
cv2.destroyAllWindows() 
