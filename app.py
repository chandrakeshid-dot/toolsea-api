from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea Python Cloud API is live and running!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Bhai, link toh daalo!"})
    
    cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')
    
    # Real Browser User-Agent and Cookies configuration
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Downloaded Media')
            thumbnail = info.get('thumbnail', '')
            
            download_url = info.get('url')
            if not download_url and 'requested_formats' in info:
                download_url = info['requested_formats'][0].get('url')
            elif not download_url and 'formats' in info:
                download_url = info['formats'][-1].get('url')
                
            return jsonify({
                "status": "success",
                "data": {
                    "title": title,
                    "thumbnail": thumbnail,
                    "download_url": download_url
                }
            })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error: " + str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
