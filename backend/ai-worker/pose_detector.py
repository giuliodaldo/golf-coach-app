"""
Pose Detection Module using MediaPipe
Extracts body landmarks and calculates angles from golf swing videos
"""

import logging
import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, List
import math

logger = logging.getLogger(__name__)

class PoseDetector:
    """
    Detects body pose landmarks from video using MediaPipe Pose
    """
    
    def __init__(self, model_complexity: int = 1, min_detection_confidence: float = 0.5):
        """
        Initialize MediaPipe Pose detector
        
        Args:
            model_complexity: 0-2, higher is more accurate but slower
            min_detection_confidence: Confidence threshold for detection
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence
        )
        
        # Important landmarks for golf swing analysis
        self.key_landmarks = {
            'left_shoulder': self.mp_pose.PoseLandmark.LEFT_SHOULDER.value,
            'right_shoulder': self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
            'left_elbow': self.mp_pose.PoseLandmark.LEFT_ELBOW.value,
            'right_elbow': self.mp_pose.PoseLandmark.RIGHT_ELBOW.value,
            'left_wrist': self.mp_pose.PoseLandmark.LEFT_WRIST.value,
            'right_wrist': self.mp_pose.PoseLandmark.RIGHT_WRIST.value,
            'left_hip': self.mp_pose.PoseLandmark.LEFT_HIP.value,
            'right_hip': self.mp_pose.PoseLandmark.RIGHT_HIP.value,
            'left_knee': self.mp_pose.PoseLandmark.LEFT_KNEE.value,
            'right_knee': self.mp_pose.PoseLandmark.RIGHT_KNEE.value,
            'left_ankle': self.mp_pose.PoseLandmark.LEFT_ANKLE.value,
            'right_ankle': self.mp_pose.PoseLandmark.RIGHT_ANKLE.value,
            'head': self.mp_pose.PoseLandmark.NOSE.value,
        }
        
        logger.info("✅ PoseDetector initialized")
    
    def extract_landmarks(self, video_path: str, skip_frames: int = 1) -> Optional[Dict]:
        """
        Extract pose landmarks from video
        
        Args:
            video_path: Path to video file
            skip_frames: Process every nth frame for speed
        
        Returns:
            Dictionary with landmarks at different swing phases
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return None
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Processing video: {total_frames} frames @ {fps}fps")
            
            landmarks_collection = {
                'address': [],  # Setup position
                'backswing': [],  # Max backswing
                'downswing': [],  # Transition
                'impact': [],  # Impact position
                'follow_through': [],  # Finish position
                'all_frames': []
            }
            
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                if frame_count % skip_frames != 0:
                    frame_count += 1
                    continue
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process frame
                results = self.pose.process(rgb_frame)
                
                if results.pose_landmarks:
                    landmarks_dict = self._extract_landmarks_dict(results.pose_landmarks)
                    landmarks_collection['all_frames'].append({
                        'frame': frame_count,
                        'timestamp': frame_count / fps,
                        'landmarks': landmarks_dict
                    })
                    
                    # Categorize by swing phase (simplified)
                    phase = self._classify_swing_phase(landmarks_dict, frame_count, total_frames)
                    if phase == 'address':
                        landmarks_collection['address'].append(landmarks_dict)
                    elif phase == 'backswing':
                        landmarks_collection['backswing'].append(landmarks_dict)
                    elif phase == 'downswing':
                        landmarks_collection['downswing'].append(landmarks_dict)
                    elif phase == 'impact':
                        landmarks_collection['impact'].append(landmarks_dict)
                    elif phase == 'follow_through':
                        landmarks_collection['follow_through'].append(landmarks_dict)
                
                frame_count += 1
            
            cap.release()
            
            logger.info(f"✅ Extracted landmarks from {frame_count} frames")
            
            return landmarks_collection if landmarks_collection['all_frames'] else None
            
        except Exception as e:
            logger.error(f"Error extracting landmarks: {e}")
            return None
    
    def _extract_landmarks_dict(self, pose_landmarks) -> Dict:
        """Convert MediaPipe landmarks to dictionary"""
        landmarks_dict = {}
        
        for name, idx in self.key_landmarks.items():
            landmark = pose_landmarks[idx]
            landmarks_dict[name] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        
        return landmarks_dict
    
    def _classify_swing_phase(self, landmarks: Dict, frame: int, total_frames: int) -> str:
        """Classify swing phase based on frame position and body position"""
        phase_ratio = frame / total_frames
        
        # Simplified phase classification
        if phase_ratio < 0.1:
            return 'address'
        elif phase_ratio < 0.4:
            return 'backswing'
        elif phase_ratio < 0.5:
            return 'downswing'
        elif phase_ratio < 0.6:
            return 'impact'
        else:
            return 'follow_through'
    
    def calculate_angle(self, p1: Dict, p2: Dict, p3: Dict) -> float:
        """
        Calculate angle between three points
        
        Args:
            p1, p2, p3: Points with x, y coordinates
        
        Returns:
            Angle in degrees
        """
        # Vector from p2 to p1
        v1 = np.array([p1['x'] - p2['x'], p1['y'] - p2['y']])
        # Vector from p2 to p3
        v2 = np.array([p3['x'] - p2['x'], p3['y'] - p2['y']])
        
        # Normalize vectors
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)
        
        # Calculate angle
        cos_angle = np.clip(np.dot(v1_norm, v2_norm), -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        return np.degrees(angle)
    
    def calculate_lag_angle(self, landmarks: Dict) -> Optional[float]:
        """
        Calculate lag angle (angle between club shaft and lead arm)
        Approximated from body landmarks
        
        Args:
            landmarks: Dictionary of body landmarks
        
        Returns:
            Lag angle in degrees
        """
        try:
            if not all(k in landmarks for k in ['left_wrist', 'left_elbow', 'left_shoulder']):
                return None
            
            # Calculate angle at wrist
            angle = self.calculate_angle(
                landmarks['left_shoulder'],
                landmarks['left_wrist'],
                landmarks['left_elbow']
            )
            
            # Adjust for golf-specific measurement
            lag_angle = max(0, 180 - angle)
            
            return round(lag_angle, 1)
            
        except Exception as e:
            logger.error(f"Error calculating lag angle: {e}")
            return None
    
    def calculate_shoulder_hip_rotation(self, landmarks: Dict) -> Optional[float]:
        """
        Calculate rotation differential between shoulders and hips
        
        Args:
            landmarks: Dictionary of body landmarks
        
        Returns:
            Rotation in degrees
        """
        try:
            # Calculate shoulder line angle
            left_shoulder = landmarks['left_shoulder']
            right_shoulder = landmarks['right_shoulder']
            shoulder_angle = math.atan2(
                right_shoulder['y'] - left_shoulder['y'],
                right_shoulder['x'] - left_shoulder['x']
            )
            
            # Calculate hip line angle
            left_hip = landmarks['left_hip']
            right_hip = landmarks['right_hip']
            hip_angle = math.atan2(
                right_hip['y'] - left_hip['y'],
                right_hip['x'] - left_hip['x']
            )
            
            # Calculate difference
            rotation = abs(math.degrees(shoulder_angle - hip_angle))
            
            return round(rotation, 1)
            
        except Exception as e:
            logger.error(f"Error calculating rotation: {e}")
            return None
    
    def assess_posture(self, landmarks: Dict) -> str:
        """
        Assess posture quality from landmarks
        
        Args:
            landmarks: Dictionary of body landmarks
        
        Returns:
            Posture rating: poor, fair, good, excellent
        """
        try:
            scores = 0
            
            # Check spine alignment (should be relatively straight)
            if landmarks['left_shoulder']['y'] < landmarks['left_hip']['y'] + 0.05:
                scores += 1
            
            # Check head position
            if 'head' in landmarks:
                head = landmarks['head']
                shoulder_mid_x = (landmarks['left_shoulder']['x'] + landmarks['right_shoulder']['x']) / 2
                if abs(head['x'] - shoulder_mid_x) < 0.1:
                    scores += 1
            
            # Check knee bend
            left_knee = landmarks['left_knee']['y']
            left_hip = landmarks['left_hip']['y']
            left_ankle = landmarks['left_ankle']['y']
            if left_knee > left_hip and left_knee < left_ankle:
                scores += 1
            
            # Assess result
            if scores >= 3:
                return 'excellent'
            elif scores >= 2:
                return 'good'
            elif scores >= 1:
                return 'fair'
            else:
                return 'poor'
            
        except Exception as e:
            logger.error(f"Error assessing posture: {e}")
            return 'unknown'
    
    def __del__(self):
        """Cleanup when object is deleted"""
        if hasattr(self, 'pose'):
            self.pose.close()
