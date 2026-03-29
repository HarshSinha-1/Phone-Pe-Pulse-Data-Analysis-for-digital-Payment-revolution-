"""
PhonePe Pulse — Streamlit Dashboard
------------------------------------
Run:  streamlit run app.py
Req:  pip install streamlit pandas plotly sqlalchemy requests
DB:   phonepe_pulse.db must be in the same folder as this file
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
import requests, os

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PhonePe Pulse Insights",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# THEME / CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0d1a2e 100%);
}
[data-testid="stSidebar"] {
    background: rgba(20, 10, 40, 0.95);
    border-right: 1px solid rgba(124, 58, 237, 0.3);
}
[data-testid="stSidebar"] * { color: #e0d4f5 !important; }

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(59,130,246,0.15));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-val  { font-size: 1.9rem; font-weight: 700; color: #a78bfa; line-height: 1.1; }
.kpi-lbl  { font-size: 0.78rem; color: #94a3b8; margin-top: 6px; letter-spacing: 0.03em; }
.kpi-icon { font-size: 1.4rem; margin-bottom: 4px; }

/* Section header */
.sec-header {
    font-size: 1.1rem; font-weight: 600; color: #c4b5fd;
    border-left: 3px solid #7c3aed;
    padding-left: 10px; margin: 18px 0 12px 0;
}

h1 { color: #e9d5ff !important; }
h2, h3 { color: #c4b5fd !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: rgba(124,58,237,0.1); border-radius: 12px; }
.stTabs [data-baseweb="tab"]      { color: #94a3b8; }
.stTabs [aria-selected="true"]    { color: #a78bfa !important; }

/* Plotly charts — transparent bg */
.js-plotly-plot .plotly { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════
DB_FILE = os.path.join(os.path.dirname(__file__), "phonepe_pulse.db")

@st.cache_resource
def get_engine():
    return create_engine(f"sqlite:///{DB_FILE}", echo=False)

engine = get_engine()

@st.cache_data(ttl=3600)
def q(sql: str) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)

# ══════════════════════════════════════════════════════════════
# GEOJSON — India states (exact names match DB)
# ══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_geojson():
    url = ("https://gist.githubusercontent.com/jbrobst/"
           "56c13bbbf9d97d187fea01ca62ea5112/raw/"
           "e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
    try:
        return requests.get(url, timeout=8).json()
    except Exception:
        return None

geojson = load_geojson()

# DB names (lowercase) → GeoJSON feature names (title-case)
STATE_MAP = {
    "andaman & nicobar islands"            : "Andaman & Nicobar Island",
    "andhra pradesh"                       : "Andhra Pradesh",
    "arunachal pradesh"                    : "Arunachal Pradesh",
    "assam"                                : "Assam",
    "bihar"                                : "Bihar",
    "chandigarh"                           : "Chandigarh",
    "chhattisgarh"                         : "Chhattisgarh",
    "dadra & nagar haveli & daman & diu"   : "Dadara & Nagar Haveli",
    "delhi"                                : "Delhi",
    "goa"                                  : "Goa",
    "gujarat"                              : "Gujarat",
    "haryana"                              : "Haryana",
    "himachal pradesh"                     : "Himachal Pradesh",
    "jammu & kashmir"                      : "Jammu & Kashmir",
    "jharkhand"                            : "Jharkhand",
    "karnataka"                            : "Karnataka",
    "kerala"                               : "Kerala",
    "ladakh"                               : "Ladakh",
    "lakshadweep"                          : "Lakshadweep",
    "madhya pradesh"                       : "Madhya Pradesh",
    "maharashtra"                          : "Maharashtra",
    "manipur"                              : "Manipur",
    "meghalaya"                            : "Meghalaya",
    "mizoram"                              : "Mizoram",
    "nagaland"                             : "Nagaland",
    "odisha"                               : "Odisha",
    "puducherry"                           : "Puducherry",
    "punjab"                               : "Punjab",
    "rajasthan"                            : "Rajasthan",
    "sikkim"                               : "Sikkim",
    "tamil nadu"                           : "Tamil Nadu",
    "telangana"                            : "Telangana",
    "tripura"                              : "Tripura",
    "uttar pradesh"                        : "Uttar Pradesh",
    "uttarakhand"                          : "Uttarakhand",
    "west bengal"                          : "West Bengal",
}

# ══════════════════════════════════════════════════════════════
# PLOT DEFAULTS — consistent dark theme across all charts
# ══════════════════════════════════════════════════════════════
PLOT_BG   = "rgba(0,0,0,0)"
FONT_CLR  = "#e2e8f0"
GRID_CLR  = "rgba(255,255,255,0.06)"
ACCENT    = "#7c3aed"

def dark(fig, height=400):
    fig.update_layout(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor=GRID_CLR, zeroline=False),
        yaxis=dict(gridcolor=GRID_CLR, zeroline=False),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

# ══════════════════════════════════════════════════════════════
# SIDEBAR — Global Filters
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:10px 0 4px'>"
        "<span style='font-size:2rem'>📱</span>"
        "<div style='font-size:1.1rem;font-weight:700;color:#a78bfa;margin-top:4px'>PhonePe Pulse</div>"
        "<div style='font-size:0.72rem;color:#64748b'>Transaction Insights Dashboard</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    years_df = q("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year")
    all_years = years_df["year"].tolist()
    sel_year = st.selectbox("📅 Year", ["All"] + all_years)
    sel_q    = st.selectbox("🗓️ Quarter", ["All", 1, 2, 3, 4])

    st.markdown("---")
    page = st.radio("📊 Section", [
        "🏠  Overview",
        "💳  Transactions",
        "👥  Users",
        "🛡️  Insurance",
        "🗺️  India Map",
    ])

    st.markdown("---")
    st.caption("Data: PhonePe Pulse GitHub (2018–2024)\nViz: Plotly · DB: SQLite")

# ── WHERE clause helper ───────────────────────────────────────
def W(base="state='india'", alias=""):
    parts = [base]
    if sel_year != "All":
        parts.append(f"year = {sel_year}")
    if sel_q != "All":
        parts.append(f"quarter = {sel_q}")
    return "WHERE " + " AND ".join(parts)

# ══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown("# 📱 PhonePe Pulse — Transaction Insights")
    st.markdown("<div style='color:#64748b;font-size:0.9rem;margin-top:-8px'>India's digital payment story · 2018 – 2024</div>", unsafe_allow_html=True)

    # ── KPI Row ──────────────────────────────────────────────
    kpi_txn = q(f"""
        SELECT ROUND(SUM(transaction_amount)/1e12, 2) AS total_tn,
               ROUND(SUM(transaction_count)/1e9, 2)  AS total_bn_cnt
        FROM aggregated_transaction {W()}
    """).iloc[0]

    kpi_usr = q(f"""
        SELECT ROUND(MAX(registered_users)/1e6, 1) AS peak_users
        FROM aggregated_user {W("state='india' AND brand='ALL'")}
    """).iloc[0]

    kpi_ins = q(f"""
        SELECT ROUND(SUM(insurance_count)/1e6, 2) AS ins_mn
        FROM aggregated_insurance {W()}
    """).iloc[0]

    growth_df = q("SELECT year, SUM(transaction_amount) AS amt FROM aggregated_transaction WHERE state='india' GROUP BY year ORDER BY year")
    growth_pct = round((growth_df.iloc[-1]["amt"] / growth_df.iloc[0]["amt"] - 1) * 100, 0)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl in [
        (c1, "💰", f"₹{kpi_txn['total_tn']} T",          "Total Transaction Value"),
        (c2, "🔁", f"{kpi_txn['total_bn_cnt']} Bn",       "Total Transactions"),
        (c3, "👤", f"{kpi_usr['peak_users']} Mn",          "Peak Registered Users"),
        (c4, "📈", f"+{int(growth_pct):,}%",              "Overall Amount Growth"),
    ]:
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-val">{val}</div>'
            f'<div class="kpi-lbl">{lbl}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: YoY + Payment Type ────────────────────────────
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="sec-header">📈 Year-over-Year Growth</div>', unsafe_allow_html=True)
        df_yoy = q("SELECT year, ROUND(SUM(transaction_amount)/1e9,2) AS amt_bn, SUM(transaction_count)/1e6 AS cnt_mn FROM aggregated_transaction WHERE state='india' GROUP BY year ORDER BY year")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_yoy["year"], y=df_yoy["amt_bn"], name="₹ Amount (Bn)",
                             marker_color="#7c3aed", opacity=0.85), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_yoy["year"], y=df_yoy["cnt_mn"], name="Count (Mn)",
                                 line=dict(color="#f472b6", width=3), mode="lines+markers"), secondary_y=True)
        fig.update_yaxes(title_text="Amount (₹ Bn)", secondary_y=False, gridcolor=GRID_CLR, color=FONT_CLR)
        fig.update_yaxes(title_text="Count (Millions)", secondary_y=True, color=FONT_CLR)
        st.plotly_chart(dark(fig, 360), use_container_width=True)

    with cr:
        st.markdown('<div class="sec-header">💳 Payment Category Breakdown</div>', unsafe_allow_html=True)
        df_type = q(f"SELECT transaction_type, ROUND(SUM(transaction_amount)/1e9,2) AS amt_bn FROM aggregated_transaction {W()} GROUP BY transaction_type ORDER BY amt_bn DESC")
        fig2 = px.pie(df_type, names="transaction_type", values="amt_bn", hole=0.45,
                      color_discrete_sequence=["#7c3aed","#3b82f6","#06b6d4","#10b981","#f59e0b"])
        fig2.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(dark(fig2, 360), use_container_width=True)

    # ── Row 3: Quarterly trend ───────────────────────────────
    st.markdown('<div class="sec-header">📅 Quarterly Transaction Trend</div>', unsafe_allow_html=True)
    df_q = q("SELECT year, quarter, ROUND(SUM(transaction_amount)/1e9,2) AS amt_bn FROM aggregated_transaction WHERE state='india' GROUP BY year, quarter ORDER BY year, quarter")
    df_q["period"] = df_q["year"].astype(str) + "-Q" + df_q["quarter"].astype(str)
    fig3 = px.area(df_q, x="period", y="amt_bn", markers=True,
                   labels={"amt_bn": "Amount (₹ Bn)", "period": ""},
                   color_discrete_sequence=["#7c3aed"])
    fig3.update_traces(fillcolor="rgba(124,58,237,0.15)", line_width=2.5)
    fig3.update_xaxes(tickangle=45, tickfont_size=9)
    st.plotly_chart(dark(fig3, 300), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2 — TRANSACTIONS
# ══════════════════════════════════════════════════════════════
elif page == "💳  Transactions":
    st.markdown("## 💳 Transaction Deep-Dive")

    tab1, tab2, tab3 = st.tabs(["🏆 State Rankings", "📍 Pincodes & Districts", "📅 Trend Analysis"])

    # ── Tab 1: State rankings ─────────────────────────────────
    with tab1:
        df_states = q(f"""
            SELECT entity_name AS state_name,
                   ROUND(SUM(transaction_amount)/1e9,2) AS amt_bn,
                   SUM(transaction_count) AS txn_count
            FROM map_transaction {W()}
            GROUP BY entity_name ORDER BY amt_bn DESC LIMIT 15
        """)
        fig = px.bar(df_states, x="amt_bn", y="state_name", orientation="h",
                     color="amt_bn", color_continuous_scale="Purples",
                     text="amt_bn",
                     labels={"amt_bn": "₹ Billion", "state_name": "State"},
                     title="Top 15 States by Transaction Amount")
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(dark(fig, 500), use_container_width=True)

        # Scatter: amount vs count
        fig2 = px.scatter(df_states.head(15), x="txn_count", y="amt_bn",
                          text="state_name", size="amt_bn", size_max=40,
                          color="amt_bn", color_continuous_scale="Viridis",
                          title="Transaction Amount vs Count (bubble = amount)",
                          labels={"txn_count": "Transaction Count", "amt_bn": "Amount (₹ Bn)"})
        fig2.update_traces(textposition="top center")
        st.plotly_chart(dark(fig2, 420), use_container_width=True)

    # ── Tab 2: Pincodes & Districts ──────────────────────────
    with tab2:
        cl, cr = st.columns(2)
        with cl:
            st.markdown('<div class="sec-header">📍 Top 10 Pincodes</div>', unsafe_allow_html=True)
            df_pin = q(f"""
                SELECT entity_name AS pincode, SUM(transaction_count) AS cnt,
                       ROUND(SUM(transaction_amount)/1e6,1) AS amt_mn
                FROM top_transaction {W("entity_type='pincode'")}
                GROUP BY entity_name ORDER BY cnt DESC LIMIT 10
            """)
            fig = px.bar(df_pin, x="pincode", y="cnt", color="amt_mn",
                         color_continuous_scale="Plasma", text="cnt",
                         labels={"pincode": "Pin Code", "cnt": "Transaction Count", "amt_mn": "₹ Mn"})
            fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
            st.plotly_chart(dark(fig, 380), use_container_width=True)

        with cr:
            st.markdown('<div class="sec-header">🏙️ Top 10 Districts</div>', unsafe_allow_html=True)
            df_dist = q(f"""
                SELECT entity_name AS district,
                       ROUND(SUM(transaction_amount)/1e9,2) AS amt_bn
                FROM top_transaction {W("entity_type='district'")}
                GROUP BY entity_name ORDER BY amt_bn DESC LIMIT 10
            """)
            fig2 = px.funnel(df_dist, y="district", x="amt_bn",
                             labels={"district": "District", "amt_bn": "₹ Billion"})
            fig2.update_traces(marker_color="#7c3aed")
            st.plotly_chart(dark(fig2, 380), use_container_width=True)

    # ── Tab 3: Trend ─────────────────────────────────────────
    with tab3:
        # Q1 vs Q3 comparison
        df_seas = q("""
            SELECT year,
                   ROUND(SUM(CASE WHEN quarter=1 THEN transaction_amount ELSE 0 END)/1e9,2) AS Q1,
                   ROUND(SUM(CASE WHEN quarter=2 THEN transaction_amount ELSE 0 END)/1e9,2) AS Q2,
                   ROUND(SUM(CASE WHEN quarter=3 THEN transaction_amount ELSE 0 END)/1e9,2) AS Q3,
                   ROUND(SUM(CASE WHEN quarter=4 THEN transaction_amount ELSE 0 END)/1e9,2) AS Q4
            FROM aggregated_transaction WHERE state='india'
            GROUP BY year ORDER BY year
        """)
        fig = go.Figure()
        colors = {"Q1": "#7c3aed", "Q2": "#3b82f6", "Q3": "#06b6d4", "Q4": "#10b981"}
        for qtr, clr in colors.items():
            fig.add_trace(go.Bar(x=df_seas["year"], y=df_seas[qtr], name=qtr, marker_color=clr))
        fig.update_layout(barmode="group", title="Seasonal Comparison: Q1–Q4 Each Year",
                          xaxis_title="Year", yaxis_title="Amount (₹ Bn)")
        st.plotly_chart(dark(fig, 400), use_container_width=True)

        # Per-type trend
        df_type_yr = q("""
            SELECT year, transaction_type,
                   ROUND(SUM(transaction_amount)/1e9,2) AS amt_bn
            FROM aggregated_transaction WHERE state='india'
            GROUP BY year, transaction_type ORDER BY year
        """)
        fig2 = px.line(df_type_yr, x="year", y="amt_bn", color="transaction_type",
                       markers=True, title="Transaction Type Trend Over Years",
                       labels={"amt_bn": "₹ Billion", "year": "Year", "transaction_type": "Type"})
        st.plotly_chart(dark(fig2, 380), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3 — USERS
# ══════════════════════════════════════════════════════════════
elif page == "👥  Users":
    st.markdown("## 👥 User Engagement Analysis")

    tab1, tab2 = st.tabs(["📱 Device & Growth", "🗺️ State-Level Users"])

    with tab1:
        cl, cr = st.columns(2)
        with cl:
            st.markdown('<div class="sec-header">📱 Device Brand Share</div>', unsafe_allow_html=True)
            df_dev = q(f"""
                SELECT brand, SUM(registered_users) AS users
                FROM aggregated_user {W("state='india' AND brand != 'ALL'")}
                GROUP BY brand ORDER BY users DESC LIMIT 12
            """)
            fig = px.treemap(df_dev, path=["brand"], values="users",
                             color="users", color_continuous_scale="RdYlGn",
                             title="Device Brands by User Count")
            st.plotly_chart(dark(fig, 380), use_container_width=True)

        with cr:
            st.markdown('<div class="sec-header">📈 Registered Users Growth</div>', unsafe_allow_html=True)
            df_grow = q("""
                SELECT year, ROUND(SUM(registered_users)/1e6,2) AS users_mn
                FROM aggregated_user WHERE state='india' AND brand='ALL'
                GROUP BY year ORDER BY year
            """)
            fig2 = px.area(df_grow, x="year", y="users_mn", markers=True,
                           labels={"users_mn": "Users (Mn)", "year": "Year"},
                           color_discrete_sequence=["#7c3aed"])
            fig2.update_traces(fillcolor="rgba(124,58,237,0.2)", line_width=2.5)
            st.plotly_chart(dark(fig2, 380), use_container_width=True)

        # App opens per user ratio
        df_ratio = q("""
            SELECT year,
                   ROUND(SUM(app_opens)*1.0 / NULLIF(SUM(CASE WHEN brand='ALL' THEN registered_users END),0), 1) AS opens_per_user
            FROM aggregated_user WHERE state='india'
            GROUP BY year ORDER BY year
        """)
        fig3 = px.bar(df_ratio, x="year", y="opens_per_user",
                      title="App Opens per Registered User (Annual)",
                      color="opens_per_user", color_continuous_scale="Teal",
                      text="opens_per_user", labels={"opens_per_user": "Opens / User", "year": "Year"})
        fig3.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        st.plotly_chart(dark(fig3, 340), use_container_width=True)

    with tab2:
        df_su = q(f"""
            SELECT entity_name AS state_name,
                   SUM(registered_users) AS users,
                   SUM(app_opens) AS app_opens
            FROM map_user {W()}
            GROUP BY entity_name ORDER BY users DESC LIMIT 20
        """)
        fig = px.scatter(df_su, x="users", y="app_opens",
                         size="users", text="state_name", size_max=50,
                         color="app_opens", color_continuous_scale="Bluered",
                         title="Registered Users vs App Opens by State",
                         labels={"users": "Registered Users", "app_opens": "App Opens"})
        fig.update_traces(textposition="top center", textfont_size=9)
        st.plotly_chart(dark(fig, 500), use_container_width=True)

        # Top 10 states bar
        fig2 = px.bar(df_su.head(10), x="state_name", y="users",
                      title="Top 10 States by Registered Users",
                      color="users", color_continuous_scale="Purples",
                      labels={"state_name": "State", "users": "Registered Users"})
        fig2.update_xaxes(tickangle=30)
        st.plotly_chart(dark(fig2, 360), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4 — INSURANCE
# ══════════════════════════════════════════════════════════════
elif page == "🛡️  Insurance":
    st.markdown("## 🛡️ Insurance Analytics")

    # Growth trend
    df_ins_t = q("""
        SELECT year, quarter,
               SUM(insurance_count)                    AS total_count,
               ROUND(SUM(insurance_amount)/1e6, 2)    AS amt_mn
        FROM aggregated_insurance WHERE state='india'
        GROUP BY year, quarter ORDER BY year, quarter
    """)
    df_ins_t["period"] = df_ins_t["year"].astype(str) + "-Q" + df_ins_t["quarter"].astype(str)

    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="sec-header">📈 Insurance Amount Growth (₹ Mn)</div>', unsafe_allow_html=True)
        fig = px.area(df_ins_t, x="period", y="amt_mn",
                      color_discrete_sequence=["#06b6d4"],
                      labels={"amt_mn": "Amount (₹ Mn)", "period": "Quarter"})
        fig.update_traces(fillcolor="rgba(6,182,212,0.15)", line_width=2.5)
        fig.update_xaxes(tickangle=45, tickfont_size=9)
        st.plotly_chart(dark(fig, 360), use_container_width=True)

    with cr:
        st.markdown('<div class="sec-header">🔢 Insurance Count Growth</div>', unsafe_allow_html=True)
        fig2 = px.bar(df_ins_t, x="period", y="total_count",
                      color="total_count", color_continuous_scale="Teal",
                      labels={"total_count": "Count", "period": "Quarter"})
        fig2.update_xaxes(tickangle=45, tickfont_size=9)
        st.plotly_chart(dark(fig2, 360), use_container_width=True)

    # Top states
    df_ins_st = q(f"""
        SELECT entity_name AS state_name,
               ROUND(SUM(insurance_amount)/1e6, 2) AS amt_mn,
               SUM(insurance_count) AS cnt
        FROM map_insurance {W()}
        GROUP BY entity_name ORDER BY amt_mn DESC LIMIT 15
    """)

    cl2, cr2 = st.columns(2)
    with cl2:
        st.markdown('<div class="sec-header">🏆 Top States by Insurance Amount</div>', unsafe_allow_html=True)
        fig3 = px.bar(df_ins_st, x="state_name", y="amt_mn",
                      color="amt_mn", color_continuous_scale="Teal",
                      labels={"state_name": "State", "amt_mn": "₹ Mn"})
        fig3.update_xaxes(tickangle=35)
        st.plotly_chart(dark(fig3, 360), use_container_width=True)

    with cr2:
        st.markdown('<div class="sec-header">📊 Top 10 States — Funnel View</div>', unsafe_allow_html=True)
        fig4 = px.funnel(df_ins_st.head(10), y="state_name", x="amt_mn",
                         labels={"state_name": "State", "amt_mn": "₹ Mn"})
        fig4.update_traces(marker_color="#06b6d4")
        st.plotly_chart(dark(fig4, 360), use_container_width=True)

    # YoY insurance
    df_ins_yr = q("""
        SELECT year, ROUND(SUM(insurance_amount)/1e6,2) AS amt_mn
        FROM aggregated_insurance WHERE state='india'
        GROUP BY year ORDER BY year
    """)
    fig5 = px.bar(df_ins_yr, x="year", y="amt_mn",
                  title="Insurance Amount by Year (₹ Mn)",
                  color="amt_mn", color_continuous_scale="GnBu", text="amt_mn",
                  labels={"year": "Year", "amt_mn": "₹ Mn"})
    fig5.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    st.plotly_chart(dark(fig5, 340), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 5 — INDIA MAP
# ══════════════════════════════════════════════════════════════
elif page == "🗺️  India Map":
    st.markdown("## 🗺️ India State-Level Heatmap")

    metric = st.radio(
        "Select Metric",
        ["💰 Transaction Amount", "🔁 Transaction Count", "👥 Registered Users", "🛡️ Insurance Amount"],
        horizontal=True
    )

    if metric == "💰 Transaction Amount":
        df_m = q(f"""
            SELECT entity_name, ROUND(SUM(transaction_amount)/1e9,2) AS value
            FROM map_transaction {W()} GROUP BY entity_name
        """)
        label = "Txn Amount (₹ Bn)"
        cscale = "Purples"

    elif metric == "🔁 Transaction Count":
        df_m = q(f"""
            SELECT entity_name, SUM(transaction_count) AS value
            FROM map_transaction {W()} GROUP BY entity_name
        """)
        label = "Transaction Count"
        cscale = "Blues"

    elif metric == "👥 Registered Users":
        df_m = q(f"""
            SELECT entity_name, ROUND(SUM(registered_users)/1e6,2) AS value
            FROM map_user {W()} GROUP BY entity_name
        """)
        label = "Registered Users (Mn)"
        cscale = "Greens"

    else:  # Insurance
        df_m = q(f"""
            SELECT entity_name, ROUND(SUM(insurance_amount)/1e6,2) AS value
            FROM map_insurance {W()} GROUP BY entity_name
        """)
        label = "Insurance Amount (₹ Mn)"
        cscale = "Teal"

    # Map DB state name → GeoJSON feature name
    df_m["geo_name"] = df_m["entity_name"].map(STATE_MAP)
    df_m_clean = df_m.dropna(subset=["geo_name"])

    if geojson:
        fig = px.choropleth(
            df_m_clean,
            geojson=geojson,
            featureidkey="properties.ST_NM",
            locations="geo_name",
            color="value",
            color_continuous_scale=cscale,
            hover_name="geo_name",
            hover_data={"value": True, "geo_name": False},
            labels={"value": label},
            title=f"India State Heatmap — {label}",
        )
        fig.update_geos(fitbounds="locations", visible=False, bgcolor=PLOT_BG)
        fig.update_layout(
            paper_bgcolor=PLOT_BG,
            font=dict(color=FONT_CLR),
            height=580,
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(title=label, tickfont=dict(color=FONT_CLR)),
            geo=dict(bgcolor=PLOT_BG),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Table below map
        st.markdown('<div class="sec-header">📋 State-wise Data</div>', unsafe_allow_html=True)
        display = df_m_clean[["geo_name", "value"]].rename(columns={"geo_name": "State", "value": label})
        st.dataframe(display.sort_values(label, ascending=False).reset_index(drop=True),
                     use_container_width=True, height=400)
    else:
        st.warning("⚠️ Could not load GeoJSON. Check internet connection.")
        st.dataframe(df_m.sort_values("value", ascending=False))