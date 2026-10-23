from datetime import datetime
import http.server
import socketserver
import urllib.parse

PORT = 8000

def save_record(name, student_id):
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    with open("attendance.txt", "a") as f:
        f.write(f"[{now}] Name: {name} | ID: {student_id}\n")