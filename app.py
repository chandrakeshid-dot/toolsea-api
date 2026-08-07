from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea API Perfect Audio Stream Live!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Bhai, link daalo!"})
    
    # 'format' option hata diya hai taaki hum saare formats nikal kar khud best wala chunein
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Instagram Video')
            thumbnail = info.get('thumbnail', '')
            
            download_url = None
            formats = info.get('formats', [])
            
            # Master Trick: Sirf 'Progressive MP4' (bina DASH wale) stream dhoondho jisme audio aur video humesha sath hote hain
            valid_formats = [
                f for f in formats 
                if f.get('ext') == 'mp4' 
                and 'dash' not in f.get('format_id', '').lower()
            ]
            
            if valid_formats:
                # Unme se sabse high quality (resolution) wali file uthao
                valid_formats.sort(key=lambda x: x.get('height', 0) or 0)
                download_url = valid_formats[-1].get('url')
            else:
                # Agar koi filter match na kare toh default combined link de do
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
