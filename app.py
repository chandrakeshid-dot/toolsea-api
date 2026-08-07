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
    
    cookie_path = 'cookies.txt'
    
    # Universal format options for YouTube and Instagram
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
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
            
            # Extract direct download stream URL safely
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
