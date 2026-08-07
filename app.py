from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea API is Live!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Bhai, link toh daalo!"})
    
    # Strictly ask for combined format (single file with video + audio)
    ydl_opts = {
        'format': 'b/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Instagram Reel')
            thumbnail = info.get('thumbnail', '')
            
            # Root level 'url' contains the direct Progressive MP4 with Audio
            download_url = info.get('url')
            
            # Backup check if root URL is missing
            if not download_url and 'formats' in info:
                for f in info['formats']:
                    vcodec = f.get('vcodec', 'none')
                    acodec = f.get('acodec', 'none')
                    if vcodec != 'none' and acodec != 'none':
                        download_url = f.get('url')
                        break

            if not download_url:
                return jsonify({"status": "error", "message": "Video stream nahi mila!"})

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
