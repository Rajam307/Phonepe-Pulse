# 📱 PhonePe Pulse – Streamlit Data Visualization Dashboard

Welcome to the PhonePe Pulse Data Visualization Dashboard — a user-friendly and interactive web app built using **Streamlit** to explore and analyze PhonePe transaction and user data across India.

![GitHub stars](https://img.shields.io/github/stars/Rajam307/Phonepe-Pulse?style=social)
![GitHub forks](https://img.shields.io/github/forks/Rajam307/Phonepe-Pulse?style=social)
![GitHub issues](https://img.shields.io/github/issues/Rajam307/Phonepe-Pulse)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Rajam307/Phonepe-Pulse)

---

## 📑 Table of Contents
- [Overview](#overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)

---

## 🌟 Overview
This dashboard provides deep insights into PhonePe digital transactions across India.  
It helps analyze state-wise performance, transaction types, user growth, and real-world business scenarios.

---

## 🚀 Key Features

### 🏠 HOME
- Beautifully designed landing page
- India map view showing total **transaction count** and **amount** (choropleth)
- Highlight cards for **top 5 states**:
  - App opens
  - Registered users
  - Transaction amount

### 📊 DATA EXPLORATION
- Explore raw PhonePe data in table format
- Filter by **state**, **year**, **quarter**, and **transaction type**
- Dynamic summary of selected filters

### 📈 ANALYSIS REPORT
- 5 real-world business scenarios with visual insights
- Each scenario contains charts like:
  - Bar Charts
  - Pie Charts
  - Line Graphs
  - Map visualizations
- Uses Lottie animations for visual storytelling

### ❌ EXIT
- A closing tab with a thank you message and animated summary

---

## 🛠️ Tech Stack
- **Python**  
- **Streamlit**  
- **PostgreSQL**  
- **Plotly**  
- **Pandas, NumPy**  

---

## 📁 Project Structure
📦 Phonepe-Pulse  
├── phonepeproject.py # Main Streamlit dashboard  
├── phonepy.ipynb # Jupyter notebook (optional analysis)  
├── requirements.txt # All required Python libraries  
├── data/ # CSV or JSON data files  
├── assets/  
│ └── lottie/ # Lottie JSON animations  
└── README.md # Project documentation  

---

## ⚙️ Installation
```bash
git clone https://github.com/Rajam307/Phonepe-Pulse.git
cd Phonepe-Pulse
pip install -r requirements.txt
streamlit run phonepeproject.py



