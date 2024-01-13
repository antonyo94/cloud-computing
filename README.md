# Cloud Computing

## 🛠 Skills
IoT, Raspberry PI Model 3, Python, Flask, AWS, Amazon EC2, Amazon Dynamo DB, NoSQL

## 📝 Requirements
*Implement an IoT system that uses a sensor system for remote sensing of the water level.*

## 📖 Lessons Learned
The **Cloud Computing** project allowed me to approach the **IoT** world for the first time through the configuration and use of a **Raspberry PI** Model 3. The project in fact involves the resolution of a real problem through the use of this type of device, to which, as is well known, it is possible to connect external sensors. Similarly, since the computing and storage resources for these devices are very limited, it was necessary to configure and use cloud services for storing, processing and accessing data. In this regard, the cloud provider chosen to carry out the project is **Amazon AWS**, which, through the issuing of university credits, allows students to carry out small projects independently. Once the key aspects of the project were defined, i.e. the hardware tools and cloud services, I had the opportunity to delve into the implementation details for its creation.
In this regard, during development, I was able to create the component in **Python** for reading data from the external sensor connected to the Raspberry and, subsequently, send this information to a **NOSql** cloud database, namely **Amazon Dynamo DB**. Once the data has been stored, it is made accessible to the public through the implementation of a web app, created using the **Flask** framework, which in turn is run on an **Amazon EC2** server instance. The application, accessible via a URL, allows you to monitor in real time the progress of the data obtained through sensors.
A further key aspect of the project is the possibility of receiving emails, as an alert signal when the data obtained reaches too high levels, in addition to the use of the Blynk IoT platform which allows, through the cloud, to monitor the telemetry data directly on your device mobile.