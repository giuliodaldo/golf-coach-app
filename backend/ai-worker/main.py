#!/usr/bin/env python3
"""
SwingCoach Live - AI Worker
FastAPI server for real-time golf swing analysis using MediaPipe
"""

import os
import sys
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Import analysis modules
from pose_detector import PoseDetector
from swing_analyzer import SwingAnalyzer

# Load environment variables
load_dotenv()

# ============================================================================
# Logging Configuration
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI App
# ============================================================================
app = FastAPI(
    title="SwingCoach Live - AI Worker",
    description="Real-time golf swing analysis engine",
    version="1.0.0"
)

# ============================================================================
# Models
# ============================================================================
class AnalysisRequest(BaseModel):
    club: str
    angles: Optional[dict] = None
    metadata: Optional[dict] = None

class AnalysisResponse(BaseModel):
    success: bool
    swing_id: str
    technical_score: float
    lag_angle: Optional[float] = None
    face_angle: Optional[float] = None
    posture: Optional[str] = None
    issues: list[str] = []
    suggested_tips: list[str] = []
    correction_focus: Optional[str] = None
    processing_time_ms: float
    model_version: str = "mediapipe-1.0"
    confidence_score: float = 0.0

# ============================================================================
# Initialize AI Models
# ============================================================================
try:
    pose_detector = PoseDetector()
    swing_analyzer = SwingAnalyzer()
    logger.info("✅ AI models initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize AI models: {e}")
    sys.exit(1)

# ============================================================================
# Routes
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "models": {
            "pose_detector": "loaded",
            "swing_analyzer": "loaded"
        }
    }

@app.post("/api/analyze/swing", response_model=AnalysisResponse)
async def analyze_swing(
    file: UploadFile = File(...),
    club: str = "driver",
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Analyze a golf swing video
    
    Args:
        file: Video file (MP4, AVI, MOV)
        club: Golf club type (driver, iron, wedge)
    
    Returns:
        Analysis results with biomechanical metrics and suggestions
    """
    import time
    start_time = time.time()
    
    swing_id = file.filename.split('.')[0]
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Save temporary file
        temp_dir = Path(tempfile.gettempdir())
        temp_path = temp_dir / file.filename
        
        with open(temp_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        logger.info(f"Processing video: {file.filename} (club: {club})")
        
        # Extract pose landmarks from video
        landmarks = pose_detector.extract_landmarks(str(temp_path))
        
        if not landmarks:
            raise HTTPException(status_code=400, detail="Could not extract pose landmarks from video")
        
        # Analyze swing mechanics
        analysis_result = swing_analyzer.analyze(
            landmarks=landmarks,
            club=club
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Prepare response
        response = AnalysisResponse(
            success=True,
            swing_id=swing_id,
            technical_score=analysis_result.get("technical_score", 0),
            lag_angle=analysis_result.get("lag_angle"),
            face_angle=analysis_result.get("face_angle"),
            posture=analysis_result.get("posture"),
            issues=analysis_result.get("issues", []),
            suggested_tips=analysis_result.get("suggested_tips", []),
            correction_focus=analysis_result.get("correction_focus"),
            processing_time_ms=processing_time,
            confidence_score=analysis_result.get("confidence_score", 0.85)
        )
        
        # Clean up temp file
        background_tasks.add_task(os.remove, temp_path)
        
        logger.info(f"✅ Analysis complete: {swing_id} (score: {response.technical_score})")
        
        return response
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/batch")
async def analyze_batch(
    files: list[UploadFile] = File(...),
    club: str = "driver"
):
    """
    Analyze multiple swing videos in batch
    
    Args:
        files: List of video files
        club: Golf club type
    
    Returns:
        List of analysis results
    """
    results = []
    
    for file in files:
        try:
            # Process each file
            analysis = await analyze_swing(file, club)
            results.append(analysis)
        except Exception as e:
            logger.error(f"Failed to analyze {file.filename}: {e}")
            results.append({
                "success": False,
                "swing_id": file.filename,
                "error": str(e)
            })
    
    return {"results": results, "count": len(results)}

@app.get("/api/models/info")
async def get_models_info():
    """Get information about loaded models"""
    return {
        "pose_detector": {
            "type": "MediaPipe Pose Landmarker",
            "landmarks": 33,
            "version": "1.0"
        },
        "swing_analyzer": {
            "type": "Custom Golf Biomechanics",
            "metrics": [
                "lag_angle",
                "face_angle",
                "posture",
                "tempo",
                "alignment"
            ]
        }
    }

@app.get("/api/stats")
async def get_stats():
    """Get worker statistics"""
    return {
        "worker_id": os.getenv("WORKER_ID", "default"),
        "gpu_enabled": os.getenv("MEDIAPIPE_GPU", "false") == "true",
        "started_at": datetime.utcnow().isoformat(),
        "model_confidence_threshold": float(os.getenv("MEDIAPIPE_CONFIDENCE_THRESHOLD", 0.5))
    }

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("AI_WORKER_PORT", 8000))
    host = os.getenv("AI_WORKER_HOST", "0.0.0.0")
    
    logger.info(f"""
╔════════════════════════════════════════════════════════════════╗
║     🏌️  SwingCoach Live - AI Worker Starting                   ║
║                                                                ║
║  📍 Server: http://{host}:{port}                    
║  🧠 Model: MediaPipe Pose Landmarker v1.0                     ║
║  🔧 GPU: {os.getenv('MEDIAPIPE_GPU', 'false')}                          
║  🎯 Confidence Threshold: {os.getenv('MEDIAPIPE_CONFIDENCE_THRESHOLD', '0.5')}          
║                                                                ║
║  Endpoints:                                                    ║
║  - GET  /health                - Health check                 ║
║  - POST /api/analyze/swing     - Analyze single swing         ║
║  - POST /api/analyze/batch     - Batch analysis               ║
║  - GET  /api/models/info       - Model information            ║
║  - GET  /api/stats             - Worker statistics            ║
║                                                                ║
║  Docs: http://{host}:{port}/docs                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
