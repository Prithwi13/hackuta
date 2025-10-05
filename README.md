# Memory Video Creator 🎬

Transform your photos into beautiful memory videos with AI-powered context generation and smart video planning.

## Features

### 🔹 Core (MVP)
- **Photo Upload & Ordering**: Drag and drop multiple photos with automatic chronological ordering
- **AI Context Generation**: BERT5 model analyzes photos to generate descriptive context
- **Smart Video Planning**: Gemini AI suggests optimal photo sequence, transitions, and music
- **Video Generation**: Create videos with smooth transitions and background music
- **Export Ready**: Download your memory video in high quality

### 🔹 Smart Improvements
- **Automatic Storytelling**: AI-generated voice-over and captions
- **Emotion Detection**: Highlight best photos based on emotional content
- **Dynamic Effects**: Ken Burns zoom, mood-based transitions
- **Music Personalization**: AI-matched background music
- **Compression**: Replace 100 photos with 1 memory video

### 🔹 Wow Factors
- **Themes & Styles**: Travel Vlog, Birthday, Retro themes
- **Interactive Captions**: AI suggests captions you can edit
- **Social Media Ready**: Multiple aspect ratios (16:9, 9:16, square)
- **Timeline Integration**: Use photo metadata for chronological ordering
- **Group Sharing**: Merge photos from multiple people

## Technology Stack

- **Backend**: Flask (Python)
- **AI Models**: 
  - BERT5 for image captioning and context generation
  - Google Gemini for video planning and analysis
- **Video Processing**: MoviePy for video generation
- **Frontend**: HTML5, CSS3, JavaScript
- **Image Processing**: PIL, OpenCV

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hackuta
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   - The Gemini API key is already configured in `config.py`
   - Create necessary directories:
     ```bash
     mkdir -p uploads outputs static
     ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload Photos**: Drag and drop or click to select multiple photos
2. **AI Processing**: The app automatically:
   - Orders photos chronologically
   - Generates context using BERT5
   - Plans video with Gemini AI
3. **Video Generation**: Creates a professional video with:
   - Smooth transitions
   - Ken Burns effects
   - Background music
4. **Download**: Get your ready-to-share memory video

## API Endpoints

- `POST /upload` - Upload photos and generate context
- `POST /generate_video` - Create video from photos and context
- `GET /download/<filename>` - Download generated video

## Project Structure

```
hackuta/
├── app.py                 # Main Flask application
├── config.py             # Configuration and API keys
├── requirements.txt      # Python dependencies
├── services/             # Core services
│   ├── photo_processor.py    # Photo processing and ordering
│   ├── context_generator.py # BERT5 context generation
│   ├── gemini_service.py    # Gemini AI integration
│   └── video_generator.py   # Video creation with MoviePy
├── templates/            # HTML templates
│   └── index.html
├── static/              # Static assets
│   ├── css/style.css
│   └── js/script.js
├── uploads/             # Uploaded photos
└── outputs/             # Generated videos
```

## Features in Detail

### AI Context Generation
- Uses BERT5 (Vision Transformer + GPT-2) for image captioning
- Generates individual captions for each photo
- Creates overall context describing the photo collection
- Extracts themes and emotions from the images

### Smart Video Planning
- Gemini AI analyzes photo content and context
- Suggests optimal photo sequence
- Recommends transitions and effects
- Plans music style and video pacing

### Video Generation
- Professional transitions (fade, slide, zoom)
- Ken Burns effect for dynamic movement
- Background music integration
- Multiple export formats for social media

## Future Enhancements

- **AI Avatars**: Virtual narrators for storytelling
- **Memory Summaries**: Generate blog posts alongside videos
- **Searchable Memories**: Tag and search through video collections
- **Advanced Effects**: More transition types and visual effects
- **Cloud Storage**: Save and sync videos across devices

## Contributing

This is a hackathon project showcasing AI-powered video creation. Feel free to fork and enhance!

## License

MIT License - feel free to use and modify for your projects.



