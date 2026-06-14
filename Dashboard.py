
Resultat : `BDVPRL` pour les lettres transformees.
""")

# Page Telechargements
elif page == "Telechargements":
st.markdown("## Ressources telechargeables")

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
    st.markdown("### NFT Metadata")
    st.json(nft_json)
    nft_str = json.dumps(nft_json, indent=2)
    b64_nft = base64.b64encode(nft_str.encode()).decode()
    download_link = f'<a href="data:application/json;base64,{b64_nft}" download="gradation_bourse.nft"><button style="width:100%; background:#00ffcc; color:black; padding:10px; border:none; border-radius:8px;">Telecharger .nft</button></a>'
    st.markdown(download_link, unsafe_allow_html=True)

with col2:
    st.markdown("### JWT Token")
    st.code(JWT[:80] + "...", language="text")
    b64_jwt = base64.b64encode(JWT.encode()).decode()
    download_link2 = f'<a href="data:text/plain;base64,{b64_jwt}" download="gradation_bourse.jwt"><button style="width:100%; background:#00ffcc; color:black; padding:10px; border:none; border-radius:8px;">Telecharger JWT</button></a>'
    st.markdown(download_link2, unsafe_allow_html=True)

st.markdown("### QR Code")
try:
    qr_img = generate_qr_code(JWT)
    st.image(qr_img, caption="Scannez pour obtenir le JWT", use_container_width=False)
except Exception as e:
    st.info(f"QR code: {str(e)}")

# Pied de page
st.markdown("---")
st.markdown(
f"""
<div style="text-align: center; color: #666; font-size: 12px;">
    Dashboard - Gradation 2.15.21.18.19.5 -> BOURSE<br>
    Derniere mise a jour : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""",
unsafe_allow_html=True
)
