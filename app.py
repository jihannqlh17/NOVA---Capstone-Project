import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# CONFIG & PACKAGES
# =====================================
st.set_page_config(
    page_title="NOVA Anti-Stunting Intelligence",
    page_icon="👶",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    dish = pd.read_csv("dish_nutrition_clean.csv")
    ing = pd.read_csv("dish_ingredients_clean.csv")
    meta = pd.read_csv("ingredients_metadata_clean.csv")
    return dish, ing, meta

dish, ing, meta = load_data()

# =====================================
# CUSTOM BRANDING & THEME (NOVA POPOINS)
# =====================================
# Mengintegrasikan Font Poppins dan skema warna premium (Deep Teal & Clean White/Soft Gray)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Reset font global ke Poppins */
html, body, [data-testid="stAppViewContainer"], .main, block-container, q {
    font-family: 'Poppins', sans-serif !important;
    background-color: #F8FAFC; /* Light clean enterprise background */
    color: #1E293B;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}
section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
    color: #E2E8F0 !important;
}

/* Hero Section Banner */
.nova-hero {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
    padding: 35px;
    border-radius: 16px;
    margin-bottom: 30px;
    color: white;
    box-shadow: 0 10px 15px -3px rgba(2, 132, 199, 0.2);
}
.nova-hero h1 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: white !important;
    margin-bottom: 5px;
}
.nova-hero p {
    font-size: 16px;
    opacity: 0.9;
}

/* KPI Card Custom Layout */
.kpi-container {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
}
.kpi-card {
    flex: 1;
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    text-align: left;
    transition: transform 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
}
.kpi-title {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #0F172A;
}
.kpi-subtext {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 4px;
}

/* Insight Box */
.insight-box {
    background-color: #F0FDF4;
    border-left: 4px solid #16A34A;
    padding: 15px;
    border-radius: 4px 12px 12px 4px;
    margin-top: 10px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR CONTROLS
# =====================================
st.sidebar.image("https://img.icons8.com/fluency/96/baby-feet.png", width=60)
st.sidebar.markdown("## **NOVA Intelligence**\n*Panel Kontrol Intervensi Gizi*")
st.sidebar.markdown("---")

# Filter Kategori Kalori
if "calorie_category" in dish.columns:
    categories = dish["calorie_category"].dropna().unique().tolist()
    selected_cat = st.sidebar.multiselect(
        "Kategori Kalori Hidangan",
        options=categories,
        default=categories
    )
else:
    selected_cat = []

# Filter Range Protein
min_prot, max_prot = int(dish["protein"].min()), int(dish["protein"].max())
protein_range = st.sidebar.slider(
    "Target Kandungan Protein (g)",
    min_prot, max_prot, (min_prot, max_prot)
)

# Filter Range Kalori
min_cal, max_cal = int(dish["calories"].min()), int(dish["calories"].max())
cal_range = st.sidebar.slider(
    "Batas Energi / Kalori (kkal)",
    min_cal, max_cal, (min_cal, max_cal)
)

# Apply Filter
filtered_dish = dish[
    (dish["protein"] >= protein_range[0]) & (dish["protein"] <= protein_range[1]) &
    (dish["calories"] >= cal_range[0]) & (dish["calories"] <= cal_range[1])
]

if selected_cat:
    filtered_dish = filtered_dish[filtered_dish["calorie_category"].isin(selected_cat)]

# =====================================
# HERO SECTION
# =====================================
st.markdown(f"""
<div class="nova-hero">
    <h1>👶 NOVA Dashboard Portal: Nutrisi & Stunting</h1>
    <p>Aplikasi berbasis data cerdas untuk optimasi formula makanan guna menekan angka stunting nasional.</p>
    <div style="margin-top: 15px; font-size: 14px; opacity: 0.85;">
        📊 <b>{filtered_dish.shape[0]:,}</b> Menu Terfilter | <b>{meta.shape[0]:,}</b> Komponen Bahan Baku Teranalisis
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================
# KPI METRICS ROW
# =====================================
avg_protein = filtered_dish["protein"].mean()
avg_calories = filtered_dish["calories"].mean()
avg_density = filtered_dish["protein_density"].mean() if "protein_density" in filtered_dish.columns else (avg_protein/filtered_dish["mass"].mean())

kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Rata-rata Protein</div>
        <div class="kpi-value" style="color: #0284C7;">{avg_protein:.2f}g</div>
        <div class="kpi-subtext">Per porsi hidangan aktif</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Kepadatan Protein</div>
        <div class="kpi-value" style="color: #16A34A;">{avg_density:.3f}</div>
        <div class="kpi-subtext">Rasio protein dibanding total massa</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Rata-rata Kalori</div>
        <div class="kpi-value" style="color: #EA580C;">{avg_calories:.0f} kkal</div>
        <div class="kpi-subtext">Keseimbangan energi harian</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Variasi Menu</div>
        <div class="kpi-value">{filtered_dish.shape[0]}</div>
        <div class="kpi-subtext">Opsi siap distribusi korporat</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# =====================================
# ANALYTICS GRAPH ROW 1
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Pemetaan Makronutrisi untuk Formulasi")
    # Scatter plot interaktif korelasi protein vs kalori
    fig_scatter = px.scatter(
        filtered_dish,
        x="calories",
        y="protein",
        size="fat" if "fat" in filtered_dish.columns else None,
        color="calorie_category" if "calorie_category" in filtered_dish.columns else None,
        hover_data=["dish_id", "mass"],
        labels={"calories": "Kalori (kkal)", "protein": "Protein (g)", "calorie_category": "Kategori"},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_scatter.update_layout(
        font_family="Poppins",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        height=380
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        💡 <b>Insight Perusahaan:</b> Area kanan atas grafik menunjukkan menu padat kalori sekaligus tinggi protein. Menu di kuadran ini ideal sebagai target utama intervensi anak stunting yang membutuhkan kejar tumbuh.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🥧 Distribusi Klaster Kalori Menu NOVA")
    if "calorie_category" in filtered_dish.columns:
        cat_counts = filtered_dish["calorie_category"].value_counts().reset_index()
        cat_counts.columns = ["Kategori", "Jumlah"]
        
        fig_pie = px.pie(
            cat_counts,
            values="Jumlah",
            names="Kategori",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        fig_pie.update_layout(
            font_family="Poppins",
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Kolom 'calorie_category' tidak ditemukan dalam dataset.")

# =====================================
# STRATEGIC RECOMMENDATION ENGINE (ANTI-STUNTING)
# =====================================
st.markdown("---")
st.markdown("## 🎯 Rekomendasi Menu Prioritas Tinggi (Anti-Stunting)")

if not filtered_dish.empty and "protein_density" in filtered_dish.columns:
    # Mengambil top 5 makanan dengan kepadatan protein tertinggi untuk stunting
    top_stunting_menu = filtered_dish.nlargest(5, "protein_density")
    
    rec_col1, rec_col2 = st.columns([1, 2])
    
    with rec_col1:
        st.markdown("#### ⭐ **Menu Pilihan Utama Bisnis**")
        best_dish = top_stunting_menu.iloc[0]
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #16A34A;">
            <span style="background: #16A34A; color: white; padding: 3px 8px; border-radius: 20px; font-size: 11px; font-weight: bold;">RASIO TERBAIK</span>
            <h3 style="margin-top: 10px; color: #0F172A;">ID Menu: {best_dish['dish_id']}</h3>
            <p style="margin: 2px 0;"><b>Kepadatan Protein:</b> {best_dish['protein_density']:.3f}</p>
            <p style="margin: 2px 0;"><b>Protein:</b> {best_dish['protein']} gram</p>
            <p style="margin: 2px 0;"><b>Kalori:</b> {best_dish['calories']} kkal</p>
            <p style="margin: 2px 0;"><b>Total Massa:</b> {best_dish['mass']} gram</p>
        </div>
        """, unsafe_allow_html=True)
        
    with rec_col2:
        st.markdown("#### 📊 **5 Besar Menu Kepadatan Protein Tertinggi**")
        fig_rec = px.bar(
            top_stunting_menu,
            x="protein_density",
            y="dish_id",
            orientation='h',
            text_auto='.3f',
            color="protein_density",
            color_continuous_scale="Greens",
            labels={"protein_density": "Kandungan Kepadatan Protein", "dish_id": "ID Hidangan"}
        )
        fig_rec.update_layout(
            font_family="Poppins", 
            height=240, 
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False
        )
        fig_rec.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_rec, use_container_width=True)

# =====================================
# DEEP INGREDIENTS CORRELATION
# =====================================
st.markdown("---")
st.markdown("### 🔍 Matriks Korelasi Zat Gizi & Eksplorasi Data")

tab1, tab2 = st.tabs(["📊 Matriks Korelasi", "📋 Dataset Mentah Terfilter"])

with tab1:
    nutri_cols = [c for c in ["calories", "protein", "fat", "carb", "protein_density"] if c in filtered_dish.columns]
    if len(nutri_cols) >= 2:
        corr_matrix = filtered_dish[nutri_cols].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            aspect="auto"
        )
        fig_corr.update_layout(font_family="Poppins", height=400)
        st.plotly_chart(fig_corr, use_container_width=True)

with tab2:
    st.dataframe(filtered_dish, use_container_width=True)