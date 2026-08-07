from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea Python Cloud API is live and running!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Bhai, link toh daalo!"})
    
    # yt-dlp options for universal downloading
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Downloaded Media')
            thumbnail = info.get('thumbnail', '')
            
            # Direct video/media stream URL
            download_url = info.get('url')
            if not download_url and 'formats' in info:
                # Fallback to best format URL
                formats = info['formats']
                download_url = formats[-1].get('url')
                
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
