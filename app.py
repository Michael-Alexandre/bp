import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# page config
# ==================================================
st.set_page_config(
    page_title="Dog BP Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# corp style (CSS)
# ==================================================
st.markdown("""
<style>
[data-testid="metric-container"] {
    background-color: #F8F9FA;
    border: 1px solid #E0E0E0;
    padding: 15px;
    border-radius: 8px;
}
h1, h2, h3 {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# TiTle
# ==================================================
st.title("Dog BP Dashboard")
st.caption("Analise dos dados de pressão arterial e frequência cardíaca do Max")


# ==================================================
# load data
# ==================================================
@st.cache_data
def load_data(file):
    colunas = [
        "data_hora",
        "sistolica",
        "diastolica",
        "bpm"
    ]
    df = pd.read_csv(file,header=None,names=colunas, parse_dates=["data_hora"])
    df["ano"] = df["data_hora"].dt.year
    df["mes"] = df["data_hora"].dt.month
    df["mes_nome"] = df["data_hora"].dt.strftime("%B")
    return df


# ==================================================
# SIDEBAR – CONTROL
# ==================================================
st.sidebar.header("Controls")


uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type="csv"
)


if uploaded_file is None:
    st.warning("Please upload a CSV file to start the analysis.")
    st.stop()


df = load_data(uploaded_file)


ano = st.sidebar.selectbox(
    "Ano",
    sorted(df["ano"].unique())
)


mes = st.sidebar.selectbox(
    "Mes",
    sorted(df[df["ano"] == ano]["mes"].unique())
)


df_filtered = df[
    (df["ano"] == ano) &
    (df["mes"] == mes)
]
df_filtered = df_filtered.dropna( subset=["sistolica", "diastolica", "bpm"] )
df_filtered["dt_diames"] = df_filtered["data_hora"].dt.strftime("%d/%m %H:%M")

# ==================================================
# KPIs – corp
# ==================================================
st.subheader("Executive Summary")


kpi1, kpi2, kpi3 = st.columns(3)


kpi1.metric(
    "Media Sistolica",
    f"{df_filtered['sistolica'].mean():.1f} mmHg"
)


kpi2.metric(
    "Media Diastolica",
    f"{df_filtered['diastolica'].mean():.1f} mmHg"
)


kpi3.metric(
    "Media Frequencia Cardiaca",
    f"{df_filtered['bpm'].mean():.1f} BPM"
)


st.divider()


# ==================================================
# GRÁFICO PRINCIPAL
# ==================================================
st.subheader("Monthly Trend Analysis")

fig = px.scatter(
    df_filtered,
    x="dt_diames",
    y=["sistolica", "diastolica", "bpm"],
    labels={
        "value": "Measurement",
        "dt_diames": "Date / Time",
        "variable": "Indicator"
    },
)

fig.update_traces(marker_size=20)
fig.update_xaxes(type="category", tickformat="%d/%m %H:%M")
fig.update_layout(
    hovermode="x unified",
    legend_title_text="Indicators",
    template="plotly_white"
)


st.plotly_chart(fig, use_container_width=True)


# ==================================================
# TABELA DETALHADA
# ==================================================
st.subheader("Tabela Detalhada Ano, Mes, Dia e Hora")


st.dataframe(
    df_filtered
        .sort_values("data_hora")
        .reset_index(drop=True),
    use_container_width=True

)




