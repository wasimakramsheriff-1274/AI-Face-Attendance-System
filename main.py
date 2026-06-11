from deepface import DeepFace
import cv2
import os
import sqlite3
import threading
from datetime import datetime

# ==========================================
# 1. DATABASE SETUP
# ==========================================
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT
    )
''')
conn.commit()
conn.close() 

def mark_attendance_thread_safe(name):
    """Logs attendance with explicit terminal feedback for testing."""
    if name == "Unknown":
        return 

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    local_conn = sqlite3.connect('attendance.db')
    local_cursor = local_conn.cursor()

    # Check if a record already exists for today
    local_cursor.execute("SELECT * FROM logs WHERE name = ? AND date = ?", (name, current_date))
    record = local_cursor.fetchone()

    if record is None:
        # Fresh entry for the day
        local_cursor.execute("INSERT INTO logs (name, date, time) VALUES (?, ?, ?)", (name, current_date, current_time))
        local_conn.commit()
        print(f"✅ SUCCESS: Attendance marked for {name} on {current_date} at {current_time}")
    else:
        # NEW FEEDBACK LOG: Confirms the database check is actively running
        print(f"ℹ️ VERIFIED: {name} recognized! (Attendance already saved for today at {record[3]}). Skipping duplicate row.")
    
    local_conn.close()

# ==========================================
# 2. GLOBAL SYSTEM VARIABLES
# ==========================================
db_path = "dataset"
current_faces = []
ai_processing = False
status_text = "System Ready - Look into camera"

def run_ai_async(frame_copy):
    """Optimized backend using face-aligned SSD tracking."""
    global current_faces, ai_processing, status_text
    try:
        status_text = "AI: Scanning Face Details..."
        
        # 1. Analyze demographics using SSD (Very fast)
        demographics = DeepFace.analyze(
            img_path=frame_copy, 
            actions=['age', 'gender', 'emotion'], 
            detector_backend='ssd', 
            enforce_detection=True, 
            silent=True
        )
        
        if isinstance(demographics, dict):
            demographics = [demographics]
        
        if len(demographics) > 0:
            demo = demographics[0]
            region = demo.get('region', {})
            
            name = "Unknown"
            status_text = "AI: Checking Database ID..."
            
            # 2. Find Identity using SSD to retain proper face alignment matrix
            identities = DeepFace.find(
                img_path=frame_copy, 
                db_path=db_path, 
                detector_backend='ssd', 
                enforce_detection=False,
                silent=True
            )
            
            if len(identities) > 0 and len(identities[0]) > 0:
                matched_image_path = identities[0].iloc[0]['identity']
                name = os.path.basename(os.path.dirname(str(matched_image_path)))
                
                # Triggers the attendance check/log
                mark_attendance_thread_safe(name)

            # Update live view data frame variables safely
            current_faces = [{
                "name": name,
                "age": demo.get('age', 'N/A'),
                "gender": demo.get('dominant_gender', 'N/A'),
                "emotion": demo.get('dominant_emotion', 'N/A'),
                "box": (region.get('x', 0), region.get('y', 0), region.get('w', 0), region.get('h', 0))
            }]
            status_text = "AI: Scan Complete"
        else:
            current_faces = []
            status_text = "AI: Searching..."

    except Exception as e:
        current_faces = []
        status_text = "AI: Monitoring..."
    finally:
        ai_processing = False 

# ==========================================
# 3. MAIN VIDEO STREAM LOOP
# ==========================================
cam = cv2.VideoCapture(0)
frame_count = 0

print("Booting face application...")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame_count += 1

    # Check updates every 25 frames for snappy tracking
    if frame_count % 25 == 0 and not ai_processing:
        ai_processing = True
        threading.Thread(target=run_ai_async, args=(frame.copy(),), daemon=True).start()

    # Draw layout UI components continuous
    for person in current_faces:
        x, y, w, h = person["box"]
        color = (0, 255, 0) if person['name'] != "Unknown" else (0, 0, 255)
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        
        text_name = f"ID: {person['name']}"
        text_demo = f"{person['gender']} | {person['age']} | {person['emotion']}"
        
        cv2.putText(frame, text_name, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, text_demo, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    status_color = (0, 165, 255) if ai_processing else (0, 255, 0)
    cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    cv2.imshow("Ultimate AI Face Dashboard", frame)

    if cv2.waitKey(1) == 27: 
        break

cam.release()
cv2.destroyAllWindows()