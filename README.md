# 📱 PhonePe Pulse — Transaction Insights Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**End-to-end analysis of India's digital payment revolution using PhonePe's open-source transaction data (2018–2024)**

[🚀 Live Demo](https://phonepe-pulse-harsh.streamlit.app/) · [📓 Colab Notebook](https://colab.research.google.com/drive/1F1hnOKeMTsThlneT-L-FtOmMXeybZPwY?usp=sharing) · [📊 Dataset](https://github.com/PhonePe/pulse)

</div>

---

## 🗂️ Table of Contents
- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Key Findings](#-key-findings)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Local Setup](#-local-setup)
- [Deploy on Streamlit Cloud](#-deploy-on-streamlit-cloud)
- [Business Case Studies](#-business-case-studies)
- [Screenshots](#-screenshots)

---

## 🔍 Overview

PhonePe Pulse is India's first open digital payments dataset, publicly released by PhonePe on GitHub. This project builds a **complete data pipeline and interactive dashboard** on top of it — from raw JSON files to a live, filterable analytics platform.

| Dimension | Details |
|---|---|
| **Time Range** | 2018 Q1 → 2024 Q4 (28 quarters) |
| **Geography** | 36 States/UTs · Districts · Pin Codes |
| **Categories** | Transactions · Users · Insurance |
| **Total Rows** | 122,733 across 9 SQL tables |
| **Charts** | 20 interactive Plotly visualisations |

---

## 🚀 Live Demo

> **[https://phonepe-pulse-harsh.streamlit.app/](https://phonepe-pulse-harsh.streamlit.app/)**

The live dashboard includes:
- KPI cards with real transaction totals (₹345 Trillion decoded)
- Year/Quarter filters in sidebar affecting all pages
- India choropleth map with 4 switchable metrics
- 5 dedicated analysis pages: Overview · Transactions · Users · Insurance · India Map

---

## 💡 Key Findings

| # | Finding | Value |
|---|---|---|
| 1 | Total transaction value (2018–2024) | **₹345.52 Trillion** |
| 2 | Overall growth rate | **+7,886%** |
| 3 | CAGR (compound annual) | **107.5%** |
| 4 | P2P payments share of total value | **77.1%** (₹2,66,528 Bn) |
| 5 | Merchant payments share of count | **60.5%** (130 Bn transactions) |
| 6 | Peak registered users | **586.8 Million** |
| 7 | Top state by amount | **Telangana** (₹41,656 Bn) |
| 8 | Highest engagement ratio | **Rajasthan** (87.3 opens/user) |
| 9 | Insurance growth (2020→2024) | **27× in 4 years** |
| 10 | Bihar avg ticket vs Karnataka | **₹1,640 vs ₹1,313** (remittance signal) |

---

## 🛠️ Tech Stack

```
Data Source    →  PhonePe Pulse GitHub (JSON files, 2018–2024)
ETL            →  Python · os · json · Pandas
Database       →  SQLite (9 tables, 122,733 rows) via SQLAlchemy
Analysis       →  SQL queries (10 business cases)
Visualisation  →  Plotly Express · Plotly Graph Objects
Dashboard      →  Streamlit (609 lines, 20 charts)
Deployment     →  Streamlit Community Cloud (free)
```

---

## 📁 Project Structure

```
📦 Phone-Pe-Pulse-Data-Analysis/
├── app.py                        # Streamlit dashboard (main entry point)
├── requirements.txt              # Python dependencies
├── phonepe_pulse.db              # SQLite database (122,733 rows, 9 tables)
├── PhonePe_Pulse_Notebook.ipynb  # Google Colab ETL + SQL + EDA notebook
└── README.md                     # This file
```

> **Note:** `phonepe_pulse.db` is committed to the repo so Streamlit Cloud can access it directly — no server setup required.

---

## 🗄️ Database Schema

| Table | Rows | Description |
|---|---|---|
| `aggregated_transaction` | 5,174 | Payment category breakdown by state/year/quarter |
| `aggregated_user` | 7,955 | Device brand user counts by state/year/quarter |
| `aggregated_insurance` | 701 | Insurance transaction totals |
| `map_transaction` | 21,612 | State & district transaction totals |
| `map_user` | 21,616 | State & district registered users + app opens |
| `map_insurance` | 14,558 | State & district insurance amounts |
| `top_transaction` | 19,135 | Top states/districts/pincodes by transaction |
| `top_user` | 19,136 | Top states/districts/pincodes by user registration |
| `top_insurance` | 12,846 | Top states/districts/pincodes by insurance |
| **TOTAL** | **122,733** | |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Git

### Steps

```bash
# 1. Clone this repo
git clone https://github.com/HarshSinha-1/Phone-Pe-Pulse-Data-Analysis-for-digital-Payment-revolution-.git
cd Phone-Pe-Pulse-Data-Analysis-for-digital-Payment-revolution-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

The app opens at `http://localhost:8501`

> The `phonepe_pulse.db` database is already included in the repo. No ETL step needed to run the dashboard locally.

### Re-running the ETL (optional)
If you want to rebuild the database from scratch:
1. Open `PhonePe_Pulse_Notebook.ipynb` in Google Colab
2. Run all cells (takes ~10 minutes to clone the PhonePe repo and parse all JSON)
3. Download `phonepe_pulse.db` at the end
4. Replace the existing `.db` file in the repo root

---


## 📊 Business Case Studies

### BC1 — Transaction Dynamics
**Scenario:** PhonePe leadership wants to understand which payment categories drive value vs volume — and when to time marketing pushes.

**Finding:** P2P payments = 77.1% of all transaction VALUE (avg ticket ₹3,134) but merchant payments = 60.5% of COUNT (avg ticket ₹502). Q4 (Oct–Dec) outperforms Q1 by 18–22% every year — festival season effect.

**Recommendation:** Invest in merchant infrastructure (volume drives habit formation). Target Q3 for merchant acquisition campaigns to ride the Q4 wave.

---

### BC2 — Device Dominance
**Scenario:** PhonePe product team needs to prioritise OEM partnerships and identify dormant user segments.

**Finding:** Xiaomi (25.1%) + Samsung (19.4%) + Vivo (18.1%) = 62.6% of all registered users. App opens per user grew from near-zero in 2018 to 66 in 2024 — but 2018–2019 cohort is largely inactive.

**Recommendation:** Negotiate pre-installation deals with Xiaomi and Samsung. Launch Realme partnership (6.4%, fastest growing budget segment). Reactivate 2018–2019 passive cohort in Maharashtra and UP at zero acquisition cost.

---

### BC3 — Insurance Penetration
**Scenario:** PhonePe's insurance vertical is growing but decelerating. Leadership wants to identify where to expand next.

**Finding:** Insurance amount grew from ₹294 Mn (2020) to ₹7,927 Mn (2024) — 27× in 4 years. Growth rate fell from 410% to 31%. Kerala's per-capita insurance spend is 8× higher than Uttar Pradesh's.

**Recommendation:** Immediate expansion into UP, Bihar, and MP before growth stalls. Model the Kerala engagement playbook. UP alone represents ₹22,500 Mn potential at 25% of Kerala's per-capita rate.

---

### BC4 — Market Expansion
**Scenario:** Competitive UPI market — understanding geographic opportunities and whitespace.

**Finding:** Top 3 states (Telangana ₹41,656 Bn, Karnataka ₹40,679 Bn, Maharashtra ₹40,374 Bn) within 3% of each other. Bihar's average ticket (₹1,640) exceeds Karnataka (₹1,313) — remittance economy signal.

**Recommendation:** Protect Southern stronghold with loyalty programmes. Launch "PhonePe for Remittances" campaign in Bihar, UP, Rajasthan — the use case already exists organically.

---

### BC5 — User Engagement
**Scenario:** Understanding why some states are sticky and others have passive user bases.

**Finding:** Rajasthan engagement ratio = 87.3 opens/user. Maharashtra = 43.5 (with 2× more users). West Bengal = 20.8 (lowest of all major states). If Maharashtra reached Rajasthan's ratio: +50 billion additional app opens without acquiring a single new user.

**Recommendation:** Re-engagement campaigns in Maharashtra and West Bengal. Introduce remittance-specific features (scheduled transfers, receipt tracking) to build habit loops in large states. Track engagement ratio as a primary KPI.

---

## 📸 Screenshots

| Page | Preview |
|---|---|
| Overview | KPI cards + YoY growth + donut chart + quarterly trend |
| Transactions | Top states bar + scatter bubble + seasonal Q1-Q4 |
| Users | Device treemap + growth area + state scatter |
| Insurance | Area chart + funnel + YoY bar |
| India Map | Choropleth with 4 switchable metrics |

---

## 📄 Dataset License

The PhonePe Pulse dataset is licensed under the [CDLA-Permissive-2.0](https://github.com/PhonePe/pulse/blob/master/LICENSE) open data license.

---

## 👤 Author

**Harsh Prakash Sinha**
- GitHub: [@HarshSinha-1](https://github.com/HarshSinha-1)
- Project Repo: [Phone-Pe-Pulse-Data-Analysis-for-digital-Payment-revolution-](https://github.com/HarshSinha-1/Phone-Pe-Pulse-Data-Analysis-for-digital-Payment-revolution-)

---

<div align="center">
<sub>Built with Python · Streamlit · Plotly · SQLite · PhonePe Pulse Open Data</sub>
</div>
