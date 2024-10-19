import socket
from ultralytics import YOLO
import cv2
import cvzone
import math

# ESP32 server details
ESP32_IP = "192.168.146.94"  # Replace with your ESP32 IP address
ESP32_PORT = 80

# Initialize YOLO model
model = YOLO("ppe.pt")
classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

# Function to send command to ESP32
def send_command_to_esp32(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ESP32_IP, ESP32_PORT))
        s.sendall(f"{command}\n".encode())

# Video input
#cap = cv2.VideoCapture(r"C:\Users\danie\PycharmProjects\Object detection project\Safety_requirement\videos\ppe2.mp4")  # For Video
cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 640)
cap.set(4, 640)

while True:
    success, img = cap.read()
    img_resized = cv2.resize(img, (640, 640))
    results = model(img_resized, stream=True)

    # Initialize flags for detection
    person_detected = False
    hardhat_detected = False
    mask_detected = False
    vest_detected = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            # Confidence and Class Name
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if conf > 0.5:
                if currentClass == 'Person':
                    person_detected = True
                elif currentClass == 'Hardhat':
                    hardhat_detected = True
                elif currentClass == 'Mask':
                    mask_detected = True
                elif currentClass == 'Safety Vest':
                    vest_detected = True

            cvzone.putTextRect(img_resized, f'{classNames[cls]} {conf}',
                               (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=(0, 255, 0),
                               colorT=(255, 255, 255), offset=5)
            cv2.rectangle(img_resized, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # Check if all required safety equipment is detected
    if person_detected:
        send_command_to_esp32("yes1")  # Send "yes" to ESP32 if all conditions are met
    if hardhat_detected:
        send_command_to_esp32("yes2")
    if mask_detected:
        send_command_to_esp32("yes3")
    if vest_detected:
        send_command_to_esp32("yes4")
    else:
        send_command_to_esp32("no")  # Send "no" if any condition is missing

    cv2.imshow("Image", img_resized)
    cv2.waitKey(1)
