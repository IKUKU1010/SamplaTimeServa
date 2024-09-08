from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import pytz  # Import pytz for timezone handling

app = FastAPI()

# Mount the static files directory to serve favicon.ico
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Welcome to the Timeserver API</h1><p>Use <a href='/time'>/time</a> to view the current time in West Africa Time (WAT).</p>"

@app.get("/time", response_class=HTMLResponse)
async def get_current_time():
    # Get current time in West Africa Time (WAT)
    tz = pytz.timezone('Africa/Lagos')  # 'Africa/Lagos' corresponds to WAT (UTC+1)
    current_time = datetime.now(tz)
    
    # Format the date, time, and day
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    day_of_week = current_time.strftime("%A")  # Get the day of the week

    # HTML content with bold stylized font, live clock, and links to notable events search
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Current Time</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                text-align: center;
                background-color: #f0f0f0;
                padding: 50px;
            }}
            .time-display {{
                font-size: 48px;
                font-weight: bold;
                color: #333;
                margin-top: 20px;
            }}
            .clock {{
                font-size: 36px;
                font-weight: bold;
                color: #007BFF;
                margin-top: 20px;
            }}
            .events {{
                margin-top: 40px;
                font-size: 20px;
            }}
            a {{
                color: #007BFF;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>Current Date and Time</h1>
        <div class="time-display">Day: {day_of_week}, Date: {formatted_time}</div>

        <h2>Live Clock</h2>
        <div class="clock" id="clock"></div>

        <h2>Notable Events on This Day in History</h2>
        <div class="events">
            <p>Check out what happened today in history:</p>
            <ul>
                <li><a href="https://www.google.com/search?q=notable+events+on+{current_time.strftime('%B+%d')}" target="_blank">Google</a></li>
                <li><a href="https://en.wikipedia.org/wiki/{current_time.strftime('%B_%d')}" target="_blank">Wikipedia</a></li>
                <li><a href="https://www.onthisday.com/date/{current_time.strftime('%Y/%B/%d')}" target="_blank">OnThisDay</a></li>
            </ul>
        </div>

        <script>
            function updateClock() {{
                const now = new Date();
                const hours = String(now.getUTCHours() + 1).padStart(2, '0'); // Adjust for UTC+1
                const minutes = String(now.getUTCMinutes()).padStart(2, '0');
                const seconds = String(now.getUTCSeconds()).padStart(2, '0');
                const timeString = hours + ':' + minutes + ':' + seconds + ' WAT';
                document.getElementById('clock').textContent = timeString;
            }}
            setInterval(updateClock, 1000);
            updateClock();  // Initial call to display clock immediately
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
