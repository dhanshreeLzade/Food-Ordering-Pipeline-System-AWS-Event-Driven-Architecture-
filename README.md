📌 Overview

A fully end-to-end event-driven food ordering system simulating a real-world distributed cloud architecture using AWS services.

The system is built using loosely coupled services communicating via events, making it scalable, modular, and cloud-native instead of a monolithic backend.

🧩 Architecture Style
Event-Driven Architecture (EDA)
Publisher–Subscriber Model
Serverless service communication
🛠️ Tech Stack
Frontend: Flask + Streamlit
Messaging: AWS SNS (Simple Notification Service)
Database: AWS DynamoDB
SDK: boto3 (AWS SDK for Python)

⚙️ Workflow

Customer places order → SNS event published → Restaurant service updates status → Delivery service completes order →
ORDERED → READY → DELIVERED → Data stored in DynamoDB → UI shows real-time updates

💡 Key Features
Real-time order tracking
Decoupled service architecture
AWS SNS-based event communication
DynamoDB for scalable storage
Cloud-like production workflow simulation

📚 Key Learnings
Event-driven system design
Pub-Sub architecture using AWS SNS
Service decoupling for scalability
NoSQL data handling with DynamoDB
Moving from monolithic to distributed thinking
