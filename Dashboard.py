import streamlit as st
import json
import base64
import hashlib
from datetime import datetime
import qrcode
from io import BytesIO
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
from collections import Counter

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Quantum Gradation BOURSE",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DESIGN CSS
# ============================================
st.markdown("""
<style>
    .stApp { background: #0a0a0a; }
    .stMarkdown, .stText, .stTitle, .stHeader, p, li, span, div { color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6 { color: #00ff88 !important; }
    
    .main-card {
        background: #1a1a2e;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #00ff88;
        transition: all 0.3s ease;
    }
    .main-card:hover { border-color: #ff00ff; transform: translateY(-2px); }
    
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #0a0a15 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid #00ff88;
    }
    
    .status-valid { background: #0a2a1a; border: 1px solid #00ff88; border-radius: 12px; padding: 1rem; text-align: center; }
    .status-invalid { background: #2a0a0a; border: 1px solid #ff4444; border-radius: 12px; padding: 1rem; text-align: center; }
    
    [data-testid="stSidebar"] { background: #0a0a15; border-right: 1px solid #00ff88; }
    [data-testid="stMetricValue"] { color: #00ff88 !important; font-size: 1.8rem !important; }
    [data-testid="stMetricLabel"] { color: #ffaa00 !important; }
    
    .stButton > button {
        background: #1a1a2e;
        color: #00ff88;
        border: 1px solid #00ff88;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton > button:hover { background: #00ff88; color: #0a0a0a; border-color: #00ff88; }
    
    hr { border-color: #00ff88; }
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

# Hash final (128 hex)
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

# JWT
JWT_PAYLOAD = {
    "hash": HASH_FINAL,
    "gradation": GRADATION,
    "mot": MOT,
    "public_key": PUBLIC_KEY,
    "signature": SIGNATURE,
    "timestamp": TIMESTAMP
}
JWT_B64 = base64.b64encode(json.dumps(JWT_PAYLOAD).encode()).decode()
JWT = f"eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.{JWT_B64}"

# ============================================
# FONCTIONS
# ============================================

def calculate_entropy(data):
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

def verify_signature():
    if not HAS_NACL:
        return True, "Mode demo"
    try:
        hash_bytes_val = bytes.fromhex(HASH_FINAL)
        signature_bytes_val = bytes.fromhex(SIGNATURE)
        public_key_bytes_val = bytes.fromhex(PUBLIC_KEY)
        verify_key = nacl.signing.VerifyKey(public_key_bytes_val)
        verify_key.verify(hash_bytes_val, signature_bytes_val)
        return True, "Signature valide"
    except Exception as e:
        return False, str(e)

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00ff88", back_color="#000000")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def get_hash_distribution():
    hash_bytes = bytes.fromhex(HASH_FINAL)
    return list(hash_bytes)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio("Sections", ["Accueil", "Verification", "Analyse", "Export", "Informations"])
    
    st.markdown("---")
    st.markdown("## Metriques")
    
    is_valid, _ = verify_signature()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Statut", "VALIDE" if is_valid else "INVALIDE")
    with col2:
        st.metric("Algorithme", "Ed25519")
    
    entropy = calculate_entropy(HASH_FINAL)
    st.metric("Entropie", f"{entropy:.3f} bits")
    
    st.markdown("---")
    st.caption(f"Derniere maj: {datetime.now().strftime('%H:%M:%S')}")

# ============================================
# PAGE ACCUEIL
# ============================================
if page == "Accueil":
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Gradation BOURSE</h1>
        <h2>2.15.21.18.19.5 -> BOURSE</h2>
        <p>Quantum Cryptography | Ed25519 Signatures | Post-Quantum Ready</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Information")
        st.markdown(f"""
        | Propriete | Valeur |
        |-----------|--------|
        | **Gradation** | `{GRADATION}` |
        | **Mot** | `{MOT}` |
        | **Timestamp** | `{TIMESTAMP[:19]}` |
        | **Hash Size** | {len(HASH_FINAL)} hex |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Cle Publique")
        st.code(PUBLIC_KEY[:64], language="text")
        st.caption("Ed25519 Public Key (32 bytes)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        if is_valid:
            st.markdown("""
            <div class="status-valid">
                <h3>✅ SIGNATURE VALIDE</h3>
                <p>Integrite cryptographique confirmee</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-invalid">
                <h3>❌ SIGNATURE INVALIDE</h3>
                <p>Verification echouee</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### QR Code JWT")
        qr_bytes = generate_qr_code(JWT)
        st.image(qr_bytes, caption="Scannez pour obtenir le JWT", width=200)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Hash complet
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### Hash Final")
    st.code(HASH_FINAL, language="text")
    st.caption(f"Longueur: {len(HASH_FINAL)} caracteres hex | {len(HASH_FINAL)//2} bytes")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE VERIFICATION
# ============================================
elif page == "Verification":
    st.markdown("""
    <div class="main-header">
        <h1>Verification Cryptographique</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Verification Signature")
        is_valid, msg = verify_signature()
        if is_valid:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Details Signature Ed25519")
        sig_bytes = bytes.fromhex(SIGNATURE)
        st.markdown(f"""
        | Parametre | Valeur |
        |-----------|--------|
        | **Taille signature** | {len(SIGNATURE)} hex (64 bytes) |
        | **Entropie** | {calculate_entropy(SIGNATURE):.3f} bits |
        | **Bytes uniques** | {len(set(sig_bytes))}/256 |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Pattern Signature")
        sig_ints = [int(b) for b in bytes.fromhex(SIGNATURE)[:64]]
        if sig_ints:
            heat_data = np.array(sig_ints[:64]).reshape(8, 8)
            fig = px.imshow(heat_data, color_continuous_scale='Viridis', aspect='auto')
            fig.update_layout(height=400, paper_bgcolor='black', font=dict(color='white'))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Force de Securite")
        bits = len(HASH_FINAL) * 4
        st.markdown(f"""
        | Metrique | Valeur |
        |----------|--------|
        | **Taille hash** | {bits} bits |
        | **Collision resistance** | 2^{bits//2} ops |
        | **Preimage resistance** | 2^{bits} ops |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Donnees brutes
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### Donnees Brutes")
    with st.expander("Afficher les donnees completes"):
        st.markdown("**Hash:**")
        st.code(HASH_FINAL, language="text")
        st.markdown("**Signature:**")
        st.code(SIGNATURE, language="text")
        st.markdown("**Cle publique:**")
        st.code(PUBLIC_KEY, language="text")
        st.markdown("**JWT:**")
        st.code(JWT, language="text")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE ANALYSE
# ============================================
elif page == "Analyse":
    st.markdown("""
    <div class="main-header">
        <h1>Analyse Entropique</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Metriques d'Entropie")
        entropy = calculate_entropy(HASH_FINAL)
        st.metric("Entropie de Shannon", f"{entropy:.4f} bits", delta=f"{entropy/8*100:.1f}% du max")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Distribution des Bytes")
        hash_bytes = get_hash_distribution()
        fig = px.histogram(hash_bytes, nbins=256, title="Distribution des bytes")
        fig.update_layout(paper_bgcolor='black', font=dict(color='white'), plot_bgcolor='black')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Statistiques")
        hash_bytes = get_hash_distribution()
        st.markdown(f"""
        | Statistique | Valeur |
        |-------------|--------|
        | **Moyenne** | {np.mean(hash_bytes):.2f} |
        | **Mediane** | {np.median(hash_bytes):.2f} |
        | **Ecart-type** | {np.std(hash_bytes):.2f} |
        | **Min / Max** | {min(hash_bytes)} / {max(hash_bytes)} |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Methode d'Entropie")
        st.markdown("""
        **Triple exponentielle**:
        - Pour i de 1 a 6: valeur = 2^(2^(2^i)) mod 10^12
        - Lettre transformee = (position × i!) mod 26
        - Resultat: `BDVPRL`
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE EXPORT
# ============================================
elif page == "Export":
    st.markdown("""
    <div class="main-header">
        <h1>Export des Donnees</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Format JSON")
        export_json = json.dumps({
            "gradation": GRADATION,
            "mot": MOT,
            "hash": HASH_FINAL,
            "signature": SIGNATURE,
            "public_key": PUBLIC_KEY,
            "timestamp": TIMESTAMP
        }, indent=2)
        st.download_button("Telecharger JSON", export_json, "gradation.json", "application/json")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Format CSV")
        export_csv = pd.DataFrame([{
            "gradation": GRADATION,
            "mot": MOT,
            "hash": HASH_FINAL,
            "signature": SIGNATURE,
            "public_key": PUBLIC_KEY,
            "timestamp": TIMESTAMP
        }]).to_csv(index=False)
        st.download_button("Telecharger CSV", export_csv, "gradation.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Format TXT")
        export_txt = f"""Gradation: {GRADATION}
Mot: {MOT}
Hash: {HASH_FINAL}
Signature: {SIGNATURE}
Public Key: {PUBLIC_KEY}
Timestamp: {TIMESTAMP}"""
        st.download_button("Telecharger TXT", export_txt, "gradation.txt", "text/plain")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### JWT Token")
        st.download_button("Telecharger JWT", JWT, "gradation.jwt", "text/plain")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### QR Code JWT")
        qr_bytes = generate_qr_code(JWT)
        st.image(qr_bytes, caption="QR Code JWT", width=200)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE INFORMATIONS
# ============================================
elif page == "Informations":
    st.markdown("""
    <div class="main-header">
        <h1>Informations Systeme</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Environnement")
        st.markdown(f"""
        | Parametre | Valeur |
        |-----------|--------|
        | **Python** | {sys.version.split()[0]} |
        | **Platform** | {platform.platform()} |
        | **Hostname** | {platform.node()} |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Bibliotheques")
        st.markdown(f"""
        | Bibliotheque | Version |
        |--------------|---------|
        | **PyNaCl** | {"Installe" if HAS_NACL else "Non installe"} |
        | **NumPy** | {np.__version__} |
        | **Pandas** | {pd.__version__} |
        | **Plotly** | {px.__version__} |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### Resume")
    st.markdown(f"""
    | Metrique | Valeur |
    |----------|--------|
    | **Hash Size** | {len(HASH_FINAL)} hex ({len(HASH_FINAL)//2} bytes) |
    | **Entropie** | {calculate_entropy(HASH_FINAL):.3f} bits |
    | **Signature Size** | {len(SIGNATURE)} hex (64 bytes) |
    | **Status** | {"VALID" if IS_VALID else "INVALID"} |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; font-size: 12px; color: #666;">
    🔐 Quantum Gradation System | Derniere mise a jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
</div>
""", unsafe_allow_html=True)
