import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="44AI Veri Analizi", layout="wide")
st.title("📊 CSV Veri Analiz Portalı")
st.markdown("### 👑 4️⃣4️⃣AI 👑 ")

uploaded_file = st.file_uploader("Lütfen bir CSV dosyası yükleyin", type=["csv"])

if uploaded_file is not None:
    uploaded_file.seek(0)
    # 1. Ham Veriyi Oku (İstatistikler için sayısal kalmalı)
    df_raw = pd.read_csv(uploaded_file, low_memory=False)
    
    # Sütun İsimlerini Türkçeleştir (Hem ham hem işlenmiş veri için)
    sozluk = {
        "Star_Rating": "Yıldız Puanı", "Word_Count": "Kelime Sayısı",
        "Review_Length_Chars": "İnceleme Karakter Uzunluğu", "Thumbs_Up_Count": "Beğeni Sayısı",
        "Sentiment_Polarity": "Duygu Puanı", "App": "Uygulama Adı",
        "Review_Date": "İnceleme Tarihi", "Review_Text": "İnceleme Metni"
    }
    df_raw = df_raw.rename(columns=sozluk)

    # 2. İstatistikler Bölümü (Ham veri üzerinden)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ℹ️ Veri Bilgisi")
        st.write(df_raw.dtypes.astype(str))
        
    with col2:
        st.subheader("🔢 Temel İstatistikler")
        # Sadece sayısal sütunların istatistiğini al
        st.write(df_raw.describe())

    st.divider()

    # 3. Görselleştirme İçin Veriyi Hazırla (Arrow hatasını önlemek için)
    df_display = df_raw.copy()
    df_display = df_display.fillna("Veri Yok")

    st.subheader("📋 Veri Önizleme (İlk 5 Satır)")
    st.dataframe(df_display.head())

   # 4. Grafik Tasarım
st.subheader("📈 Profesyonel Veri Görselleştirme")

if 'df_display' in locals() or 'df_raw' in locals():
    columns = df_display.columns.tolist()
    
    # Veri tiplerini ayır (Ticari kalite için kritik)
    numeric_cols = df_display.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df_display.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df_display.select_dtypes(include=['datetime', 'object']).columns.tolist() # Object içindeki tarihler için

    col_control, col_plot = st.columns([1, 2])

    with col_control:
        graph_type = st.selectbox("Grafik Türü Seçin:", 
                                  ["Sütun (Kategori Dağılımı)", 
                                   "Zaman Serisi (Çizgi)", 
                                   "Korelasyon (Noktalı)", 
                                   "Kutu Grafiği (Dağılım)"])

        if graph_type == "Sütun (Kategori Dağılımı)":
            x_axis = st.selectbox("Kategori Sütunu (X):", categorical_cols + numeric_cols)
            st.info("Bu grafik, seçtiğiniz sütundaki verilerin miktarını sayar.")
            
        elif graph_type == "Zaman Serisi (Çizgi)":
            x_axis = st.selectbox("Tarih Sütunu (X):", columns)
            y_axis = st.selectbox("Sayısal Değer (Y):", numeric_cols)
            
        elif graph_type == "Korelasyon (Noktalı)":
            x_axis = st.selectbox("X Ekseni (Sayısal):", numeric_cols)
            y_axis = st.selectbox("Y Ekseni (Sayısal):", numeric_cols)
            
        elif graph_type == "Kutu Grafiği (Dağılım)":
            x_axis = st.selectbox("Grup Sütunu (X):", categorical_cols)
            y_axis = st.selectbox("Sayısal Değer (Y):", numeric_cols)

    with col_plot:
        # Örneklem (Performans için)
        df_plot = df_raw.sample(min(3000, len(df_raw))).copy()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        try:
            sns.set_style("whitegrid") # Daha profesyonel görünüm
            
            if graph_type == "Sütun (Kategori Dağılımı)":
                counts = df_plot[x_axis].value_counts().head(15) # En çok tekrar eden 15'i göster
                sns.barplot(x=counts.index.astype(str), y=counts.values, ax=ax, palette="viridis")
                plt.xticks(rotation=45)
                ax.set_title(f"{x_axis} Dağılımı")

            elif graph_type == "Zaman Serisi (Çizgi)":
                df_plot[x_axis] = pd.to_datetime(df_plot[x_axis], errors='coerce')
                df_plot = df_plot.dropna(subset=[x_axis])
                df_resampled = df_plot.groupby(x_axis)[y_axis].mean().sort_index().reset_index()
                sns.lineplot(data=df_resampled, x=x_axis, y=y_axis, ax=ax, marker='o')
                ax.set_title(f"Zaman İçinde {y_axis} Değişimi")

            elif graph_type == "Korelasyon (Noktalı)":
                sns.scatterplot(data=df_plot, x=x_axis, y=y_axis, alpha=0.6, ax=ax)
                ax.set_title(f"{x_axis} vs {y_axis} İlişkisi")

            elif graph_type == "Kutu Grafiği (Dağılım)":
                sns.boxplot(data=df_plot, x=x_axis, y=y_axis, ax=ax)
                plt.xticks(rotation=45)
                ax.set_title(f"{x_axis} Gruplarına Göre {y_axis} Dağılımı")

            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Grafik çizilemedi. Lütfen verilerin tipini kontrol edin.")
else:
    st.info("Lütfen bir CSV dosyası yükleyin.")