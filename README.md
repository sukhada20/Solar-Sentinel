# ☀️ Solar Sentinel – Real-Time UV Monitoring Dashboard

Solar Sentinel is a Flask-based web application that helps users monitor **real-time UV index data**, understand their **sun exposure risk**, and receive **skin-type-based sunscreen reminders**. Powered by the [OpenUV API](https://www.openuv.io/) and deployed on [Render](https://render.com/), this app combines data science, frontend interactivity, and public health awareness.

![ezgif-7fb2a1c47cf1a6](https://github.com/user-attachments/assets/1eed25ac-4331-4a55-b558-eba1638fde6b)

---

## 🌟 Features

- 📍 **Location-Based UV Index** for cities like New York, Nagpur, London and more
- 📊 **Interactive UV Forecast Chart** (Chart.js) for the last 12 hours
- 🌅 **Sunrise/Sunset Display** (partially implemented)
- 🧴 **Skin Type Quiz** using the Fitzpatrick scale
- 🔔 **Sunscreen Reminder Scheduler**
- ⚡ **Responsive UI** with TailwindCSS
- 🔐 Secure API key loading using Flask + Python dotenv

---

## 🚀 Live Demo

🌍 Hosted on [Render](https://render.com)

🔗 [View the Live App](https://solar-sentinel.onrender.com/)  

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, TailwindCSS, Chart.js, Vanilla JS
- **API:** [OpenUV.io](https://www.openuv.io/)
- **Deployment:** Render (free tier, no credit card)

---

## 📦 Project Structure
solar-sentinel/
│
├── app.py # Flask app entry point
├── requirements.txt # Dependencies
├── Procfile # Render deployment instruction
├── runtime.txt # Python version (3.12.9)
├── .env # Environment variables (not committed)
│
├── templates/
│ ├── index.html
│ └── partials/content.html
│
├── static/
│ ├── styles.css
│ └── script.js
│
└── README.md # You are here!

---

## 🧪 Local Development
### 1. Clone the repository
git clone https://github.com/your-username/solar-sentinel.git
cd solar-sentinel
### 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
### 3. Install dependencies
pip install -r requirements.txt
### 4. Set up .env
Create a .env file and add your OpenUV API Key
OPENUV_API_KEY=your_openuv_key_here
### 5. Run the app
python app.py
Then open your browser at http://localhost:5000

---

## ⚙️ Deployment (Render)
1) Create a free Render account
2) Connect your GitHub repo
3) Add build + start commands:
4) Build: pip install -r requirements.txt
5) Start: gunicorn app:app
6) Add environment variable:
   OPENUV_API_KEY=your_key
7) Hit Deploy

---

## 📌 Known Issues
🌅 Sunrise/sunset card is partially implemented :( 
🌎 Currently limited to a few predefined cities
🧴 No Predictions were added

--- 

## 🧠 Credits
OpenUV API — real-time UV index
Chart.js — charts
TailwindCSS — responsive styling

--- 

## 📜 License
This project is licensed under the MIT License — feel free to fork and adapt it.
