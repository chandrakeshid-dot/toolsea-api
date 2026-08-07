from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea API is live!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Bhai, link toh daalo!"})
    
    # Force yt-dlp to pick ONLY formats with BOTH video and audio combined
    ydl_opts = {
        'format': 'best[vcodec!=none][acodec!=none]/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Instagram Video')
            thumbnail = info.get('thumbnail', '')
            
            download_url = None
            
            # Filter formats to ensure format is not DASH video-only
            if 'formats' in info:
                valid_formats = [
                    f for f in info['formats']
                    if f.get('vcodec') not in (None, 'none') 
                    and f.get('acodec') not in (None, 'none')
                    and 'dash' not in f.get('format_id', '').lower()
                ]
                if valid_formats:
                    download_url = valid_formats[-1].get('url')
            
            # Fallback if no specific filter matches
            if not download_url:
                download_url = info.get('url')
                
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
