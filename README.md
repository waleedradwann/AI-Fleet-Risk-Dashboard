AI Fleet Risk Dashboard

Overview

AI Fleet Risk Dashboard is a real time fleet monitoring and driver analytics platform developed using Python, Streamlit, Machine Learning, ROS2, and ESP32.

The system collects vehicle telemetry data, analyzes driver behavior, and generates risk insights through an interactive dashboard. The project demonstrates how modern IoT devices and machine learning techniques can be combined to improve fleet safety, operational awareness, and driver performance monitoring.

Key Features

* Real time vehicle telemetry monitoring
* Driver safety score calculation
* Driver risk classification
* Machine learning based risk prediction
* Interactive fleet analytics dashboard
* ESP32 integration for edge data collection
* ROS2 communication architecture
* Data visualization and reporting

Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-Learn
* Plotly
* ROS2
* ESP32
* SQLite

System Architecture

ESP32 Vehicle Sensor Node

↓

ROS2 Communication Layer

↓

Python Data Processing Engine

↓

Machine Learning Risk Analysis

↓

Streamlit Dashboard Interface

Project Objectives

The project aims to:

* Monitor vehicle health and driver performance
* Detect risky driving behavior
* Generate actionable fleet insights
* Demonstrate Industry 4.0 and IoT concepts
* Build a scalable connected fleet monitoring platform

Future Enhancements

* GPS based vehicle tracking
* Live route visualization
* Driver behavior analysis using accelerometer data
* Geofencing capabilities
* Predictive maintenance analytics
* Cloud deployment
* Multi vehicle fleet management
* Advanced AI safety scoring

Repository Structure
AI-Fleet-Risk-Dashboard/
├── app.py
├── dashboard.py
├── database.py
├── telemetry.py
├── predict.py
├── train.py
├── train_model.py
├── requirements.txt
├── driver_monitoring.db
└── data.csv

Installation
pip install -r requirements.txt

Run Dashboard
streamlit run dashboard.py

Author

Waleed Radwan

Electrical Engineer focused on Industrial Automation, Embedded Systems, IoT, ROS2, and Machine Learning.
