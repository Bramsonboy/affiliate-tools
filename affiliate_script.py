import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Affiliate Script Generator", page_icon="🛍️")
st.title("🛍️ Affiliate Script Generator")
st.caption("1 klik → 1 script siap pakai (Shopee style) 🔥")

# --- INPUT ---
nama_produk = st.text_input("Nama Produk")
keunggulan = st.text_area("Keunggulan Produk")
target = st.text_input("Target Pembeli")

masalah = st.text_input("Masalah yang Dirasakan Target", placeholder="contoh: mata cepat lelah baca di HP")
situasi = st.text_input("Situasi / Konteks", placeholder="contoh: baca sebelum tidur atau di perjalanan")

gaya = st.selectbox("Gaya Konten", ["Santai & Relatable", "Excited & Hype", "Serius & Edukatif"])

platform = st.selectbox("Platform Konten", [
    "Shopee Video 10-15 detik",
    "Shopee Video 30 detik",
    "TikTok Video 10-15 detik"
])

# --- GENERATE ---
if st.button("⚡ Generate Script", type="primary"):

    # ✅ VALIDASI
    if not nama_produk or not keunggulan or not masalah:
        st.warning("Isi minimal: produk, keunggulan, dan masalah")
    else:
        with st.spinner("Lagi mikirin script yang jualan..."):

            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=st.secrets["OPENROUTER_API_KEY"]
            )

            # 🔥 PROMPT FINAL (ANTI KAKU + SHOPEE STYLE)
            prompt = f"""
Kamu adalah orang biasa yang lagi sharing pengalaman pakai produk ke teman, bukan sales.

Tugas:
Buat 1 script video pendek gaya Shopee yang natural banget, kayak ngomong langsung.

Cara nulis:
- mulai dari masalah yang relatable
- masuk ke solusi (produk)
- tutup dengan CTA halus

Gaya:
- santai
- sedikit tidak baku tidak apa-apa
- kayak ngobrol
- jangan terlalu rapi (biar natural)

Aturan WAJIB:
- maksimal 2 kalimat untuk SCRIPT
- jangan pakai kata marketing seperti:
  "terbaik", "dijamin", "wajib punya", "ubah hidup"
- jangan terdengar seperti iklan
- jangan tambahkan catatan, tips, atau penjelasan lain
- gunakan gaya orang Indonesia sehari-hari

HOOK harus langsung ke masalah, tanpa pembukaan panjang.

Gunakan kalimat pendek, seperti orang ngomong langsung.
Hindari storytelling panjang seperti "gue pernah..." di awal.

CTA jangan menggunakan kata:
"dijamin", "wajib", "harus", atau kata marketing lainnya.
---

DATA:
Produk: {nama_produk}
Keunggulan: {keunggulan}
Target: {target}
Masalah: {masalah}
Situasi: {situasi}
Gaya: {gaya}
Platform: {platform}

---

Output:

ANGLE:
(1 kalimat, fokus ke masalah user)

HOOK:
(kalimat pembuka yang relatable banget)

SCRIPT:
(maksimal 2 kalimat, problem → solusi, natural banget)

CTA:
(halus, kayak rekomendasi teman)
"""

            response = client.chat.completions.create(
                model="anthropic/claude-3.5-haiku",  # 🔥 model terbaik buat lo sekarang
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85
            )

            hasil = response.choices[0].message.content

            st.success("Siap dipakai! 🔥")
            st.markdown("---")
            st.subheader("🎬 Script Final:")
            st.write(hasil)