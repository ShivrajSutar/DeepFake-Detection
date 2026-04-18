import streamlit as st
import cv2
import numpy as np
import tempfile
import time
from forensics import VeriFireForensics

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Forensic AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyber-Noir Hackathon Aesthetic
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 10px; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'engine' not in st.session_state:
    st.session_state.engine = VeriFireForensics()
if 'analysis_active' not in st.session_state:
    st.session_state.analysis_active = False
if 'session_scores' not in st.session_state:
    st.session_state.session_scores = []

# --- SIDEBAR UI ---
st.sidebar.title("🔍 Control Center")
source_type = st.sidebar.radio("Select Input Source", ["Webcam", "Video File", "Static Image"])

uploaded_file = None
if source_type in ["Video File", "Static Image"]:
    uploaded_file = st.sidebar.file_uploader(f"Upload {source_type}", type=['mp4', 'mov', 'jpg', 'jpeg', 'png'])

st.sidebar.divider()

# Start/Stop Buttons
col_btn1, col_btn2 = st.sidebar.columns(2)
if col_btn1.button("▶ Start", use_container_width=True):
    st.session_state.analysis_active = True
    st.session_state.session_scores = []  # Clear previous data

if col_btn2.button("⏹ Stop", use_container_width=True):
    st.session_state.analysis_active = False

st.sidebar.info("""
**Monetization Model:**
- Free: Real/Authentic
- $0.50: Suspicious
- $5.00: Deepfake Bounty
""")

# --- MAIN DASHBOARD UI ---
st.title("🔥 DeepFake Detection")
st.caption("Industrial-Grade Deepfake Detection | Powered by EfficientNet-B7 & Swin-Transformer Logic")

col_main, col_stats = st.columns([2, 1])
frame_placeholder = col_main.empty()
live_metric_placeholder = col_stats.empty()

# --- CORE LOGIC: IMAGE PROCESSING ---
if source_type == "Static Image" and uploaded_file and st.session_state.analysis_active:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Process Image
    res_img, score, verdict = st.session_state.engine.analyze_frame(image)
    st.session_state.session_scores = [score]

    frame_placeholder.image(res_img, channels="BGR", use_container_width=True)
    st.session_state.analysis_active = False  # Single frame doesn't need a loop
    st.rerun()

# --- CORE LOGIC: VIDEO / WEBCAM LOOP ---
elif st.session_state.analysis_active:
    cap = None
    if source_type == "Webcam":
        cap = cv2.VideoCapture(1)  # Change to 1 if using external camera
    elif source_type == "Video File" and uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)

    if cap:
        while cap.isOpened() and st.session_state.analysis_active:
            ret, frame = cap.read()
            if not ret:
                st.session_state.analysis_active = False
                break

            # Analyze
            processed_frame, score, verdict = st.session_state.engine.analyze_frame(frame)
            st.session_state.session_scores.append(score)

            # Update UI
            frame_placeholder.image(processed_frame, channels="BGR", use_container_width=True)

            with live_metric_placeholder.container():
                st.subheader("Live Telemetry")
                color_text = "red" if verdict == "FAKE" else "green"
                st.markdown(f"Status: :{color_text}[{verdict}]")
                st.metric("Max AI Threat", f"{score:.1%}")
                st.progress(score)

        cap.release()
        st.rerun()

# --- FINAL FORENSIC REPORT ---
if not st.session_state.analysis_active and len(st.session_state.session_scores) > 0:
    scores = st.session_state.session_scores
    avg_score = sum(scores) / len(scores)
    peak_score = max(scores)
    final_verdict = "FAKE" if avg_score > 0.60 else "SUSPICIOUS" if avg_score > 0.35 else "REAL"

    # Monetization Calculation
    if peak_score > 0.51:
        fee, status = 5.00, "PREMIUM BOUNTY EARNED"
    elif peak_score > 0.40:
        fee, status = 0.50, "SERVICE FEE APPLIED"
    else:
        fee, status = 0.00, "FREE TIER (AUTHENTIC)"

    st.divider()
    st.balloons()

    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Final Verdict", final_verdict)
    res_col2.metric("Peak AI Signal", f"{peak_score:.2%}")
    res_col3.metric("Bounty/Invoice", f"${fee:.2f}", status)

    st.subheader("📈 Temporal Consistency Analysis")
    st.line_chart(scores)

    with st.expander("📄 View Detailed Forensic Logs"):
        st.code(f"""
        VERIFIRE MULTI-FACE REPORT v5.0
        --------------------------------------
        SESSION STATS:
        - Frames Analyzed:  {len(scores)}
        - Mean Probability: {avg_score:.5f}
        - Peak Probability: {peak_score:.5f}

        BILLING DATA:
        - Status:          {status}
        - Total Due:       ${fee:.2f}

        SYSTEM STACK:
        - Mesh: MediaPipe 478-Landmark
        - Logic: Jitter Variance + Symmetry
        --------------------------------------
        """)
        if fee > 0:
            st.button(f"Pay ${fee:.2f} to Download Forensic Certificate")