from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from config import *
from services.photo_processor import PhotoProcessor
from services.context_generator import ContextGenerator
from services.gemini_service import GeminiService
from services.working_cinematic_generator import WorkingCinematicGenerator as VideoGenerator

app = Flask(__name__)
CORS(app)

# Configure upload settings
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Initialize services
photo_processor = PhotoProcessor()
context_generator = ContextGenerator()
video_generator = VideoGenerator()
gemini_service = GeminiService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photos():
    try:
        if 'photos' not in request.files:
            return jsonify({'error': 'No photos uploaded'}), 400
        
        files = request.files.getlist('photos')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Process uploaded photos
        photo_paths = []
        for file in files:
            if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                photo_paths.append(file_path)
        
        if not photo_paths:
            return jsonify({'error': 'No valid image files uploaded'}), 400
        
        # Order photos chronologically
        print(f"Original photo order: {[os.path.basename(p) for p in photo_paths]}")
        ordered_photo_paths = photo_processor.order_photos(photo_paths)
        print(f"Chronologically ordered photos: {[os.path.basename(p) for p in ordered_photo_paths]}")
        
        # Generate context using BERT5
        context = context_generator.generate_context(ordered_photo_paths)
        
        # Get video plan from Gemini
        video_plan = gemini_service.plan_video(ordered_photo_paths, context)
        
        return jsonify({
            'success': True,
            'photo_count': len(ordered_photo_paths),
            'context': context,
            'video_plan': video_plan,
            'photo_paths': ordered_photo_paths
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        photo_paths = data.get('photo_paths', [])
        context = data.get('context', '')
        video_plan = data.get('video_plan', {})
        
        if not photo_paths:
            return jsonify({'error': 'No photos provided'}), 400
        
        # Generate video
        output_path = video_generator.create_video(
            photo_paths=photo_paths,
            context=context,
            video_plan=video_plan
        )
        
        return jsonify({
            'success': True,
            'video_path': output_path,
            'download_url': f'/download/{os.path.basename(output_path)}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
