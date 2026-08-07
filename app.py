from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea API is live with Audio Fix!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Bhai, link toh daalo!"})
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Instagram Video')
            thumbnail = info.get('thumbnail', '')
            
            download_url = None
            
            # 1. Sabse pehle pre-merged file dhoondhenge jisme Video aur Audio dono hon
            if 'formats' in info:
                for f in reversed(info['formats']):
                    vcodec = f.get('vcodec')
                    acodec = f.get('acodec')
                    
                    # Fix: Handle both None object and 'none' string safely
                    has_video = vcodec is not None and vcodec != 'none'
                    has_audio = acodec is not None and acodec != 'none'
                    
                    if has_video and has_audio:
                        download_url = f.get('url')
                        break
            
            # 2. Agar merged file na mile, toh direct default url use karein
            if not download_url:
                download_url = info.get('url')
                
            # 3. Last fallback (agar kuch na mile toh aakhri format le lo)
            if not download_url and 'formats' in info:
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
