from datetime import datetime
import http.server
import socketserver
import urllib.parse

PORT = 8000

def save_record(name, student_id):
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    with open("attendance.txt", "a") as f:
        f.write(f"[{now}] Name: {name} | ID: {student_id}\n")
        
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Attendance System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: #c0bad5;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }

        h1 {
            text-align: center;
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #667071;
            font-size: 0.85rem;
            margin-bottom: 25px;
        }

        .input-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #0e0455;
            font-size: 0.9rem;
        }

        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #0e0455;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 1rem;
        }

        input:focus {
            border-color: #27ae60;
            outline: none;
        }

        .btn {
            width: 100%;
            background-color: #0e0455;
            color: white;
            border: none;
            padding: 12px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }

        .btn:hover {
            background-color: #1a0b73;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Student Attendance System</h1>
        <p class="subtitle">SAD Midterm_Exam</p>

        <!-- Check-in Form -->
        <form action="/submit" method="POST" class="attendance-form">
            <div class="input-group">
                <label for="name">Full Name</label>
                <input type="text" id="name" name="name" placeholder="Enter full name" required>
            </div>
            
            <div class="input-group">
                <label for="student_id">Student ID</label>
                <input type="text" id="student_id" name="student_id" placeholder="Enter student ID" required>
            </div>
            
            <button type="submit" class="btn">Submit</button>
        </form>
    </div>
</body>
</html>
"""
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/submit':
            length = int(self.headers['Content-Length'])
            data = urllib.parse.parse_qs(self.rfile.read(length).decode())
           
            name = data.get('name', [''])[0]
            student_id = data.get('student_id', [''])[0]
           
            if name and student_id:
                save_record(name, student_id)
                print(f"Attendance recorded for: {name}")
           
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever() 
