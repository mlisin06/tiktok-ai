import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="TikTok Auto Content Generator", page_icon="📱", layout="centered")

st.title("📱 TikTok Smart Content Generator")
st.write("Upload foto, masukkan topik, dan biarkan AI meracik konten TikTok yang menarik!")

api_key = st.text_input("Masukkan Gemini API Key Anda:", type="password")
topic = st.text_input("Topik atau Ide Video:", placeholder="Contoh: Tips outfit santai weekend")

uploaded_files = st.file_uploader(
    "Upload beberapa foto pendukung (Format: JPG, PNG):", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.write("### Preview Foto Anda:")
    cols = st.columns(len(uploaded_files) if len(uploaded_files) <= 4 else 4)
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        with cols[i % 4]:
            st.image(img, caption=f"Foto {i+1}", use_column_width=True)

if st.button("🚀 Buat Konten TikTok Sekarang", type="primary"):
    if not api_key:
        st.error("Mohon masukkan Gemini API Key Anda terlebih dahulu!")
    elif not topic:
        st.warning("Mohon masukkan topik video terlebih dahulu!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            contents = [
                f"Bertindaklah sebagai Content Creator TikTok profesional. Berdasarkan topik '{topic}' dan foto-foto yang diunggah, buatkan draf konten TikTok yang menarik, interaktif, dan aman dari pelanggaran:"
            ]
            
            if uploaded_files:
                for file in uploaded_files:
                    image_part = Image.open(file)
                    contents.append(image_part)
                contents.append("Analisis foto-foto di atas dan sesuaikan skrip serta hook-nya agar nyambung dengan visual tersebut.")
            
            contents.append("""
            Berikan dalam format berikut:
            1. **Hook (3 detik pertama):** Kalimat pembuka/teks layar yang memancing rasa penasaran.
            2. **Skrip/Alur Slide Foto:** Panduan teks atau narasi per slide foto untuk durasi 30-40 detik.
            3. **Saran Audio/Musik:** Jenis musik yang cocok (upbeat, chill, lofi).
            4. **Caption TikTok:** Caption interaktif memancing komentar + emoji.
            5. **Hashtag:** Kumpulan hashtag FYP yang relevan.
            """)
            
            with st.spinner("🤖 Gemini sedang menganalisis foto dan meracik konten..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents,
                )
                
            st.success("🎉 Konten TikTok Berhasil Dibuat!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
