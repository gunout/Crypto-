""")
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE VAULT
# ============================================
elif page == "Vault":
st.markdown('<div class="futuristic-header"><h1 class="hologram-text">HOLOGRAM QUANTUM VAULT</h1></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="neural-card">', unsafe_allow_html=True)
    st.markdown("### NFT Quantum")
    nft_data = {
        "gradation": GRADATION,
        "mot": MOT,
        "hash": HASH_FINAL[:32] + "...",
        "timestamp": TIMESTAMP
    }
    st.json(nft_data)
    
    nft_str = json.dumps(nft_data, indent=2)
    b64_nft = base64.b64encode(nft_str.encode()).decode()
    st.markdown(f'<a href="data:application/json;base64,{b64_nft}" download="quantum_gradation.nft"><button style="background:#00ffcc; color:black; padding:10px; border-radius:10px;">Download NFT</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="neural-card">', unsafe_allow_html=True)
    st.markdown("### Quantum Certificate")
    cert = f"""-----BEGIN QUANTUM CERT-----
Gradation: {GRADATION}
Fingerprint: {hashlib.sha256(HASH_FINAL.encode()).hexdigest()[:32]}
Public Key: {PUBLIC_KEY[:32]}...
-----END QUANTUM CERT-----"""
    st.code(cert[:150] + "...", language="text")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="neural-card">', unsafe_allow_html=True)
    st.markdown("### Neural QR")
    qr_bytes = generate_qr_code(PUBLIC_KEY)
    st.image(qr_bytes, caption="Quantum Public Key", width=200)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="neural-card">', unsafe_allow_html=True)
st.markdown("### Download Portal")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.download_button("JWT Token", JWT, "quantum_token.jwt")
with col_b:
    st.download_button("Signature", SIGNATURE, "quantum_signature.sig")
with col_c:
    st.download_button("Hash", HASH_FINAL, "quantum_hash.hash")
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE FUTURE
# ============================================
elif page == "Future":
st.markdown('<div class="futuristic-header"><h1 class="hologram-text">FUTURECAST PREDICTIONS</h1></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="neural-card">', unsafe_allow_html=True)
    st.markdown("### Quantum Timeline")
    timeline_df = generate_quantum_timeline()
    st.dataframe(timeline_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="neural-card">', unsafe_allow_html=True)
    st.markdown("### Post-Quantum Predictions")
    
    years = list(range(2026, 2126, 20))
    security = [0.9999, 0.999, 0.99, 0.97, 0.95]
    
    fig = go.Figure(data=[go.Scatter(x=years[:5], y=security, mode='lines+markers', line=dict(color='cyan'))])
    fig.update_layout(
        title="Security vs Time",
        yaxis_tickformat=".0%",
        paper_bgcolor='rgba(0,0,0,0)',
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="neural-card">', unsafe_allow_html=True)
    st.markdown("### Neural Predictions")
    
    predictions = [
        "2030: Quantum resistance confirmed",
        "2050: Neural verification standard",
        "2080: Post-quantum transition",
        "2126: Gradation still valid"
    ]
    for pred in predictions:
        st.markdown(f"- {pred}")
    
    st.markdown("---")
    st.markdown("### Risk Assessment")
    risks = {"Current": 0.001, "10 years": 0.01, "50 years": 0.15, "100 years": 0.50}
    for period, risk in risks.items():
        st.progress(risk, text=f"{period}: {risk*100:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="neural-card">', unsafe_allow_html=True)
st.markdown("### Final Report")
st.markdown("""""")
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; font-size: 11px; color: #666;">
<span class="quantum-badge">QUANTUM GRADATION SYSTEM</span><br>
Last Quantum Pulse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
</div>
""", unsafe_allow_html=True)
