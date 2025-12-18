from flask import Flask, request
import requests

app = Flask(__name__)

# Tumhara original AI endpoint
EXTERNAL_API_URL = "https://apis.prexzyvilla.site/ai/gpt-5"

@app.route('/')
def home():
    return "<h1>Flip AI Proxy is LIVE! 🚀</h1><p>Use: /ai?text=Your message in English</p><p>Example: /ai?text=Tell me a funny joke</p>"

@app.route('/ai', methods=['GET'])
def proxy_ai():
    text = request.args.get('text')
    
    if not text:
        return "Error: Missing 'text' parameter. Example: /ai?text=Hello", 400
    
    try:
        # External AI ko call karo
        response = requests.get(EXTERNAL_API_URL, params={'text': text}, timeout=30)
        
        if response.status_code != 200:
            return f"AI Service Error ({response.status_code})", response.status_code
        
        try:
            data = response.json()
            # Sirf 'text' field return karo – clean output
            if 'text' in data:
                return data['text']
            else:
                return "No response from AI."
        except:
            # Agar JSON nahi hai to direct text return
            return response.text
    
    except requests.exceptions.Timeout:
        return "Request timed out. Try again."
    except requests.exceptions.RequestException:
        return "Failed to connect to AI service."

# Render ke liye zaroori nahi, lekin safe rahega
if __name__ == '__main__':
    app.run()