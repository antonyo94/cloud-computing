# Cloud Computing

## 🛠 Skills
- IoT
- Raspberry PI Model 3
- Python
- Flask
- AWS
- Amazon EC2
- Amazon Dynamo DB
- NoSQL

## 📝 Requirements
*Implement an IoT system that uses a sensor system for remote sensing of the water level.*

## 📖 Lessons Learned
- The **Cloud Computing** project allowed me to approach the **IoT** world for the first time through the configuration and use of a **Raspberry PI** Model 3.

- The project involved solving a real problem using the Raspberry Pi, which can connect to external sensors. Given the limited computing and storage resources of the device, I configured and used **cloud services** for storing, processing, and accessing data.

- The cloud provider chosen for the project was **Amazon AWS**, which provides university credits for students to work on small projects independently.

- Once the hardware tools and cloud services were defined, I:
  - Created a **Python** component for reading data from an external sensor connected to the Raspberry Pi.
  - Sent this data to a **NoSQL** cloud database, **Amazon DynamoDB**.

- After storing the data, I made it accessible through the implementation of a web app using the **Flask** framework, which runs on an **Amazon EC2** server instance:

- The application is accessible via a URL and allows real-time monitoring of sensor data.

- Key aspects of the project include:
  - Receiving **email alerts** when data levels exceed a set threshold.
  - Using the **Blynk IoT platform** to monitor telemetry data directly on mobile devices via the cloud.
