1. System Design Architecture

The architecture is modular, separating the high-speed data ingestion from the computationally heavy inference engine.

Ingestion Layer: Captures frames at 30–60 FPS. It handles color-space conversion (BGR to RGB) and normalization.

Feature Extraction (The Backbone): * Geometric Stream: Uses the MediaPipe 478-Landmark Mesh to track facial topology.

Texture Stream: Analyzes high-frequency noise using EfficientNet logic to find "GAN-signatures" (areas where the AI has smoothed out natural skin pores).

Inference Engine: This is where your custom logic lives. It calculates the Variance (σ 
2
 ) of movement and Blink Symmetry.

Fusion Layer: A weighted averaging system that combines these scores. If the Geometry is "shaky" but the Texture is "clean," the system flags it as SUSPICIOUS rather than FAKE.

2. Forensic Workflow (Step-by-Step)

The workflow follows a strict sequential logic to ensure no data is lost during real-time processing:

1. Initialization: Model Loading: Loads the .task file and initializes the face_trackers dictionary for multi-face support.
2. Frame Pre-op: Resizing/Denoising: Frames are scaled to a standard resolution (e.g., 720p) to ensure the jitter calculation is consistent regardless of the camera used.
3. Detection: Landmark Mapping: The system identifies up to 5 faces. Each face is assigned a Track ID to prevent data cross-contamination.
4. Analysis:	Biometric Audit:	The system compares the current landmark positions against the face_trackers buffer to calculate the Velocity Gradient.
5. Verdict:	Thresholding:	If the "Synthetic Signal" exceeds 60%, the UI triggers a RED alert; above 85% triggers a BOUNTY event.
6. Archiving:	Session Logging:	All scores are saved to the session_scores list to generate the final line chart and invoice.


3. The "Bounty" Logic Integration

From a system design perspective, the monetization is a Triggered Event Listener:

Monitor: The analyze_frame function constantly returns a score.

Evaluate: The UI checks if score > threshold.

Flag: If the threshold is met, a bounty_flag is set to True.

Invoice: Upon stopping the session, the system queries the bounty_flag. If true, it looks up the peak score and generates the corresponding Invoice Amount ($5.00 for High Certainty).

4. Technical Hardware Requirements

For optimal performance of Forensic AI:

CPU: Multi-core (i5 or equivalent) to handle the 5-face parallel tracking.

GPU: Not strictly required but recommended for reducing latency in the EfficientNet texture analysis.

RAM: Minimum 8GB to maintain the temporal buffers for longer video files.
