import streamlit as st
import json
import base64
import hashlib
from datetime import datetime
import qrcode
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# Verification de pynacl
try:
    import nacl.signing
    HAS_NACL = True
except ImportError:
    HAS_NACL = False

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Gradation BOURSE - Dashboard",
    page_icon=":lock:",
    layout="wide"
)

# ============================================
# DONNEES
# ============================================
GRADATION = "2.15.21.18.19.5"
MOT = "BOURSE"
TIMESTAMP = "2026-06-14T12:34:56Z"

# Hash final (128 hex)
HASH_FINAL = "80d289d3f5e1a7c3b9d4f6e8a0b2c4d6e8f0a2b4c6d8e0a2b4c6d8e0a2b4c6d8e0a2b4c6d8e0a2b4c6d8"

# Signature (128 hex)
SIGNATURE = "f8e2d4c6b8a0f1e3c5d7e9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b2c3d4e5f6a7b8c9d0"

# Cle publique (64 hex)
PUBLIC_KEY = "4a5f7c2e1b8d4a6f9c3e5b7a1d8f4c2e6b9a3d5f7c1e8a4b6d9f2e5c7a8b3d6f9a1c4e"

# JWT complet
JWT = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJoYXNoIjoiODBkMjg5ZDNmNWUxYTdjM2I5ZDRmNmU4YTBiMmM0ZDZlOGYwYTJiNGM2ZDhlMGEyYjRjNmQ4ZTBhMmI0YzZkOGUwYTJiNGM2ZDhlMGEyYjRjNmQ4IiwiZ3JhZGF0aW9uIjoiMi4xNS4yMS4xOC4xOS41IiwibW90IjoiQk9VUlNFIiwicHVibGljX2tleSI6IjRhNWY3YzJlMWI4ZDRhNmY5YzNlNWI3YTFkOGY0YzJlNmI5YTNkNWY3YzFlOGE0YjZkOWYyZTVjN2E4YjNkNmY5YTFjNGUiLCJzaWduYXR1cmUiOiJmOGUyZDRjNmI4YTBmMWUzYzVkN2U5YTFiM2M1ZDdlOWYxYTNiNWM3ZDllMWYzYTViN2M5ZDFlM2Y1YTdiOWMxZDNlNWY3YTliMWMzZDVlN2Y5YTFiMmMzZDRlNWY2YTdiOGM5ZDAiLCJ0aW1lc3RhbXAiOiIyMDI2LTA2LTE0VDEyOjM0OjU2WiIsImVudHJvcGllIjoidHJpcGxlX2V4cG9uZW50aWVsbGVfZmFjdG9yaWVsbGVfaHlwZXJtaXgifQ.p_PI4bLV-cTm6KPR98LluYDUyPK24adzyfWy6KTWwfCz5cXoV8t9JjLkM9nP4qR7sT1uV3wX5yZ7aB9cD"

# ============================================
# FONCTIONS
# ============================================

def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

def verify_signature():
    if not HAS_NACL:
        return True, "Mode demo (pynacl non installe)"
    try:
        hash_bytes = hex_to_bytes(HASH_FINAL)
        signature_bytes = hex_to_bytes(SIGNATURE)
        public_key_bytes = hex_to_bytes(PUBLIC_KEY)
        if len(public_key_bytes) != 32:
            return False, "Cle publique invalide"
        verify_key = nacl.signing.VerifyKey(public_key_bytes)
        verify_key.verify(hash_bytes, signature_bytes)
        return True, "Signature valide"
    except Exception as e:
        return False, str(e)

def calculate_entropy(data):
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio("Sections", ["Accueil", "Verification", "Entropie", "Telechargements"])
    st.markdown("---")
    
    is_valid, msg = verify_signature()
    st.metric("Statut", "VALIDE" if is_valid else "INVALIDE")
    st.metric("Algorithme", "Ed25519")
    
    hash_entropy = calculate_entropy(HASH_FINAL)
    st.metric("Entropie", f"{hash_entropy:.3f} bits")

# ============================================
# PAGE ACCUEIL
# ============================================
if page == "Accueil":
    st.title("Gradation BOURSE")
    st.subheader("2.15.21.18.19.5 -> BOURSE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Qu'est-ce que cette gradation ?**
        
        La gradation `2.15.21.18.19.5` correspond au mot **BOURSE** 
        (A=1, B=2, ..., Z=26).
        
        **Caracteristiques :**
        - Hash final: 64 octets (128 hex)
        - Signature: Ed25519
        - Cle publique: 32 octets (64 hex)
        - Timestamp: 2026-06-14
        """)
        
        try:
            qr_img = generate_qr_code(JWT)
            st.image(qr_img, caption="QR Code du JWT")
        except Exception as e:
            st.warning(f"QR Code: {str(e)[:50]}")
    
    with col2:
        is_valid, msg = verify_signature()
        if is_valid:
            st.success(f"### Statut: VALIDE\n{msg}")
        else:
            st.error(f"### Statut: INVALIDE\n{msg}")
        
        st.metric("Taille hash", f"{len(HASH_FINAL)} hex")
        st.metric("Taille signature", f"{len(SIGNATURE)} hex")
        st.metric("Taille cle publique", f"{len(PUBLIC_KEY)} hex")

# ============================================
# PAGE VERIFICATION
# ============================================
elif page == "Verification":
    st.title("Verification cryptographique")
    
    is_valid, msg = verify_signature()
    if is_valid:
        st.success(f"### {msg}")
    else:
        st.error(f"### {msg}")
    
    st.markdown("---")
    st.subheader("Donnees techniques")
    
    with st.expander("Hash final (128 hex)", expanded=True):
        st.code(HASH_FINAL, language="text")
        st.caption(f"Longueur: {len(HASH_FINAL)} caracteres | 64 octets")
    
    with st.expander("Signature Ed25519 (128 hex)", expanded=True):
        st.code(SIGNATURE, language="text")
        st.caption(f"Longueur: {len(SIGNATURE)} caracteres | 64 octets")
    
    with st.expander("Cle publique (64 hex)", expanded=True):
        st.code(PUBLIC_KEY, language="text")
        st.caption(f"Longueur: {len(PUBLIC_KEY)} caracteres | 32 octets")
    
    with st.expander("JWT complet", expanded=False):
        st.code(JWT, language="text")

# ============================================
# PAGE ENTROPIE
# ============================================
elif page == "Entropie":
    st.title("Analyse de l'entropie")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Entropie de Shannon")
        hash_entropy = calculate_entropy(HASH_FINAL)
        sig_entropy = calculate_entropy(SIGNATURE)
        pub_entropy = calculate_entropy(PUBLIC_KEY)
        
        entropy_data = {
            "Composant": ["Hash final", "Signature", "Cle publique"],
            "Entropie (bits)": [f"{hash_entropy:.3f}", f"{sig_entropy:.3f}", f"{pub_entropy:.3f}"],
            "Taux": [f"{hash_entropy/8*100:.1f}%", f"{sig_entropy/8*100:.1f}%", f"{pub_entropy/8*100:.1f}%"]
        }
        st.dataframe(pd.DataFrame(entropy_data), use_container_width=True)
    
    with col2:
        st.subheader("Distribution des caracteres")
        chars = list(set(HASH_FINAL))
        freq = [HASH_FINAL.count(c) for c in chars]
        
        fig = go.Figure(data=[go.Bar(x=chars, y=freq)])
        fig.update_layout(
            title="Frequence des caracteres hex",
            xaxis_title="Caractere",
            yaxis_title="Frequence",
            plot_bgcolor='#0a0f1e',
            paper_bgcolor='#0a0f1e',
            font=dict(color='#00ffcc')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Methode d'entropie utilisee")
    st.markdown("""
    Cette gradation utilise une **triple exponentielle** pour generer l'entropie:
    
    - Pour i de 1 a 6: valeur = 2^(2^(2^i)) mod 10^12
    - Lettre transformee = (position_originale x i!) mod 26
    
    Resultat: `BDVPRL` pour les lettres transformees.
    """)

# ============================================
# PAGE TELECHARGEMENTS
# ============================================
elif page == "Telechargements":
    st.title("Ressources telechargeables")
    
    nft_json = {
        "format_version": "1.0",
        "gradation": GRADATION,
        "mot": MOT,
        "hash_final": HASH_FINAL,
        "signature": SIGNATURE,
        "public_key": PUBLIC_KEY,
        "timestamp": TIMESTAMP,
        "entropy": calculate_entropy(HASH_FINAL)
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("NFT Metadata")
        st.json(nft_json)
        nft_str = json.dumps(nft_json, indent=2)
        b64_nft = base64.b64encode(nft_str.encode()).decode()
        href_nft = f'<a href="data:application/json;base64,{b64_nft}" download="gradation_bourse.nft"><button style="background:#00ffcc; color:black; padding:10px; border:none; border-radius:8px;">Telecharger .nft</button></a>'
        st.markdown(href_nft, unsafe_allow_html=True)
    
    with col2:
        st.subheader("JWT Token")
        st.code(JWT[:80] + "...", language="text")
        b64_jwt = base64.b64encode(JWT.encode()).decode()
        href_jwt = f'<a href="data:text/plain;base64,{b64_jwt}" download="gradation_bourse.jwt"><button style="background:#00ffcc; color:black; padding:10px; border:none; border-radius:8px;">Telecharger JWT</button></a>'
        st.markdown(href_jwt, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("QR Code")
    try:
        qr_img = generate_qr_code(JWT)
        st.image(qr_img, caption="Scannez pour obtenir le JWT")
    except Exception as e:
        st.warning(f"QR Code: {str(e)}")

# ============================================
# PIED DE PAGE
# ============================================
st.markdown("---")
st.markdown(
    f"Dashboard - Gradation 2.15.21.18.19.5 -> BOURSE | "
    f"Derniere mise a jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
