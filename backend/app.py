import os
import uuid
import threading
from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def delete_file_after_delay(filepath, delay=300):
    """Deletes a file after a specified delay in seconds (default 5 mins)"""
    def delete():
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Deleted temporary file: {filepath}")
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")

    timer = threading.Timer(delay, delete)
    timer.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/json')

@app.route('/icon-<size>.png')
def serve_icon(size):
    return send_file(f'icon-{size}.png', mimetype='image/png')

@app.route('/api/convert', methods=['POST'])
def convert_to_mp3():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']

    # Generate a unique filename for this download
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f'%(title)s_{unique_id}.%(ext)s')

    # yt-dlp options for extracting best audio as mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # yt-dlp might change the extension, let's construct the actual filename
            title = info_dict.get('title', 'audio')
            # Clean title for filename (yt-dlp does this automatically in outtmpl,
            # but to be safe we find the generated file)

            # The actual output file will have .mp3 extension because of the postprocessor
            expected_filename = ydl.prepare_filename(info_dict)
            base_name, _ = os.path.splitext(expected_filename)
            actual_filepath = f"{base_name}.mp3"

            if os.path.exists(actual_filepath):
                # Schedule deletion after sending
                delete_file_after_delay(actual_filepath)

                # We need to return the file. Since send_file might need the file to exist
                # while it streams, the thread deletion is safe enough.
                # Use as_attachment=True to trigger download
                return send_file(
                    actual_filepath,
                    as_attachment=True,
                    download_name=f"{title}.mp3",
                    mimetype='audio/mpeg'
                )
            else:
                return jsonify({'error': 'Failed to convert or find the file.'}), 500

    except Exception as e:
        print(f"Error during conversion: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Listen on all interfaces so it can be accessed from a mobile phone on the same network
    app.run(host='0.0.0.0', port=5000, debug=True)
