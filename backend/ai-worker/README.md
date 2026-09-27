# SwingCoach Live - AI Worker

FastAPI server for real-time golf swing analysis using MediaPipe Pose Landmarker.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# API docs available at
# http://localhost:8000/docs
```

## 🎯 What It Does

- **Pose Detection**: Extracts 33 body landmarks from golf swing videos
- **Angle Calculation**: Calculates lag angle, face angle, and rotation
- **Error Detection**: Identifies common golf swing errors
- **Scoring**: Rates swing quality 0-100
- **Recommendations**: Provides corrective tips and drills

## 📁 Project Structure

```
backend/ai-worker/
├── main.py                # FastAPI app entry point
├── pose_detector.py       # MediaPipe Pose extraction
├── swing_analyzer.py      # Swing analysis logic
├── models/               # ML models directory
│   └── mediapipe_pose_landmarker.task
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🔌 API Endpoints

### Health Check

```
GET /health

Response:
{
  "status": "ok",
  "timestamp": "2024-01-15T09:00:00Z",
  "models": {
    "pose_detector": "loaded",
    "swing_analyzer": "loaded"
  }
}
```

### Analyze Single Swing

```
POST /api/analyze/swing
Content-Type: multipart/form-data

Parameters:
- file: (video file) *.mp4, *.avi, *.mov, *.mkv
- club: (string) driver, iron, or wedge

Response (200):
{
  "success": true,
  "swing_id": "swing-123",
  "technical_score": 78.5,
  "lag_angle": 22.5,
  "face_angle": 1.2,
  "posture": "good",
  "issues": ["slow_tempo", "slight_sway"],
  "suggested_tips": [
    "Increase backswing tempo",
    "Keep centered during swing"
  ],
  "correction_focus": "Focus on: Slow Tempo",
  "processing_time_ms": 2450,
  "confidence_score": 0.92
}
```

### Batch Analysis

```
POST /api/analyze/batch
Content-Type: multipart/form-data

Parameters:
- files: (multiple video files)
- club: (string) driver, iron, or wedge

Response:
{
  "results": [
    { ...analysis result... },
    { ...analysis result... }
  ],
  "count": 2
}
```

### Model Information

```
GET /api/models/info

Response:
{
  "pose_detector": {
    "type": "MediaPipe Pose Landmarker",
    "landmarks": 33,
    "version": "1.0"
  },
  "swing_analyzer": {
    "type": "Custom Golf Biomechanics",
    "metrics": ["lag_angle", "face_angle", "posture", "tempo"]
  }
}
```

### Worker Statistics

```
GET /api/stats

Response:
{
  "worker_id": "default",
  "gpu_enabled": false,
  "started_at": "2024-01-15T09:00:00Z",
  "model_confidence_threshold": 0.5
}
```

## 🧠 AI Models

### MediaPipe Pose Landmarker

Detects 33 body landmarks with sub-pixel accuracy:

```
Landmarks include:
- Nose, eyes, ears (head)
- Shoulders, elbows, wrists (arms)
- Hips, knees, ankles (legs)
- And 12 more for full body tracking
```

### Swing Analyzer

Custom model trained on golf biomechanics:

**Metrics calculated:**
- Lag angle (club shaft vs arm angle)
- Face angle (club face relative to target line)
- Posture quality (spine and stance)
- Shoulder-hip rotation differential
- Swing tempo rating

**Errors detected:**
- Casting (early lag release)
- Early extension (losing hip bend)
- Reverse pivot (weight stays forward)
- Swaying (lateral movement)
- And 6 more common errors

## 🔧 Configuration

### Environment Variables

```
PYTHON_ENV=development          # development or production
AI_WORKER_PORT=8000            # Server port
AI_WORKER_HOST=0.0.0.0         # Server host
MEDIAPIPE_GPU=false            # Enable GPU (if available)
MEDIAPIPE_CONFIDENCE_THRESHOLD=0.5  # Pose confidence (0-1)
MODEL_PATH=./models            # Models directory
```

### Performance Settings

```python
# In PoseDetector
model_complexity=1  # 0=faster, 2=most accurate
min_detection_confidence=0.5
smooth_landmarks=True  # Reduce jitter
```

## 📊 Analysis Result Format

```python
{
    "success": bool,
    "swing_id": "str",              # Video filename without extension
    
    # Technical Metrics
    "technical_score": float,       # 0-100
    "lag_angle": float,             # Degrees
    "face_angle": float,            # Degrees
    "posture": str,                 # poor, fair, good, excellent
    "shoulder_rotation": float,     # Degrees
    "hip_rotation": float,          # Degrees
    
    # Analysis Results
    "issues": list[str],            # Error types detected
    "suggested_tips": list[str],    # Corrective tips
    "correction_focus": str,        # Primary focus area
    
    # Metadata
    "processing_time_ms": float,    # Analysis duration
    "model_version": str,           # mediapipe-1.0
    "confidence_score": float       # 0-1 confidence
}
```

## 🎬 Video Input Requirements

**Optimal:**
- Format: MP4 (H.264 codec)
- Resolution: 720p (1280×720)
- FPS: 30 fps
- Duration: 1-3 seconds
- File size: < 50MB

**Acceptable:**
- Format: AVI, MOV, MKV
- Resolution: 480p - 1080p
- FPS: 24-60 fps
- Duration: < 5 seconds
- File size: < 100MB

**Won't work:**
- Very low resolution (< 480p)
- Extreme angles (camera too low/high)
- Very dark/bright conditions
- Multiple people in frame

## 🚀 Performance

| Operation | Time | Hardware |
|-----------|------|----------|
| Pose extraction | 50-200ms | CPU (single frame) |
| Full video analysis | 2-10s | CPU (30 frames) |
| Batch 5 videos | 20-50s | CPU (parallel) |
| With GPU | 50% faster | NVIDIA GPU |

**Optimization tips:**
- Use 720p resolution for speed
- Process at 15 FPS instead of 30
- Enable GPU if available
- Batch process multiple videos

## 🔍 Pose Landmarks

Full list of 33 landmarks:

```
Head (0-10):
  0: Nose
  1: Left Eye Inner
  2: Left Eye
  3: Left Eye Outer
  4: Right Eye Inner
  5: Right Eye
  6: Right Eye Outer
  7: Left Ear
  8: Right Ear

Arms (9-20):
  9: Mouth Left
  10: Mouth Right
  11: Left Shoulder
  12: Right Shoulder
  13: Left Elbow
  14: Right Elbow
  15: Left Wrist
  16: Right Wrist

Hands (17-20):
  17: Left Pinky
  18: Right Pinky
  19: Left Index
  20: Right Index

Legs (21-32):
  21: Left Hip
  22: Right Hip
  23: Left Knee
  24: Right Knee
  25: Left Ankle
  26: Right Ankle
  27: Left Heel
  28: Right Heel
  29: Left Foot Index
  30: Right Foot Index

Full Body:
  31: Left Wrist (repeated)
  32: Right Wrist (repeated)
```

## 🧪 Testing

```bash
# Test with sample video
curl -X POST "http://localhost:8000/api/analyze/swing" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_swing.mp4" \
  -F "club=driver"

# Test health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## 🐛 Debugging

### Enable Debug Logging

```bash
LOG_LEVEL=debug python main.py
```

### Check Pose Detection

```python
from pose_detector import PoseDetector

detector = PoseDetector()
landmarks = detector.extract_landmarks('video.mp4')

# Print frame count
print(f"Processed {len(landmarks['all_frames'])} frames")

# Check first frame
first_frame = landmarks['all_frames'][0]
print(first_frame['landmarks']['left_shoulder'])
```

### Verify MediaPipe Installation

```bash
python -c "import mediapipe as mp; print(mp.__version__)"
# Should print: 0.10.7 or similar
```

## 🔒 Security

- File uploads have size limits (100MB max)
- Only specific video formats accepted
- Files processed then deleted
- No persistent storage of uploads
- API validates all inputs

## 📚 Dependencies

### Core
- **fastapi**: Web framework
- **uvicorn**: ASGI server

### AI/ML
- **mediapipe**: Pose detection
- **opencv-python**: Video processing
- **numpy**: Numerical computation

### Utilities
- **python-multipart**: File uploads
- **pydantic**: Data validation
- **python-dotenv**: Environment config

## 🔄 Processing Pipeline

```
1. Video Upload
   ↓
2. OpenCV reads video frames
   ↓
3. MediaPipe extracts pose landmarks
   ↓
4. PoseDetector processes landmarks
   ↓
5. SwingAnalyzer scores and analyzes
   ↓
6. Generates metrics and recommendations
   ↓
7. Returns JSON response
   ↓
8. Temp files deleted
```

## 🚀 Production Deploy

### Docker

```bash
docker build -t golf-coach-ai-worker .
docker run -p 8000:8000 golf-coach-ai-worker
```

### With GPU Support

```bash
docker run \
  --gpus all \
  -e MEDIAPIPE_GPU=true \
  -p 8000:8000 \
  golf-coach-ai-worker
```

### Railway Deployment

```bash
# Set environment
AI_WORKER_PORT=8000
MEDIAPIPE_GPU=false  # Railway doesn't provide GPU

# Start command
python main.py
```

## 📈 Monitoring

Monitor these metrics:

- **Response time**: Should be < 5s for most videos
- **CPU usage**: 100% during processing, idle afterward
- **Memory usage**: Peak ~500MB during analysis
- **Error rate**: Should be < 1%
- **Model confidence**: Check confidence_score >= 0.8

## 🤝 Contributing

Code style:
- Python 3.9+ syntax
- Type hints required
- Docstrings for functions
- Max line length: 100 chars

## 📖 Resources

- [MediaPipe Docs](https://mediapipe.readthedocs.io)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [OpenCV Guide](https://docs.opencv.org)
- [NumPy Tutorial](https://numpy.org/doc)

## 📝 License

MIT License - see LICENSE file
