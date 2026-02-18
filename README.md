# 🛡️ Smart Intrusion Detection System using Raspberry Pi 4

A simple, low-cost **security and surveillance system** built using Raspberry Pi, Ultrasonic Sensor, and PIR Motion Sensor.
This project detects unauthorized movement or proximity and triggers an alert.

---

## 📖 Project Description

This system continuously monitors an area for intrusions using two sensors:

* **PIR Motion Sensor** → Detects human movement based on infrared radiation.
* **Ultrasonic Sensor (HC-SR04)** → Measures distance to detect nearby objects.
* **Raspberry Pi 4** → Processes data and activates an alarm.

When motion is detected or distance crosses a defined threshold, the system triggers a buzzer and logs the event.

---

## ✨ Features

* Real-time motion detection
* Distance-based intrusion detection
* Instant buzzer alert
* Continuous monitoring loop
* Low-cost and easy to build
* Ideal for home, lab, and office security

---

## 🧰 Hardware Requirements

| Component                   | Quantity    |
| --------------------------- | ----------- |
| Raspberry Pi 4              | 1           |
| PIR Motion Sensor           | 1           |
| Ultrasonic Sensor (HC-SR04) | 1           |
| Buzzer                      | 1           |
| Breadboard                  | 1           |
| Jumper Wires                | As required |
| Power Supply                | 1           |

---

## 💻 Software Requirements

* Raspberry Pi OS
* Python 3
* RPi.GPIO Library

Install required library:

```bash
pip3 install RPi.GPIO
```

---

## 🔌 Circuit Connections

### PIR Sensor → Raspberry Pi

| PIR Pin | Raspberry Pi Pin |
| ------- | ---------------- |
| VCC     | 5V               |
| GND     | GND              |
| OUT     | GPIO 17          |

### Ultrasonic Sensor (HC-SR04)

| Sensor Pin | Raspberry Pi Pin |
| ---------- | ---------------- |
| VCC        | 5V               |
| GND        | GND              |
| TRIG       | GPIO 23          |
| ECHO       | GPIO 24          |

### Buzzer

| Buzzer Pin | Raspberry Pi Pin |
| ---------- | ---------------- |
| Positive   | GPIO 18          |
| Negative   | GND              |

---

## ⚙️ Working Principle

1. System continuously reads PIR sensor for motion.
2. Ultrasonic sensor measures distance from nearby objects.
3. If motion is detected OR distance is below threshold:

   * Buzzer turns ON
   * Alert message is printed in terminal.
4. System returns to monitoring mode after alert.

---

## 🚀 How to Run the Project

Clone this repository:

```bash
git clone https://github.com/your-username/intrusion-detection-pi.git
cd intrusion-detection-pi
```

Run the program:

```bash
python3 intrusion.py
```

---

## 📈 Future Improvements

* Send Email/SMS alerts
* Add camera for photo capture
* Mobile app notifications
* Cloud data logging

---

## 👨‍💻 Authors

* Your Name
* Team Members

---

## 📜 License

This project is licensed under the **MIT License**.
