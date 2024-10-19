
---

# Safety Requirement Detection Project

This project involves the detection of Personal Protective Equipment (PPE), such as hardhats, masks, and safety vests, using a YOLO model. It is integrated with an ESP32 microcontroller that receives commands based on the detected safety equipment. The project can process both webcam feeds and videos, providing real-time feedback on safety compliance.

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [How It Works](#how-it-works)
5. [Libraries Used](#libraries-used)
6. [Connecting to the ESP32](#connecting-to-the-esp32)
7. [Usage](#usage)
8. [Contributing](#contributing)
9. [License](#license)

## Overview
This project uses the YOLO object detection model to identify if a person is wearing the required safety gear such as:
- Hardhat
- Mask
- Safety Vest

When the required equipment is detected, the system sends a command to an ESP32 microcontroller over a network to trigger actions like opening a door or turning on an indicator light.

## Requirements
- Python 3.x
- OpenCV
- cvzone
- YOLOv8 (Ultralytics)
- A trained YOLO model (`ppe.pt`)
- ESP32 microcontroller
- Webcam or video input

## Installation
### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/safety-requirement-detection.git
cd safety-requirement-detection
```

### 2. Install required libraries:
```bash
pip install -r requirements.txt
```

### 3. Set up the YOLO model:
- Download or train a custom YOLO model (`ppe.pt`) trained on images of people with and without safety equipment.
- Place the `ppe.pt` file in the root of the project directory.

### 4. Configure the ESP32 IP address:
- Replace the `ESP32_IP` variable in the code with the actual IP address of your ESP32 device.

### 5. Run the detection code:
```bash
python detection_model.py
```

## How It Works
1. The YOLO model detects safety equipment (hardhat, mask, safety vest) and non-compliance cases (no hardhat, no mask, etc.) from video or webcam input.
2. The system classifies detected objects and their confidence levels.
3. If the required PPE is detected, it sends commands to the ESP32 via sockets to trigger actions.

## Libraries Used
### 1. [Ultralytics YOLO](https://docs.ultralytics.com/)
- This library provides an easy-to-use interface for running YOLO models for object detection.
- Used for loading the pre-trained `ppe.pt` model and performing object detection.

### 2. [OpenCV](https://opencv.org/)
- OpenCV is used for capturing video input, resizing frames, and drawing bounding boxes.
- It processes frames from both webcam feeds and video files and displays the output.

### 3. [cvzone](https://pypi.org/project/cvzone/)
- cvzone simplifies the process of drawing rectangles, adding text, and other visual elements in the OpenCV interface.
- Used to display bounding boxes, class names, and confidence scores on detected objects.

### 4. [socket](https://docs.python.org/3/library/socket.html)
- A Python library that provides access to low-level networking interfaces.
- Used for sending commands to the ESP32 via the network.

### 5. [math](https://docs.python.org/3/library/math.html)
- The math module is used for rounding off confidence values for the detected objects.

## Connecting to the ESP32
This project sends commands to an ESP32 microcontroller over a WiFi network. The ESP32 acts as a server, and the Python script sends specific commands depending on the detection results.

- **Yes**: Sent when the person is detected with all required safety equipment.
- **No**: Sent if any piece of required equipment is missing.

To establish communication:
1. Ensure the ESP32 is connected to the same WiFi network as your computer.
2. Update the `ESP32_IP` and `ESP32_PORT` values in the script to match your ESP32 configuration.

## Usage
### Running the Detection Model
To start detecting safety requirements from a video or webcam, simply run:
```bash
python detection_model.py
```
By default, the script uses a video feed. To switch to a webcam, modify the `cap` variable to `cv2.VideoCapture(0)` in the code.

### Running the ESP32 Connection
To run the system that sends commands to the ESP32, run:
```bash
python esp32_connection.py
```

This script will continuously monitor the video feed and send commands to the ESP32 when conditions are met.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request to enhance the project or add features.

## License
This project is licensed under the MIT License