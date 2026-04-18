import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class VeriFireForensics:
    def __init__(self, model_path='face_landmarker.task'):
        # CRITICAL: We use IMAGE mode because it is the most versatile for both images and video frames
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=5,  # Multi-face enabled
            output_face_blendshapes=True)
        self.detector = vision.FaceLandmarker.create_from_options(options)

        # State tracking
        self.prev_landmarks = None
        self.velocity_history = []

    def analyze_frame(self, frame):
        # 1. Standardize input
        if frame is None:
            return None, 0.0, "ERROR"

        h, w, _ = frame.shape

        # 2. Convert to MediaPipe format
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 3. Detect
        result = self.detector.detect(mp_img)

        if not result or not result.face_landmarks or len(result.face_landmarks) == 0:
            return frame, 0.0, "NO FACE DETECTED"

        max_frame_score = 0.0

        # 4. Process Every Face Found (Multi-face)
        for i, face_lms in enumerate(result.face_landmarks):
            # --- Biometric Jitter Logic ---
            current_lms = np.array([[lm.x, lm.y, lm.z] for lm in face_lms])
            jitter_score = 0.05  # Base noise

            if self.prev_landmarks is not None and len(self.prev_landmarks) == len(current_lms):
                movement = np.linalg.norm(current_lms - self.prev_landmarks, axis=1)
                self.velocity_history.append(np.mean(movement))
                if len(self.velocity_history) > 20: self.velocity_history.pop(0)

                # If too still (frozen AI) or too shaky (bad mask overlay)
                v_var = np.var(self.velocity_history)
                if v_var < 0.000001 or v_var > 0.005:
                    jitter_score += 0.4

            self.prev_landmarks = current_lms

            # --- Symmetry Logic ---
            if result.face_blendshapes and len(result.face_blendshapes) > i:
                shapes = {bs.category_name: bs.score for bs in result.face_blendshapes[i]}
                # AI blinks are often perfectly identical; humans are slightly off
                if abs(shapes['eyeBlinkLeft'] - shapes['eyeBlinkRight']) < 0.001:
                    jitter_score += 0.25

            # Final Face Score
            score = min(max(jitter_score + np.random.uniform(0.01, 0.05), 0.0), 0.99)
            if score > max_frame_score:
                max_frame_score = score

            # --- Drawing ---
            color = (0, 0, 255) if score > 0.60 else (0, 255, 0)  # Red if Fake, Green if Real
            for lm in face_lms:
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 1, color, -1)

            # Text Tag
            cv2.putText(frame, f"ID {i}: {score:.1%}", (int(face_lms[0].x * w), int(face_lms[0].y * h) - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        verdict = "FAKE" if max_frame_score > 0.60 else "SUSPICIOUS" if max_frame_score > 0.35 else "REAL"
        return frame, max_frame_score, verdict