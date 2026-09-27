"""
Golf Swing Analysis Module
Analyzes pose landmarks and provides technical feedback
"""

import logging
from typing import Dict, List, Optional
import statistics

logger = logging.getLogger(__name__)

class SwingAnalyzer:
    """
    Analyzes golf swing mechanics from pose landmarks
    """
    
    def __init__(self):
        """Initialize analyzer with golf-specific metrics"""
        
        # Ideal ranges for different club types
        self.ideal_ranges = {
            'driver': {
                'lag_angle': (18, 28),
                'face_angle': (-5, 5),
                'shoulder_rotation': (80, 100),
                'hip_rotation': (40, 60),
            },
            'iron': {
                'lag_angle': (20, 30),
                'face_angle': (-3, 3),
                'shoulder_rotation': (75, 90),
                'hip_rotation': (35, 50),
            },
            'wedge': {
                'lag_angle': (25, 35),
                'face_angle': (-2, 2),
                'shoulder_rotation': (60, 75),
                'hip_rotation': (25, 40),
            }
        }
        
        # Common golf swing errors
        self.error_patterns = {
            'early_extension': {
                'description': 'Losing hip flexion too early in downswing',
                'severity': 'major',
                'tips': [
                    'Maintain hip bend through impact',
                    'Practice medicine ball rotational throws',
                    'Focus on staying connected'
                ]
            },
            'reverse_pivot': {
                'description': 'Weight stays on front leg during backswing',
                'severity': 'major',
                'tips': [
                    'Shift weight to back leg in backswing',
                    'Practice weight transfer drills',
                    'Feel the load on back leg'
                ]
            },
            'swaying': {
                'description': 'Excessive lateral movement during swing',
                'severity': 'moderate',
                'tips': [
                    'Focus on rotation, not lateral movement',
                    'Practice with feet together',
                    'Keep head still during backswing'
                ]
            },
            'casting': {
                'description': 'Releasing lag angle too early',
                'severity': 'major',
                'tips': [
                    'Delay wrist release until impact',
                    'Practice lag maintenance drills',
                    'Focus on width and lag'
                ]
            },
            'steep_angle': {
                'description': 'Attacking angle too steep into the ball',
                'severity': 'moderate',
                'tips': [
                    'Shallow out your attack angle',
                    'Practice sweeping motion',
                    'Focus on staying in plane'
                ]
            },
            'poor_posture': {
                'description': 'Slouching or hunching over the ball',
                'severity': 'moderate',
                'tips': [
                    'Maintain spine angle throughout swing',
                    'Practice with proper setup',
                    'Use mirror for form check'
                ]
            },
            'slow_tempo': {
                'description': 'Swing rhythm is too slow',
                'severity': 'minor',
                'tips': [
                    'Count: 1-2-3 for backswing, 1 for downswing',
                    'Practice with metronome',
                    'Smooth transition is key'
                ]
            },
            'fast_tempo': {
                'description': 'Swing rhythm is too quick',
                'severity': 'minor',
                'tips': [
                    'Slow down backswing',
                    'Pause at top briefly',
                    'Smooth tempo throughout'
                ]
            },
            'thin_strike': {
                'description': 'Hitting ball on upper part of clubface',
                'severity': 'major',
                'tips': [
                    'Move ball position back slightly',
                    'Lower hands at address',
                    'Focus on descending strike'
                ]
            },
            'fat_strike': {
                'description': 'Hitting ground before ball',
                'severity': 'major',
                'tips': [
                    'Move ball position forward',
                    'Improve weight transfer',
                    'Better sequence and timing'
                ]
            }
        }
        
        logger.info("✅ SwingAnalyzer initialized")
    
    def analyze(self, landmarks: Dict, club: str) -> Dict:
        """
        Analyze swing from landmarks
        
        Args:
            landmarks: Dictionary with pose landmarks from different frames
            club: Club type (driver, iron, wedge)
        
        Returns:
            Dictionary with analysis results
        """
        
        analysis = {
            'technical_score': 0,
            'lag_angle': None,
            'face_angle': None,
            'posture': 'unknown',
            'shoulder_rotation': None,
            'hip_rotation': None,
            'issues': [],
            'suggested_tips': [],
            'correction_focus': None,
            'confidence_score': 0.85
        }
        
        try:
            # Use frames from different swing phases
            if landmarks['impact']:
                impact_frame = landmarks['impact'][0] if landmarks['impact'] else None
                if impact_frame:
                    analysis['face_angle'] = self._estimate_face_angle(impact_frame)
            
            if landmarks['backswing']:
                backswing_frame = landmarks['backswing'][-1] if landmarks['backswing'] else None
                if backswing_frame:
                    analysis['lag_angle'] = self._estimate_lag_angle(backswing_frame)
            
            # Assess posture from address position
            if landmarks['address']:
                address_frame = landmarks['address'][0] if landmarks['address'] else None
                if address_frame:
                    analysis['posture'] = self._assess_posture_quality(address_frame)
            
            # Calculate rotation if we have frames
            if landmarks['all_frames'] and len(landmarks['all_frames']) > 1:
                analysis['shoulder_rotation'] = self._calculate_rotation_metrics(
                    landmarks['all_frames'], 'shoulder'
                )
                analysis['hip_rotation'] = self._calculate_rotation_metrics(
                    landmarks['all_frames'], 'hip'
                )
            
            # Detect errors
            analysis['issues'] = self._detect_errors(analysis, club)
            
            # Generate tips
            analysis['suggested_tips'] = self._generate_tips(analysis['issues'])
            
            # Calculate technical score
            analysis['technical_score'] = self._calculate_score(analysis, club)
            
            # Determine correction focus
            analysis['correction_focus'] = self._get_correction_focus(analysis['issues'])
            
            logger.info(f"Analysis complete: score={analysis['technical_score']}, issues={len(analysis['issues'])}")
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            analysis['confidence_score'] = 0.5
        
        return analysis
    
    def _estimate_lag_angle(self, landmarks: Dict) -> Optional[float]:
        """Estimate lag angle from pose landmarks"""
        try:
            # This is a simplified estimation
            # In a real scenario, you'd calculate from wrist, elbow, shoulder
            if all(k in landmarks for k in ['left_wrist', 'left_elbow', 'left_shoulder']):
                # Simplified calculation
                lag_angle = 22.0  # Default mid-range value
                return round(lag_angle, 1)
        except Exception as e:
            logger.error(f"Error estimating lag angle: {e}")
        
        return None
    
    def _estimate_face_angle(self, landmarks: Dict) -> Optional[float]:
        """Estimate club face angle at impact"""
        try:
            # Simplified estimation
            face_angle = 1.0  # Near neutral
            return round(face_angle, 1)
        except Exception as e:
            logger.error(f"Error estimating face angle: {e}")
        
        return None
    
    def _assess_posture_quality(self, landmarks: Dict) -> str:
        """Assess overall posture quality"""
        try:
            # Simplified posture assessment
            score = 0
            
            # Check if spine is relatively straight
            if 'left_shoulder' in landmarks and 'left_hip' in landmarks:
                shoulder_y = landmarks['left_shoulder']['y']
                hip_y = landmarks['left_hip']['y']
                if abs(shoulder_y - hip_y) > 0.1:
                    score += 1
            
            # Check knee bend
            if 'left_knee' in landmarks:
                score += 1
            
            if score >= 2:
                return 'good'
            elif score >= 1:
                return 'fair'
            else:
                return 'poor'
            
        except Exception as e:
            logger.error(f"Error assessing posture: {e}")
            return 'unknown'
    
    def _calculate_rotation_metrics(self, frames: List[Dict], rotation_type: str) -> Optional[float]:
        """Calculate shoulder or hip rotation"""
        try:
            if not frames:
                return None
            
            # Simplified rotation calculation
            if rotation_type == 'shoulder':
                return 90.0  # Average shoulder rotation
            elif rotation_type == 'hip':
                return 45.0  # Average hip rotation
            
        except Exception as e:
            logger.error(f"Error calculating rotation: {e}")
        
        return None
    
    def _detect_errors(self, analysis: Dict, club: str) -> List[str]:
        """Detect common swing errors"""
        errors = []
        
        try:
            # Check lag angle
            if analysis['lag_angle']:
                ideal_min, ideal_max = self.ideal_ranges[club]['lag_angle']
                if analysis['lag_angle'] < ideal_min:
                    errors.append('low_lag_angle')
                elif analysis['lag_angle'] > ideal_max:
                    errors.append('casting')
            
            # Check face angle
            if analysis['face_angle']:
                ideal_min, ideal_max = self.ideal_ranges[club]['face_angle']
                if analysis['face_angle'] < ideal_min:
                    errors.append('closed_face')
                elif analysis['face_angle'] > ideal_max:
                    errors.append('open_face')
            
            # Check posture
            if analysis['posture'] == 'poor':
                errors.append('poor_posture')
            
            # Add some demo errors for variety
            if len(errors) == 0:
                errors.append('slow_tempo')
            
        except Exception as e:
            logger.error(f"Error detecting errors: {e}")
        
        return errors[:3]  # Return top 3 errors
    
    def _generate_tips(self, errors: List[str]) -> List[str]:
        """Generate corrective tips based on detected errors"""
        tips = []
        
        for error in errors:
            if error in self.error_patterns:
                pattern = self.error_patterns[error]
                tips.extend(pattern['tips'][:2])  # Add first 2 tips
        
        return list(set(tips))[:4]  # Return unique tips, max 4
    
    def _calculate_score(self, analysis: Dict, club: str) -> float:
        """Calculate overall technical score 0-100"""
        try:
            score = 100.0
            
            # Deduct points for each error
            for error in analysis['issues']:
                if error in self.error_patterns:
                    severity = self.error_patterns[error]['severity']
                    deduction = {
                        'major': 15,
                        'moderate': 10,
                        'minor': 5
                    }
                    score -= deduction.get(severity, 10)
            
            # Ensure score is in valid range
            score = max(20, min(100, score))
            
            return round(score, 0)
            
        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return 70.0
    
    def _get_correction_focus(self, errors: List[str]) -> Optional[str]:
        """Determine primary correction focus"""
        if not errors:
            return "Maintain current form"
        
        # Priority order for focus
        priority_errors = ['casting', 'poor_posture', 'early_extension', 'reverse_pivot']
        
        for error in priority_errors:
            if error in errors:
                return f"Focus on: {error.replace('_', ' ').title()}"
        
        # Return first error if not in priority list
        return f"Work on: {errors[0].replace('_', ' ').title()}"
