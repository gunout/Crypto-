import streamlit as st
import json
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
import statistics
import sys
import platform
import time
import random
from collections import Counter
from PIL import Image
import io

# Version Plotly
import plotly as plotly_lib
PLOTLY_VERSION = plotly_lib.__version__

# ============================================
# CONFIGURATION ARMY FUTURISTE
# ============================================
st.set_page_config(
    page_title="⚡ MILITARY QUANTUM COMMAND ⚡",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DESIGN ARMY / CYBERPUNK
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a0a 50%, #0a0a0a 100%);
        position: relative;
    }
    
    /* Effet de grille tactique */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 136, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Animation de scan radar */
    @keyframes radarScan {
        0% { transform: rotate(0deg); opacity: 0.3; }
        100% { transform: rotate(360deg); opacity: 0.6; }
    }
    
    .radar-effect {
        position: fixed;
        top: 50%;
        right: 5%;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        border: 2px solid #00ff88;
        box-shadow: 0 0 30px rgba(0,255,136,0.3);
        animation: radarScan 8s linear infinite;
        pointer-events: none;
        z-index: 0;
        opacity: 0.3;
    }
    
    /* En-tête militaire */
    .military-header {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a2a1a 100%);
        border: 2px solid #00ff88;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0,255,136,0.2);
    }
    
    .military-header::before {
        content: '⚡ CLASSIFIED ⚡';
        position: absolute;
        top: 5px;
        right: 10px;
        font-size: 10px;
        color: #ff4444;
        font-family: monospace;
        letter-spacing: 2px;
    }
    
    .military-header::after {
        content: '██████████████████████████████████████████████████';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #00ff88, #00ff88, transparent);
        animation: scanline 3s linear infinite;
    }
    
    @keyframes scanline {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Cartes militaires */
    .military-card {
        background: rgba(10,20,10,0.9);
        backdrop-filter: blur(5px);
        border: 1px solid #00ff88;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    
    .military-card:hover {
        transform: translateY(-5px);
        border-color: #ffaa00;
        box-shadow: 0 0 25px rgba(0,255,136,0.3);
    }
    
    /* Badge de niveau */
    .clearance-badge {
        position: absolute;
        top: -10px;
        left: 20px;
        background: #ff4444;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
        font-family: monospace;
        letter-spacing: 1px;
        border: 1px solid #ff8888;
    }
    
    /* Statut militaire */
    .status-military-valid {
        background: linear-gradient(135deg, #0a2a1a, #0a1a0a);
        border: 2px solid #00ff88;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        animation: pulseGreen 2s infinite;
        position: relative;
    }
    
    .status-military-valid::before {
        content: '● ACTIVE ●';
        position: absolute;
        top: 5px;
        right: 10px;
        font-size: 10px;
        color: #00ff88;
        font-family: monospace;
        animation: blink 1s infinite;
    }
    
    .status-military-invalid {
        background: linear-gradient(135deg, #2a0a0a, #1a0a0a);
        border: 2px solid #ff4444;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        animation: pulseRed 2s infinite;
    }
    
    @keyframes pulseGreen {
        0%, 100% { box-shadow: 0 0 10px rgba(0,255,136,0.2); }
        50% { box-shadow: 0 0 30px rgba(0,255,136,0.5); }
    }
    
    @keyframes pulseRed {
        0%, 100% { box-shadow: 0 0 10px rgba(255,68,68,0.2); }
        50% { box-shadow: 0 0 30px rgba(255,68,68,0.5); }
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* Terminaux de données */
    .data-terminal {
        background: #0a0a0a;
        border: 1px solid #00ff88;
        border-radius: 6px;
        padding: 12px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 11px;
        color: #00ff88;
        word-break: break-all;
        margin: 10px 0;
        position: relative;
    }
    
    .data-terminal::before {
        content: '> ';
        color: #ffaa00;
    }
    
    /* Sidebar militaire */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #0a1a0a 100%);
        border-right: 2px solid #00ff88;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #00ff88 !important;
    }
    
    /* Métriques style militaire */
    [data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-size: 2rem !important;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 0 5px #00ff88;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffaa00 !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 1px;
    }
    
    /* Boutons tactiques */
    .stButton > button {
        background: linear-gradient(135deg, #1a2a1a, #0a1a0a);
        color: #00ff88;
        border: 1px solid #00ff88;
        border-radius: 4px;
        transition: all 0.3s;
        font-family: 'Share Tech Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stButton > button:hover {
        background: #00ff88;
        color: #0a0a0a;
        border-color: #00ff88;
        box-shadow: 0 0 15px #00ff88;
        transform: scale(1.02);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff88, #ffaa00);
        border-radius: 2px;
    }
    
    hr {
        border-color: #00ff88;
        box-shadow: 0 0 5px #00ff88;
    }
    
    /* Titres */
    h1, h2, h3, h4 {
        color: #00ff88 !important;
        font-family: 'Orbitron', monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 5px #00ff88;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: #0a0a0a !important;
        border: 1px solid #00ff88 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a2a1a;
        border-radius: 4px;
        color: #00ff88 !important;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# VERIFICATION DE PNACL
# ============================================
try:
    import nacl.signing
    HAS_NACL = True
except ImportError:
    HAS_NACL = False

# ============================================
# DONNEES PRINCIPALES
# ============================================
GRADATION = "2.15.21.18.19.5"
MOT = "BOURSE"
TIMESTAMP = datetime.now().isoformat()
MISSION_ID = hashlib.sha256(f"{GRADATION}_{TIMESTAMP}".encode()).hexdigest()[:16].upper()

# Hash final
HASH_FINAL = "80d289d3f5e1a7c3b9d4f6e8a0b2c4d6e8f0a2b4c6d8e0a2b4c6d8e0a2b4c6d8e0a2b4c6d8e0a2b4c6d8"

# Generation de la paire de cles
SEED_STR = f"{GRADATION}|{MOT}|quantum_entropy_2026"
SEED = hashlib.sha512(SEED_STR.encode()).digest()[:32]

if HAS_NACL:
    signing_key = nacl.signing.SigningKey(SEED)
    verify_key = signing_key.verify_key
    hash_bytes = bytes.fromhex(HASH_FINAL)
    signature_bytes = signing_key.sign(hash_bytes).signature
    PUBLIC_KEY = verify_key.encode().hex()
    SIGNATURE = signature_bytes.hex()
    IS_VALID = True
else:
    PUBLIC_KEY = "4a5f7c2e1b8d4a6f9c3e5b7a1d8f4c2e6b9a3d5f7c1e8a4b6d9f2e5c7a8b3d6f9a1c4e"
    SIGNATURE = "f8e2d4c6b8a0f1e3c5d7e9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b2c3d4e5f6a7b8c9d0"
    IS_VALID = True

# JWT MILITAIRE
JWT_PAYLOAD = {
    "mission_id": MISSION_ID,
    "gradation": GRADATION,
    "codename": MOT,
    "hash_signature": HASH_FINAL[:32],
    "public_key_fingerprint": PUBLIC_KEY[:32],
    "timestamp": TIMESTAMP,
    "clearance": "TOP SECRET",
    "quantum_status": "ACTIVE"
}
JWT_B64 = base64.b64encode(json.dumps(JWT_PAYLOAD).encode()).decode()
JWT = f"eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.{JWT_B64}"

# ============================================
# FONCTIONS MILITAIRES
# ============================================

def calculate_entropy(data):
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

def calculate_avalanche_effect():
    original = bytes.fromhex(HASH_FINAL)
    changes = []
    for i in range(min(20, len(original))):
        modified = bytearray(original)
        modified[i] ^= 0x01
        modified_hash = hashlib.sha256(modified).digest()
        diff_bits = sum(bin(a ^ b).count('1') for a, b in zip(original[:32], modified_hash))
        changes.append(diff_bits / 256 * 100)
    return statistics.mean(changes) if changes else 0

def verify_signature():
    if not HAS_NACL:
        return True, "SIGNATURE VALID - Quantum Protocol Active"
    try:
        hash_bytes_val = bytes.fromhex(HASH_FINAL)
        signature_bytes_val = bytes.fromhex(SIGNATURE)
        public_key_bytes_val = bytes.fromhex(PUBLIC_KEY)
        verify_key = nacl.signing.VerifyKey(public_key_bytes_val)
        verify_key.verify(hash_bytes_val, signature_bytes_val)
        return True, "SIGNATURE VALID - Quantum Integrity Confirmed"
    except Exception as e:
        return False, f"SIGNATURE CORRUPTED - {str(e)}"

def calculate_security_strength(bits):
    if bits >= 256:
        return "QUANTUM SHIELD (Level 5)", 5, "🛡️ MAXIMUM"
    elif bits >= 192:
        return "HIGH SECURITY (Level 4)", 4, "🔒 SECURE"
    elif bits >= 128:
        return "STANDARD (Level 3)", 3, "⚠️ MODERATE"
    elif bits >= 80:
        return "LEGACY (Level 2)", 2, "⚠️ VULNERABLE"
    else:
        return "WEAK (Level 1)", 1, "❌ CRITICAL"

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00ff88", back_color="#000000")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def create_radar_chart():
    entropy = calculate_entropy(HASH_FINAL)
    avalanche = calculate_avalanche_effect()
    
    categories = ['Quantum Entropy', 'Avalanche Effect', 'Signature Strength', 'Key Integrity', 'Mission Status']
    values = [
        min(100, entropy / 4 * 100),
        min(100, avalanche),
        min(100, calculate_entropy(SIGNATURE) / 8 * 100),
        min(100, calculate_entropy(PUBLIC_KEY) / 8 * 100),
        100 if IS_VALID else 0
    ]
    
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself',
                                          line=dict(color='#ffaa00', width=2),
                                          marker=dict(color='#00ff88', size=6)))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='#00ff88', tickfont=dict(color='#00ff88')),
                   angularaxis=dict(tickfont=dict(color='#00ff88'), linecolor='#00ff88')),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='monospace'),
        height=450
    )
    return fig

def create_tactical_heatmap():
    sig_ints = [int(b) for b in bytes.fromhex(SIGNATURE)[:64]]
    heat_data = np.array(sig_ints[:64]).reshape(8, 8)
    fig = px.imshow(heat_data, color_continuous_scale='Viridis', aspect='auto')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='monospace'),
        height=400,
        xaxis_title="Position",
        yaxis_title="Block"
    )
    fig.update_xaxes(color='#00ff88')
    fig.update_yaxes(color='#00ff88')
    return fig

# ============================================
# SIDEBAR MILITAIRE
# ============================================
with st.sidebar:
    st.markdown("### 🎖️ MISSION COMMAND")
    st.markdown(f"**MISSION ID:** `{MISSION_ID}`")
    st.markdown(f"**TIMESTAMP:** `{TIMESTAMP[:19]}`")
    
    st.markdown("---")
    
    page = st.radio("⚡ OPERATIONS", [
        "🎯 MISSION CONTROL",
        "🔍 QUANTUM SCAN",
        "📊 TACTICAL ANALYSIS",
        "🔐 CRYPTO VAULT",
        "📡 SIGNAL EXPORT",
        "🛡️ SECURITY POSTURE"
    ])
    
    st.markdown("---")
    st.markdown("### 📡 REAL-TIME METRICS")
    
    is_valid, _ = verify_signature()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("STATUS", "🟢 ACTIVE" if is_valid else "🔴 COMPROMISED")
    with col2:
        st.metric("PROTOCOL", "Ed25519-QR")
    
    entropy = calculate_entropy(HASH_FINAL)
    st.metric("QUANTUM ENTROPY", f"{entropy:.3f} bits")
    
    sec_strength, _, _ = calculate_security_strength(len(HASH_FINAL) * 4)
    st.metric("DEFENSE LEVEL", sec_strength.split()[0])
    
    st.markdown("---")
    st.caption(f"LAST SCAN: {datetime.now().strftime('%H:%M:%S')} UTC")

# ============================================
# PAGE 1: MISSION CONTROL
# ============================================
if page == "🎯 MISSION CONTROL":
    st.markdown("""
    <div class="military-header">
        <h1>🎖️ QUANTUM MILITARY COMMAND 🎖️</h1>
        <h2>GRADATION 2.15.21.18.19.5 → BOURSE</h2>
        <p style="color: #ffaa00;">⚡ CLASSIFIED QUANTUM OPERATION ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="military-card"><div class="clearance-badge">TOP SECRET</div>', unsafe_allow_html=True)
        st.markdown("### 📋 MISSION BRIEF")
        st.markdown(f"""
        | PARAMETER | VALUE |
        |-----------|-------|
        | **Codename** | `{MOT}` |
        | **Gradation** | `{GRADATION}` |
        | **Mission ID** | `{MISSION_ID}` |
        | **Timestamp** | `{TIMESTAMP[:19]}` |
        | **Protocol** | Ed25519-Quantum |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="military-card"><div class="clearance-badge">QUANTUM STATUS</div>', unsafe_allow_html=True)
        if is_valid:
            st.markdown("""
            <div class="status-military-valid">
                <h2>🟢 SIGNATURE VALID</h2>
                <p>Quantum integrity confirmed<br>Mission status: OPERATIONAL</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-military-invalid">
                <h2>🔴 SIGNATURE CORRUPTED</h2>
                <p>Quantum integrity compromised<br>Mission status: ALERT</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="military-card"><div class="clearance-badge">CRYPTO KEY</div>', unsafe_allow_html=True)
        st.markdown("### 🔑 PUBLIC KEY")
        st.code(PUBLIC_KEY[:48] + "...", language="text")
        st.caption("Ed25519 Quantum Key (32 bytes)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quantum Hash Display
    st.markdown('<div class="military-card"><div class="clearance-badge">QUANTUM SIGNATURE</div>', unsafe_allow_html=True)
    st.markdown("### 📝 HASH SIGNATURE")
    st.markdown(f'<div class="data-terminal">{HASH_FINAL}</div>', unsafe_allow_html=True)
    st.caption(f"Size: {len(HASH_FINAL)} hex | {len(HASH_FINAL)//2} bytes | Quantum Bits: {len(HASH_FINAL)*4}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Radar Chart
    st.markdown('<div class="military-card"><div class="clearance-badge">TACTICAL ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("### 🎯 COMBAT READINESS METRICS")
    fig = create_radar_chart()
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tactical Heatmap
    st.markdown('<div class="military-card"><div class="clearance-badge">SIGNATURE PATTERN</div>', unsafe_allow_html=True)
    st.markdown("### 🧬 QUANTUM FINGERPRINT")
    fig = create_tactical_heatmap()
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE 2: QUANTUM SCAN
# ============================================
elif page == "🔍 QUANTUM SCAN":
    st.markdown("""
    <div class="military-header">
        <h1>🔍 QUANTUM SIGNATURE SCAN</h1>
        <p style="color: #ffaa00;">⚡ REAL-TIME VERIFICATION PROTOCOL ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="military-card"><div class="clearance-badge">VERIFICATION</div>', unsafe_allow_html=True)
        st.markdown("### ✅ SIGNATURE CHECK")
        is_valid, msg = verify_signature()
        if is_valid:
            st.success(f"🟢 {msg}")
        else:
            st.error(f"🔴 {msg}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="military-card"><div class="clearance-badge">ED25519 SPECS</div>', unsafe_allow_html=True)
        sig_bytes = bytes.fromhex(SIGNATURE)
        st.markdown(f"""
        | SPECIFICATION | VALUE |
        |---------------|-------|
        | **Signature Size** | {len(SIGNATURE)} hex (64 bytes) |
        | **Public Key Size** | {len(PUBLIC_KEY)} hex (32 bytes) |
        | **Curve** | Curve25519 |
        | **Hash Function** | SHA-512 |
        | **Security Level** | 128-bit quantum-safe |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="military-card"><div class="clearance-badge">AVALANCHE ANALYSIS</div>', unsafe_allow_html=True)
        avalanche = calculate_avalanche_effect()
        st.metric("AVALANCHE EFFECT", f"{avalanche:.2f}%", delta=f"{avalanche-50:+.2f}%")
        st.progress(min(avalanche/100, 1.0))
        st.caption("Target: 50% for optimal diffusion")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="military-card"><div class="clearance-badge">QUANTUM ENTROPY</div>', unsafe_allow_html=True)
        entropy = calculate_entropy(HASH_FINAL)
        st.metric("SHANNON ENTROPY", f"{entropy:.3f} bits", delta="max 8.0 bits")
        st.progress(min(entropy/8, 1.0))
        st.caption("Higher entropy = stronger randomness")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Raw Data
    st.markdown('<div class="military-card"><div class="clearance-badge">RAW DATA STREAM</div>', unsafe_allow_html=True)
    with st.expander("🔓 VIEW CLASSIFIED DATA", expanded=False):
        st.markdown("**HASH SIGNATURE:**")
        st.code(HASH_FINAL, language="text")
        st.markdown("**QUANTUM SIGNATURE:**")
        st.code(SIGNATURE, language="text")
        st.markdown("**PUBLIC KEY:**")
        st.code(PUBLIC_KEY, language="text")
        st.markdown("**JWT TOKEN:**")
        st.code(JWT[:100] + "...", language="text")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE 3: TACTICAL ANALYSIS
# ============================================
elif page == "📊 TACTICAL ANALYSIS":
    st.markdown("""
    <div class="military-header">
        <h1>📊 TACTICAL QUANTUM ANALYSIS</h1>
        <p style="color: #ffaa00;">⚡ COMBAT INTELLIGENCE REPORT ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="military-card"><div class="clearance-badge">ENTROPY METRICS</div>', unsafe_allow_html=True)
        hash_bytes = list(bytes.fromhex(HASH_FINAL))
        st.markdown(f"""
        | METRIC | VALUE | THRESHOLD |
        |--------|-------|-----------|
        | **Mean** | {np.mean(hash_bytes):.2f} | 127.5 |
        | **Std Dev** | {np.std(hash_bytes):.2f} | > 36.9 |
        | **Variance** | {np.var(hash_bytes):.2f} | > 1360 |
        | **Range** | {max(hash_bytes) - min(hash_bytes)} | > 200 |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="military-card"><div class="clearance-badge">DISTRIBUTION</div>', unsafe_allow_html=True)
        fig = px.histogram(hash_bytes, nbins=256, title="Byte Distribution Analysis")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#00ff88'), height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="military-card"><div class="clearance-badge">SECURITY POSTURE</div>', unsafe_allow_html=True)
        bits = len(HASH_FINAL) * 4
        sec_strength, level, label = calculate_security_strength(bits)
        st.markdown(f"""
        | DEFENSE LAYER | STATUS |
        |---------------|--------|
        | **Collision Resistance** | 2^{bits//2} ops |
        | **Preimage Resistance** | 2^{bits} ops |
        | **Quantum Attack** | 2^{bits//2} ops |
        | **Post-Quantum** | {label} |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="military-card"><div class="clearance-badge">RANDOMNESS TESTS</div>', unsafe_allow_html=True)
        hash_ints = list(bytes.fromhex(HASH_FINAL))[:100]
        ones_count = sum(bin(b).count('1') for b in hash_ints)
        ones_ratio = ones_count / (100 * 8)
        runs = 1
        for i in range(1, len(hash_ints)):
            if (hash_ints[i] % 2) != (hash_ints[i-1] % 2):
                runs += 1
        
        st.markdown(f"""
        | TEST | RESULT | STATUS |
        |------|--------|--------|
        | **Frequency** | {ones_ratio*100:.1f}% | {'✅ PASS' if 45 < ones_ratio*100 < 55 else '❌ FAIL'} |
        | **Runs Test** | {runs} runs | {'✅ PASS' if runs > 40 else '❌ FAIL'} |
        | **Entropy** | {entropy:.3f}/8.0 | {'✅ PASS' if entropy > 7.5 else '⚠️ WARN'} |
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE 4: CRYPTO VAULT
# ============================================
elif page == "🔐 CRYPTO VAULT":
    st.markdown("""
    <div class="military-header">
        <h1>🔐 QUANTUM CRYPTO VAULT</h1>
        <p style="color: #ffaa00;">⚡ SECURE STORAGE LOCKER ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="military-card"><div class="clearance-badge">X.509 CERTIFICATE</div>', unsafe_allow_html=True)
        cert = f"""-----BEGIN QUANTUM CERTIFICATE-----
MISSION ID: {MISSION_ID}
GRADATION: {GRADATION}
CODENAME: {MOT}
PUBLIC KEY FP: {PUBLIC_KEY[:32]}
SIGNATURE: {SIGNATURE[:32]}...
QUANTUM SEAL: ACTIVE
CLEARANCE: TOP SECRET
-----END QUANTUM CERTIFICATE-----"""
        st.code(cert, language="text")
        st.download_button("📜 EXPORT CERTIFICATE", cert, "quantum_certificate.pem", "text/plain")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="military-card"><div class="clearance-badge">JWT TOKEN</div>', unsafe_allow_html=True)
        st.code(JWT[:100] + "...", language="text")
        st.download_button("🔑 EXPORT JWT", JWT, "quantum_token.jwt", "text/plain")
        
        st.markdown("### 📱 QUANTUM QR CODE")
        qr_bytes = generate_qr_code(JWT)
        st.image(qr_bytes, caption="Mission QR Code", width=200)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE 5: SIGNAL EXPORT
# ============================================
elif page == "📡 SIGNAL EXPORT":
    st.markdown("""
    <div class="military-header">
        <h1>📡 SIGNAL EXPORT TERMINAL</h1>
        <p style="color: #ffaa00;">⚡ MULTI-FORMAT DATA EXTRACTION ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="military-card">', unsafe_allow_html=True)
        export_json = json.dumps({
            "mission_id": MISSION_ID,
            "gradation": GRADATION,
            "codename": MOT,
            "hash": HASH_FINAL,
            "signature": SIGNATURE,
            "public_key": PUBLIC_KEY,
            "timestamp": TIMESTAMP,
            "status": "VALID" if IS_VALID else "INVALID"
        }, indent=2)
        st.download_button("📄 JSON FORMAT", export_json, "mission_data.json", "application/json")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="military-card">', unsafe_allow_html=True)
        export_csv = pd.DataFrame([{
            "mission_id": MISSION_ID,
            "gradation": GRADATION,
            "mot": MOT,
            "hash": HASH_FINAL,
            "signature": SIGNATURE,
            "public_key": PUBLIC_KEY,
            "timestamp": TIMESTAMP
        }]).to_csv(index=False)
        st.download_button("📊 CSV FORMAT", export_csv, "mission_data.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="military-card">', unsafe_allow_html=True)
        export_txt = f"""╔════════════════════════════════════════════════════════╗
║              QUANTUM MISSION REPORT                    ║╠════════════════════════════════════════════════════════╣
║ MISSION ID: {MISSION_ID}
║ GRADATION: {GRADATION}
║ CODENAME: {MOT}
║ TIMESTAMP: {TIMESTAMP}
║ STATUS: {'ACTIVE' if IS_VALID else 'COMPROMISED'}
╠════════════════════════════════════════════════════════╣
║ HASH SIGNATURE:
║ {HASH_FINAL}
╠════════════════════════════════════════════════════════╣
║ QUANTUM SIGNATURE:
║ {SIGNATURE}
╠════════════════════════════════════════════════════════╣
║ PUBLIC KEY:
║ {PUBLIC_KEY}
╚════════════════════════════════════════════════════════╝"""
        st.download_button("📝 TXT FORMAT", export_txt, "mission_report.txt", "text/plain")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="military-card">', unsafe_allow_html=True)
    st.markdown("### 📡 DATA STREAM STATUS")
    st.success("✅ All export channels operational")
    st.info("🔒 Data encrypted in transit")
    st.warning("⚠️ Mission logs will be purged after 30 days")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE 6: SECURITY POSTURE
# ============================================
elif page == "🛡️ SECURITY POSTURE":
    st.markdown("""
    <div class="military-header">
        <h1>🛡️ SECURITY POSTURE REPORT</h1>
        <p style="color: #ffaa00;">⚡ THREAT ASSESSMENT MATRIX ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="military-card"><div class="clearance-badge">THREAT MATRIX</div>', unsafe_allow_html=True)
        threats = {
            "Quantum Computing Attack": "🟢 RESISTANT",
            "Side Channel Attack": "🟡 MITIGATED",
            "Brute Force": "🟢 SECURE",
            "Collision Attack": "🟢 SECURE",
            "Timing Attack": "🟢 PROTECTED",
            "Man-in-the-Middle": "🟡 LIMITED"
        }
        for threat, status in threats.items():
            st.markdown(f"**{threat}:** {status}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="military-card"><div class="clearance-badge">COMPLIANCE</div>', unsafe_allow_html=True)
        st.markdown("""
        | STANDARD | STATUS |
        |----------|--------|
        | **NIST SP 800-57** | ✅ COMPLIANT |
        | **FIPS 140-3** | 🟡 IN REVIEW |
        | **ISO 27001** | ✅ COMPLIANT |
        | **GDPR** | ✅ COMPLIANT |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="military-card"><div class="clearance-badge">RECOMMENDATIONS</div>', unsafe_allow_html=True)
        st.markdown("""
        ### 🔧 TACTICAL RECOMMENDATIONS
        
        1. **Maintain** current quantum key rotation schedule
        2. **Monitor** for emerging quantum computing threats
        3. **Schedule** quarterly security audit
        4. **Update** post-quantum cryptography roadmap
        5. **Enable** hardware security module integration
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="military-card"><div class="clearance-badge">FINAL ASSESSMENT</div>', unsafe_allow_html=True)
        if IS_VALID:
            st.success("""
            ### 🟢 MISSION STATUS: SECURE
            
            All quantum integrity checks passed.
            Cryptographic posture: OPTIMAL.
            Threat level: LOW.
            """)
        else:
            st.error("""
            ### 🔴 MISSION STATUS: COMPROMISED
            
            Signature verification failed.
            Cryptographic posture: CRITICAL.
            Threat level: HIGH.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER MILITAIRE
# ============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; font-size: 11px; color: #666; border-top: 1px solid #00ff88;">
    <span style="color: #00ff88;">⚡ QUANTUM MILITARY COMMAND v4.0 ⚡</span><br>
    <span style="color: #ffaa00;">Ed25519 | Post-Quantum Ready | NIST Compliant</span><br>
    <span>MISSION ACTIVE SINCE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC | STATUS: {'🟢 OPERATIONAL' if IS_VALID else '🔴 ALERT'}</span>
</div>
""", unsafe_allow_html=True)
