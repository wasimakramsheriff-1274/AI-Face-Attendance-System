<h1 align="center">🤖 AI Face Recognition Attendance & Monitoring System</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/AI_Powered-Deep_Learning-8A2BE2?style=for-the-badge" alt="AI Powered" />
</p>

> A high-performance, full-stack, multi-threaded computer vision pipeline that automates attendance tracking using facial recognition. The system leverages deep learning to identify verified individuals while concurrently tracking real-time demographics (Age, Gender, Emotion). It logs safe, non-duplicate entries into an SQLite database and serves them on a responsive, custom dark-themed web control panel.

---

## 💻 Core Tech Stack
<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
</p>

---

## 🚀 Core Features

* **Buttery Smooth Live Tracking:** Multi-threaded architecture isolates the heavy AI deep learning models onto background threads, maintaining a lag-free 30 FPS webcam stream.
* **Lightweight & High-Speed Inference:** Implements the Single Shot MultiBox Detector (SSD) backend via DeepFace for quick, accurate facial tracking under tricky indoor lighting.
* **Dual-Inference Pipeline:** Simultaneously computes facial identity matching against a local image dataset while tracking dynamic demographics (Age, Gender, and dominant Emotions).
* **Smart Database Logging:** Powered by SQLite3 with a thread-safe connection framework. Includes automated daily cooldown checks to block duplicate logs for the same user on the same day.
* **Intruder/Visitor Protection:** Automatically categorizes unindexed faces as `Unknown`, displays a visual warning box on-screen, and filters them out from polluting the attendance database.
* **Premium Web Dashboard:** A web control panel built with Flask, HTML5, and CSS3 displaying real-time analytics cards (Total Scans, Verified Attendees Present) and a descending historical log stream.

---

## 📦 Installation & Setup

**1. Clone the Repository:**
**```bash**
git clone [https://github.com/wasimakramsheriff-1274/AI-Face-Attendance-System.git](https://github.com/wasimakramsheriff-1274/AI-Face-Attendance-System.git)
cd AI-Face-Attendance-System

**2. Set up Virtual Environment:**

**Bash**
python -m venv face_env
face_env\Scripts\activate

**3. Install Dependencies:**

**Bash**
pip install -r requirements.txt

**4. Prepare the Dataset:**
Create a folder named dataset/ in the root directory. Inside it, create subfolders named after the individuals you wish to recognize and drop a clear headshot inside:

**Plaintext**
dataset/
└── Wasim/
    └── photo.jpg
    
**🖥️ Running the Application**
To run the full-stack system, execute both modules concurrently using two active terminal windows:

**Terminal 1 (AI Face Tracker Engine):**

**Bash**
python main.py

**Terminal 2 (Flask Web Server):**

**Bash**
python app.py

Once running, open your preferred web browser and navigate to http://127.0.0.1:5000 to view the live monitoring control panel.
