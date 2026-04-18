# DeepFake-Detection
Project Vision

Forensic AI is an enterprise-grade deepfake detection ecosystem designed for legal, journalistic, and corporate security sectors. By leveraging a multimodal detection ensemble, Forensic AI moves beyond simple pattern matching to provide a comprehensive biometric audit of digital media. Our system detects synthetic "shimmer," geometric inconsistencies, and temporal glitches that are invisible to the human eye.

The Three Pillars of Detection

Biometric Mesh Analysis: Maps 478 sub-pixel points to monitor for "Mask Shimmer"—the micro-vibrations occurring when generative models fail to perfectly anchor to human facial structures.

Texture Forensics: Utilizes spatial frequency analysis to identify "GAN Fingerprints," such as unnatural skin smoothing or inconsistent light distribution.

Temporal Consistency: Analyzes frame-to-frame stability to detect "Flicker Artifacts" common in high-end face-swap technology.

Key Features

Multi-Subject Forensic Tracking: Independently analyzes up to 5 faces simultaneously, assigning a unique threat-score to each individual in the frame.

Real-Time Telemetry: Provides a live "Synthetic Probability" graph, allowing users to identify the exact second a video was manipulated.

Hybrid Media Support: A unified engine for Live Streams, Video Forensics, and High-Resolution Image Audits.

Monetization: The "Bounty" Logic

Forensic AI operates on a Value-Based Billing model, ensuring that security is accessible while high-stakes detections are monetized:

AI Signal <40% = Free
AI Signal >40% & <51% = 0.50$
AI Signal >51% = 5.00$
Technical Implementation

Backend: Python 3.10, Flask/Streamlit, MediaPipe Vision.

Models: EfficientNet-B7 backbone with customized landmark variance tracking.

Deployment: Scalable container-ready architecture for cloud or local forensic workstations.

Installation

Bash
git clone https://github.com/your-username/Forensic-AI.git/n
cd Forensic-AI/n
pip install -r requirements.txt
streamlit run app.py
Forensic AI: Because in the age of generative synthesis, seeing is no longer believing.
