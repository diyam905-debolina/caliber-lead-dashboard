import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import io

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Caliber Lead Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS  – clean, professional look
# ─────────────────────────────────────────
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit default header */
#MainMenu, footer, header { visibility: hidden; }

/* Main background */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Dashboard title bar */
.dash-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 16px 0;
    border-bottom: 1px solid #eee;
    margin-bottom: 20px;
}

.dash-title h1 {
    font-size: 22px;
    font-weight: 700;
    color: #1a1a1a;
    margin: 0;
}

.dash-title span {
    font-size: 12px;
    background: #E1F5EE;
    color: #0F6E56;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
}

/* KPI Cards */
.kpi-card {
    background: #F8F9FA;
    border-radius: 10px;
    padding: 18px 20px;
    border: 0.5px solid #EBEBEB;
}

.kpi-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #888;
    font-weight: 600;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1;
}

.kpi-sub {
    font-size: 11px;
    margin-top: 5px;
    color: #888;
}

.kpi-sub.green { color: #1D9E75; }
.kpi-sub.red   { color: #D85A30; }

/* Section titles */
.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 0.5px solid #eee;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: #1E293B;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #94A3B8 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

/* Metric containers */
div[data-testid="metric-container"] {
    background: #F8F9FA;
    border: 0.5px solid #EBEBEB;
    border-radius: 10px;
    padding: 14px 18px;
}

div[data-testid="metric-container"] label {
    font-size: 10px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #888 !important;
    font-weight: 600;
}

div[data-testid="metric-container"] [data-testid="metric-value"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
}

/* Table styling */
.dataframe {
    font-size: 12px !important;
    border-radius: 8px;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid #eee;
}

.stTabs [data-baseweb="tab"] {
    font-size: 12px;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 4px 4px 0 0;
    color: #888;
}

.stTabs [aria-selected="true"] {
    color: #3266ad !important;
    font-weight: 600;
    background: white !important;
    border-bottom: 2px solid #3266ad !important;
}

/* Info box */
.info-box {
    background: #F0F7FF;
    border: 0.5px solid #C3DCFB;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #185FA5;
    margin-bottom: 14px;
}

/* Marketing badge */
.mkt-badge {
    background: #E1F5EE;
    color: #0F6E56;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

/* Pill badges */
.pill-green  { background:#E1F5EE; color:#0F6E56; padding:2px 8px; border-radius:20px; font-size:10px; font-weight:600; }
.pill-blue   { background:#E6F1FB; color:#185FA5; padding:2px 8px; border-radius:20px; font-size:10px; font-weight:600; }
.pill-orange { background:#FAEEDA; color:#854F0B; padding:2px 8px; border-radius:20px; font-size:10px; font-weight:600; }
.pill-red    { background:#FCEBEB; color:#A32D2D; padding:2px 8px; border-radius:20px; font-size:10px; font-weight:600; }
.pill-gray   { background:#F1EFE8; color:#5F5E5A; padding:2px 8px; border-radius:20px; font-size:10px; font-weight:600; }

/* Upload area */
.upload-hint {
    background: #F8F9FA;
    border: 1.5px dashed #D1D5DB;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    color: #888;
    font-size: 12px;
    margin-bottom: 16px;
}

/* Divider */
.subtle-divider {
    border: none;
    border-top: 0.5px solid #eee;
    margin: 16px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONSTANTS & FORMULAS
# ─────────────────────────────────────────
PRODUCTIVE_STATUSES = [
    'Contacted - Interested',
    'Meeting Schedule',
    'Budget Constraint',
    'Deferred Interest'
]

UNPRODUCTIVE_STATUSES = [
    'Contacted - Irrelevant',
    'Knowledge / Job - Irrelevant',
    'Contacted - Not Interested',
    'Already In - Funnel',
    'Unresponsive'
]

COLORS = {
    'productive':   '#3266ad',
    'unproductive': '#D85A30',
    'converted':    '#1D9E75',
    'pursuing':     '#BA7517',
    'business':     '#185FA5',
    'marketing':    '#1D9E75',
    'neutral':      '#B4B2A9',
}

CHART_COLORS = ['#3266ad','#1D9E75','#D85A30','#BA7517','#8B5CF6','#0F6E56','#993556','#185FA5']

REGION_ORDER  = ['Guj & North', 'South', 'Mah & Goa', 'APAC', 'MENA']
STAGE_ORDER   = ['Discovery/Teaser Demo','Demo','Technical Evaluation','Negotiation/Review','CP wrt SOW','Closed Won']

# ─────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────
def normalize_region(r):
    if not r or str(r).strip() == '' or str(r).lower() == 'nan':
        return 'Unknown'
    r = str(r).strip()
    if any(x in r for x in ['Guj','Gujarat','North']): return 'Guj & North'
    if 'South'        in r: return 'South'
    if any(x in r for x in ['Maharashtra','Goa','Mah']): return 'Mah & Goa'
    if 'APAC'         in r: return 'APAC'
    if 'MENA'         in r: return 'MENA'
    return r

def normalize_product(p):
    if not p or str(p).strip() == '' or str(p).lower() == 'nan':
        return 'Unknown'
    p = str(p).strip()
    # D&I and DSG are the same product group
    if any(x in p for x in ['D&I','DSG','D & I']): return 'D&I / DSG'
    # Remove trailing semicolons (e.g. "Manufacturing; OTT")
    if ';' in p: return p.split(';')[0].strip()
    return p

def pct(num, den, decimals=1):
    return round(num / den * 100, decimals) if den > 0 else 0

def pill_color(value, low=15, mid=40):
    """Return CSS class based on percentage value."""
    if value >= mid:   return 'pill-green'
    if value >= low:   return 'pill-blue'
    if value > 0:      return 'pill-orange'
    return 'pill-gray'

def unprod_pill_color(value):
    if value >= 75: return 'pill-red'
    if value >= 50: return 'pill-orange'
    return 'pill-green'

# ─────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────
def load_data(uploaded_file):
    """Load and process CSV file uploaded by user."""
    df = pd.read_csv(uploaded_file, dtype=str).fillna('')

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    col_map = {
        'full name':         'full_name',
        'name':              'full_name',
        'company':           'company',
        'account name':      'account_name',
        'region':            'region',
        'territory':         'region',
        'product group':     'product_group',
        'product':           'product_group',
        'prod category':     'product_group',
        'lead status':       'lead_status',
        'status':            'lead_status',
        'stage':             'stage',
        'pipeline stage':    'stage',
        'type of source':    'type_of_source',
        'source':            'type_of_source',
        'conversion source': 'conversion_source',
        'channel':           'conversion_source',
        'created time':      'created_time',
        'date':              'created_time',
    }

    rename = {}
    for col in df.columns:
        if col in col_map:
            rename[col] = col_map[col]
    df = df.rename(columns=rename)

    # Ensure required columns exist
    for req in ['region','product_group','conversion_source']:
        if req not in df.columns:
            df[req] = 'Unknown'
    if 'lead_status' not in df.columns:
        df['lead_status'] = ''
    if 'type_of_source' not in df.columns:
        df['type_of_source'] = ''
    if 'stage' not in df.columns:
        df['stage'] = ''
    if 'full_name' not in df.columns:
        df['full_name'] = df.get('account_name', pd.Series([''] * len(df)))
    if 'created_time' not in df.columns:
        df['created_time'] = ''

    # Normalize region and product
    df['region']        = df['region'].apply(normalize_region)
    df['product_group'] = df['product_group'].apply(normalize_product)

    # Classify each row
    df['is_productive']   = df['lead_status'].isin(PRODUCTIVE_STATUSES)
    df['is_unproductive'] = df['lead_status'].isin(UNPRODUCTIVE_STATUSES)
    df['is_pursuing']     = df['lead_status'] == 'Pursuing'
    df['is_potential']    = df['lead_status'] == ''   # Potential sheet rows have no lead_status
    # Potentials from Potential sheet (stage column filled, lead_status empty)
    df['is_converted']    = (df['lead_status'] == '') & (df['stage'] != '')

    return df


def compute_metrics(df):
    total       = len(df)
    productive  = df['is_productive'].sum() + df['is_potential'].sum()
    unproductive= df['is_unproductive'].sum()
    pursuing    = df['is_pursuing'].sum()
    converted   = df['is_potential'].sum()
    prod_pct    = pct(productive, total)
    unprod_pct  = pct(unproductive, total)
    conv_pct    = pct(converted, productive)
    return dict(total=total, productive=productive, unproductive=unproductive,
                pursuing=pursuing, converted=converted,
                prod_pct=prod_pct, unprod_pct=unprod_pct, conv_pct=conv_pct)


def channel_metrics(df, channel):
    sub = df[df['conversion_source'] == channel]
    return compute_metrics(sub)


def breakdown_stats(df, group_col):
    """Return a DataFrame with metric columns grouped by group_col."""
    rows = []
    for val in df[group_col].unique():
        sub = df[df[group_col] == val]
        m = compute_metrics(sub)
        rows.append({
            group_col:      val,
            'Total':        m['total'],
            'Productive':   m['productive'],
            'Prod %':       m['prod_pct'],
            'Unproductive': m['unproductive'],
            'Unprod %':     m['unprod_pct'],
            'Converted':    m['converted'],
            'Conv %':       m['conv_pct'],
        })
    return pd.DataFrame(rows).sort_values('Total', ascending=False).reset_index(drop=True)

# ─────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────
CHART_LAYOUT = dict(
    font_family='Inter',
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    height=280,
)

def bar_chart(df, x, y, color=None, title='', horizontal=False, colors=None, height=280):
    if horizontal:
        fig = px.bar(df, x=y, y=x, orientation='h',
                     color=color, text_auto=True, title=title,
                     color_discrete_sequence=colors or CHART_COLORS)
        fig.update_traces(textfont_size=10, textposition='outside')
        fig.update_layout(**{**CHART_LAYOUT, 'height': height})
        fig.update_xaxes(showgrid=True, gridcolor='#F0F0F0', zeroline=False)
        fig.update_yaxes(showgrid=False)
    else:
        fig = px.bar(df, x=x, y=y, color=color, text_auto=True, title=title,
                     color_discrete_sequence=colors or CHART_COLORS)
        fig.update_traces(textfont_size=10, textposition='outside')
        fig.update_layout(**{**CHART_LAYOUT, 'height': height})
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0', zeroline=False)
    return fig


def donut_chart(labels, values, title='', colors=None, height=260):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.62,
        marker_colors=colors or CHART_COLORS,
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>'
    ))
    fig.update_layout(**{**CHART_LAYOUT, 'height': height, 'title': title,
                         'showlegend': True})
    return fig


def grouped_bar(categories, datasets, title='', height=280):
    fig = go.Figure()
    for ds in datasets:
        fig.add_trace(go.Bar(
            name=ds['name'], x=categories, y=ds['data'],
            marker_color=ds['color'],
            text=ds['data'], textposition='outside', textfont_size=10
        ))
    fig.update_layout(**{**CHART_LAYOUT, 'height': height, 'title': title,
                         'barmode': 'group'})
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0', zeroline=False)
    return fig


# ─────────────────────────────────────────
# DOWNLOAD HELPER
# ─────────────────────────────────────────
def df_to_excel(dfs_dict):
    """Convert dict of {sheet_name: df} to Excel bytes."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        for sheet, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    return buf.getvalue()


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Caliber Lead Analytics")
    st.markdown("---")

    st.markdown("### Upload Data")
    uploaded_file = st.file_uploader(
        "Upload monthly CSV export from Zoho CRM",
        type=['csv'],
        help="Export from Zoho: Lead sheet + Potential sheet combined as one CSV"
    )

    if uploaded_file:
        st.success(f"✓ {uploaded_file.name}")

    st.markdown("---")

    if uploaded_file:
        st.markdown("### Filters")
        region_filter  = st.multiselect("Region",  REGION_ORDER, default=[], placeholder="All regions")
        product_filter = st.multiselect("Product", [], default=[], placeholder="All products",
                                         key='product_filter_placeholder')
        channel_filter = st.selectbox("Channel", ["All", "Business", "Marketing"])

        st.markdown("---")
        st.markdown("### Period Comparison")
        prev_file = st.file_uploader(
            "Prior month CSV (optional)",
            type=['csv'],
            help="Upload previous month to enable period comparison"
        )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#64748B; line-height:1.6;'>
    <b>Formulas:</b><br>
    Productive = Interested + Meeting + Budget + Deferred + Potential<br><br>
    Unproductive = Not Interested + Irrelevant + Job/Knowledge + Unresponsive + Already in Funnel<br><br>
    Conversion % = Potential / Productive
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────

if not uploaded_file:
    # Welcome screen
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px;'>
        <div style='font-size:56px; margin-bottom:16px;'>📊</div>
        <h2 style='font-size:24px; font-weight:700; color:#1a1a1a; margin-bottom:10px;'>
            Caliber Technologies — Lead Analytics Dashboard
        </h2>
        <p style='font-size:14px; color:#888; max-width:480px; margin:0 auto 24px;'>
            Upload your monthly Zoho CRM export to generate the full interactive dashboard —
            overview, channel performance, region & product breakdown, funnel tracking, and period comparison.
        </p>
        <div style='display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin-top:20px;'>
            <div style='background:#F8F9FA; border-radius:8px; padding:16px 20px; min-width:140px;'>
                <div style='font-size:20px;'>⬆️</div>
                <div style='font-size:12px; font-weight:600; margin-top:6px;'>Upload CSV</div>
                <div style='font-size:11px; color:#888;'>From sidebar</div>
            </div>
            <div style='background:#F8F9FA; border-radius:8px; padding:16px 20px; min-width:140px;'>
                <div style='font-size:20px;'>📊</div>
                <div style='font-size:12px; font-weight:600; margin-top:6px;'>View Dashboard</div>
                <div style='font-size:11px; color:#888;'>All 7 tabs auto-fill</div>
            </div>
            <div style='background:#F8F9FA; border-radius:8px; padding:16px 20px; min-width:140px;'>
                <div style='font-size:20px;'>📥</div>
                <div style='font-size:12px; font-weight:600; margin-top:6px;'>Export Report</div>
                <div style='font-size:11px; color:#888;'>Excel or PDF</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Load data
df = load_data(uploaded_file)
prev_df = load_data(prev_file) if 'prev_file' in dir() and prev_file else None

# Apply sidebar filters
filtered_df = df.copy()
if 'region_filter' in dir() and region_filter:
    filtered_df = filtered_df[filtered_df['region'].isin(region_filter)]
if 'channel_filter' in dir() and channel_filter != 'All':
    filtered_df = filtered_df[filtered_df['conversion_source'] == channel_filter]

# Update product filter options dynamically
products_available = sorted(filtered_df['product_group'].unique().tolist())
with st.sidebar:
    if uploaded_file:
        product_filter_real = st.multiselect(
            "Product (live)", products_available, default=[], placeholder="All products"
        )
        if product_filter_real:
            filtered_df = filtered_df[filtered_df['product_group'].isin(product_filter_real)]

# Metrics
m = compute_metrics(filtered_df)

# Dashboard header
month_label = uploaded_file.name.replace('.csv', '').replace('_', ' ')
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown(f"<h2 style='font-size:20px;font-weight:700;margin:0;padding:0;'>📊 Caliber Technologies — Lead Analytics</h2>", unsafe_allow_html=True)
with col_badge:
    st.markdown(f"<div style='text-align:right;margin-top:4px;'><span style='background:#E1F5EE;color:#0F6E56;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:600;'>{month_label}</span></div>", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:0.5px solid #eee;margin:10px 0 16px 0;'>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Overview",
    "📡 Channel Performance",
    "🔗 Source Performance",
    "🗺️ Region Performance",
    "📦 Product Performance",
    "🔄 Funnel Movement",
    "📅 Period Comparison"
])


# ═══════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════
with tab1:
    # KPI Row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.metric("Total Leads", m['total'])
    with c2:
        st.metric("Productive", m['productive'], f"{m['prod_pct']}%")
    with c3:
        st.metric("Unproductive", m['unproductive'], f"-{m['unprod_pct']}%")
    with c4:
        st.metric("Pursuing", m['pursuing'])
    with c5:
        st.metric("Converted", m['converted'])
    with c6:
        st.metric("Conversion %", f"{m['conv_pct']}%")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # Charts Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Lead Quality Distribution</div>", unsafe_allow_html=True)
        fig = donut_chart(
            labels=['Converted', 'Productive', 'Unproductive', 'Pursuing'],
            values=[m['converted'], m['productive'] - m['converted'], m['unproductive'], m['pursuing']],
            colors=[COLORS['converted'], COLORS['productive'], COLORS['unproductive'], COLORS['pursuing']]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("<div class='section-title'>Conversion Contribution by Channel</div>", unsafe_allow_html=True)
        biz_conv = filtered_df[(filtered_df['conversion_source'] == 'Business') & (filtered_df['is_potential'])].shape[0]
        mkt_conv = filtered_df[(filtered_df['conversion_source'] == 'Marketing') & (filtered_df['is_potential'])].shape[0]
        fig = donut_chart(
            labels=['Business', 'Marketing'],
            values=[biz_conv, mkt_conv],
            colors=[COLORS['business'], COLORS['marketing']]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Unproductive breakdown
    st.markdown("<div class='section-title'>Unproductive Lead Breakdown</div>", unsafe_allow_html=True)
    unprod_counts = (
        filtered_df[filtered_df['is_unproductive']]
        ['lead_status'].value_counts().reset_index()
    )
    unprod_counts.columns = ['Status', 'Count']
    unprod_counts['Status'] = unprod_counts['Status'].str.replace('Contacted - ', '').str.replace('Knowledge / ', '')
    fig = bar_chart(unprod_counts, 'Status', 'Count',
                    horizontal=True,
                    colors=['#F09595','#ED93B1','#EF9F27','#AFA9EC','#B4B2A9'],
                    height=200)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Excel export
    st.markdown("<hr style='border:none;border-top:0.5px solid #eee;margin:16px 0;'>", unsafe_allow_html=True)
    col_dl, col_info = st.columns([1, 3])
    with col_dl:
        excel_data = df_to_excel({'Overview': filtered_df[['full_name','region','product_group','lead_status','type_of_source','conversion_source','stage']]})
        st.download_button(
            "📥 Download Report (Excel)",
            data=excel_data,
            file_name=f"Caliber_Lead_Report_{datetime.today().strftime('%Y_%m')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_info:
        st.caption("Downloads all current data as Excel. For PDF: use browser Print → Save as PDF (Ctrl+P).")


# ═══════════════════════════════
# TAB 2 — CHANNEL PERFORMANCE
# ═══════════════════════════════
with tab2:
    biz = channel_metrics(filtered_df, 'Business')
    mkt = channel_metrics(filtered_df, 'Marketing')

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-title'>🔵 Business Channel</div>", unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total", biz['total'])
        b2.metric("Productive", biz['productive'], f"{biz['prod_pct']}%")
        b3.metric("Unproductive", biz['unproductive'])
        b4.metric("Converted", biz['converted'], f"Conv {biz['conv_pct']}%")

        biz_df = filtered_df[filtered_df['conversion_source'] == 'Business']
        biz_status = biz_df['lead_status'].value_counts().reset_index()
        biz_status.columns = ['Status', 'Count']
        st.dataframe(biz_status, hide_index=True, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>🟢 Marketing Channel</div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total", mkt['total'])
        m2.metric("Productive", mkt['productive'], f"{mkt['prod_pct']}%")
        m3.metric("Unproductive", mkt['unproductive'])
        m4.metric("Converted", mkt['converted'], f"Conv {mkt['conv_pct']}%")

        mkt_df = filtered_df[filtered_df['conversion_source'] == 'Marketing']
        mkt_status = mkt_df['lead_status'].value_counts().reset_index()
        mkt_status.columns = ['Status', 'Count']
        st.dataframe(mkt_status, hide_index=True, use_container_width=True)

    st.markdown("<div class='section-title'>Channel Performance — Side-by-Side</div>", unsafe_allow_html=True)
    fig = grouped_bar(
        categories=['Total', 'Productive', 'Unproductive', 'Converted'],
        datasets=[
            {'name': 'Business', 'data': [biz['total'], biz['productive'], biz['unproductive'], biz['converted']], 'color': COLORS['business']},
            {'name': 'Marketing', 'data': [mkt['total'], mkt['productive'], mkt['unproductive'], mkt['converted']], 'color': COLORS['marketing']},
        ]
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Download
    ch_df = pd.DataFrame([
        {'Channel': 'Business', **{k: v for k, v in biz.items()}},
        {'Channel': 'Marketing', **{k: v for k, v in mkt.items()}}
    ])
    st.download_button(
        "📥 Download Channel Data",
        data=df_to_excel({'Channel Performance': ch_df}),
        file_name=f"Caliber_Channel_Performance_{datetime.today().strftime('%Y_%m')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════
# TAB 3 — SOURCE PERFORMANCE
# ═══════════════════════════════
with tab3:
    src_df = (
        filtered_df.groupby('type_of_source')
        .agg(
            Total=('type_of_source', 'count'),
            Productive=('is_productive', 'sum'),
            Unproductive=('is_unproductive', 'sum'),
            Pursuing=('is_pursuing', 'sum'),
        )
        .reset_index()
        .rename(columns={'type_of_source': 'Source'})
        .sort_values('Total', ascending=False)
    )
    src_df['Prod %']    = src_df.apply(lambda r: pct(r['Productive'], r['Total']), axis=1)
    src_df['Unprod %']  = src_df.apply(lambda r: pct(r['Unproductive'], r['Total']), axis=1)

    # KPI row
    cols = st.columns(len(src_df))
    for i, row in src_df.iterrows():
        with cols[list(src_df.index).index(i)]:
            st.metric(row['Source'], int(row['Total']), f"Prod {row['Prod %']}%")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Lead Volume by Source</div>", unsafe_allow_html=True)
        fig = donut_chart(
            labels=src_df['Source'].tolist(),
            values=src_df['Total'].tolist(),
            colors=CHART_COLORS
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("<div class='section-title'>Productive % by Source</div>", unsafe_allow_html=True)
        fig = bar_chart(
            src_df.sort_values('Prod %', ascending=True),
            'Source', 'Prod %', horizontal=True,
            colors=CHART_COLORS
        )
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-title'>Source Performance — Detailed View</div>", unsafe_allow_html=True)
    st.dataframe(
        src_df[['Source','Total','Productive','Prod %','Unproductive','Unprod %','Pursuing']],
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Source Data",
        data=df_to_excel({'Source Performance': src_df}),
        file_name=f"Caliber_Source_Performance_{datetime.today().strftime('%Y_%m')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════
# TAB 4 — REGION PERFORMANCE
# ═══════════════════════════════
with tab4:
    st.markdown("""
    <div class='info-box'>
        📌 <b>Marketing Channel Only</b> — Metrics include only leads from Marketing channel
    </div>
    """, unsafe_allow_html=True)

    mkt_df = filtered_df[filtered_df['conversion_source'] == 'Marketing']
    rg_df = breakdown_stats(mkt_df, 'region')

    # KPI row
    region_cols = st.columns(len(rg_df))
    for i, row in rg_df.iterrows():
        with region_cols[i]:
            st.metric(row['region'], int(row['Total']), f"Prod {row['Prod %']}%")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Marketing Leads — Region Distribution</div>", unsafe_allow_html=True)
        fig = bar_chart(rg_df, 'region', 'Total', colors=[COLORS['marketing']])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("<div class='section-title'>Productive % by Region</div>", unsafe_allow_html=True)
        fig = bar_chart(
            rg_df.sort_values('Prod %', ascending=True),
            'region', 'Prod %', horizontal=True,
            colors=CHART_COLORS
        )
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-title'>Region-Wise Performance (Marketing Only)</div>", unsafe_allow_html=True)
    st.dataframe(
        rg_df.rename(columns={'region': 'Region'}),
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Region Data",
        data=df_to_excel({'Region Performance': rg_df}),
        file_name=f"Caliber_Region_Performance_{datetime.today().strftime('%Y_%m')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════
# TAB 5 — PRODUCT PERFORMANCE
# ═══════════════════════════════
with tab5:
    st.markdown("""
    <div class='info-box'>
        📌 <b>Marketing Channel Only</b> — Metrics include only leads from Marketing channel
    </div>
    """, unsafe_allow_html=True)

    mkt_df = filtered_df[filtered_df['conversion_source'] == 'Marketing']
    pg_df = breakdown_stats(mkt_df, 'product_group')

    cols = st.columns(min(len(pg_df), 6))
    for i, row in pg_df.iterrows():
        if i < 6:
            with cols[i]:
                st.metric(row['product_group'], int(row['Total']), f"Prod {row['Prod %']}%")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Marketing Leads — Product Distribution</div>", unsafe_allow_html=True)
        fig = bar_chart(pg_df, 'product_group', 'Total', colors=CHART_COLORS[:len(pg_df)])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("<div class='section-title'>Productive % by Product</div>", unsafe_allow_html=True)
        fig = bar_chart(
            pg_df.sort_values('Prod %', ascending=True),
            'product_group', 'Prod %', horizontal=True,
            colors=CHART_COLORS
        )
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-title'>Product-Wise Performance (Marketing Only)</div>", unsafe_allow_html=True)
    st.dataframe(
        pg_df.rename(columns={'product_group': 'Product'}),
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Product Data",
        data=df_to_excel({'Product Performance': pg_df}),
        file_name=f"Caliber_Product_Performance_{datetime.today().strftime('%Y_%m')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════
# TAB 6 — FUNNEL MOVEMENT
# ═══════════════════════════════
with tab6:
    potentials = filtered_df[filtered_df['is_potential'] & (filtered_df['stage'] != '')]

    stage_counts = potentials['stage'].value_counts().reset_index()
    stage_counts.columns = ['Stage', 'Count']

    # KPI row
    stage_order_map = {s: i for i, s in enumerate(STAGE_ORDER)}
    for stage in STAGE_ORDER:
        c = stage_counts[stage_counts['Stage'] == stage]['Count'].values
        count = int(c[0]) if len(c) > 0 else 0

    fc = st.columns(len(STAGE_ORDER))
    for i, stage in enumerate(STAGE_ORDER):
        c = stage_counts[stage_counts['Stage'] == stage]['Count'].values
        count = int(c[0]) if len(c) > 0 else 0
        fc[i].metric(stage.split('/')[0], count)

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Funnel Stage Distribution</div>", unsafe_allow_html=True)
        stage_counts_ordered = stage_counts.copy()
        stage_counts_ordered['order'] = stage_counts_ordered['Stage'].map(
            lambda x: stage_order_map.get(x, 99)
        )
        stage_counts_ordered = stage_counts_ordered.sort_values('order')
        fig = bar_chart(
            stage_counts_ordered, 'Stage', 'Count',
            colors=['#B5D4F4','#3266ad','#BA7517','#D85A30','#993556','#1D9E75'][:len(stage_counts_ordered)],
            horizontal=True
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("<div class='section-title'>Stage Distribution — Donut</div>", unsafe_allow_html=True)
        fig = donut_chart(
            labels=stage_counts_ordered['Stage'].tolist(),
            values=stage_counts_ordered['Count'].tolist(),
            colors=['#B5D4F4','#3266ad','#BA7517','#D85A30','#993556','#1D9E75'][:len(stage_counts_ordered)]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-title'>All Potential Leads — Stage & Channel</div>", unsafe_allow_html=True)
    pot_display = potentials[['full_name','region','product_group','stage','conversion_source','type_of_source']].copy()
    pot_display.columns = ['Name','Region','Product Group','Stage','Channel','Source']
    st.dataframe(pot_display, hide_index=True, use_container_width=True)

    st.download_button(
        "📥 Download Funnel Data",
        data=df_to_excel({'Funnel Movement': pot_display}),
        file_name=f"Caliber_Funnel_{datetime.today().strftime('%Y_%m')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════
# TAB 7 — PERIOD COMPARISON
# ═══════════════════════════════
with tab7:
    if prev_df is None:
        st.markdown("""
        <div class='info-box'>
            💡 Upload a prior month's CSV from the sidebar to activate live period comparison.
        </div>
        """, unsafe_allow_html=True)

    curr_m = compute_metrics(filtered_df)
    prev_m = compute_metrics(prev_df) if prev_df is not None else {
        'total': 0, 'productive': 0, 'unproductive': 0,
        'pursuing': 0, 'converted': 0, 'prod_pct': 0,
        'unprod_pct': 0, 'conv_pct': 0
    }

    label_curr = uploaded_file.name.replace('.csv', '').replace('_', ' ')
    label_prev = prev_file.name.replace('.csv', '').replace('_', ' ') if prev_df is not None else "Prior Period"

    # KPI row with delta
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Leads",    curr_m['total'],      delta=curr_m['total'] - prev_m['total'])
    c2.metric("Productive",     curr_m['productive'],  delta=curr_m['productive'] - prev_m['productive'])
    c3.metric("Unproductive",   curr_m['unproductive'],delta=-(curr_m['unproductive'] - prev_m['unproductive']))
    c4.metric("Converted",      curr_m['converted'],   delta=curr_m['converted'] - prev_m['converted'])
    c5.metric("Conversion %",   f"{curr_m['conv_pct']}%", delta=f"{round(curr_m['conv_pct'] - prev_m['conv_pct'], 1)}%")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # Grouped bar
    st.markdown("<div class='section-title'>Period Comparison — Key Metrics</div>", unsafe_allow_html=True)
    fig = grouped_bar(
        categories=['Total', 'Productive', 'Unproductive', 'Converted', 'Pursuing'],
        datasets=[
            {'name': label_curr,
             'data': [curr_m['total'], curr_m['productive'], curr_m['unproductive'], curr_m['converted'], curr_m['pursuing']],
             'color': '#3266ad'},
            {'name': label_prev,
             'data': [prev_m['total'], prev_m['productive'], prev_m['unproductive'], prev_m['converted'], prev_m['pursuing']],
             'color': '#B4B2A9'},
        ],
        height=320
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    if prev_df is not None:
        comp_df = pd.DataFrame([
            {'Metric': 'Total Leads',    label_curr: curr_m['total'],       label_prev: prev_m['total'],       'Change': curr_m['total'] - prev_m['total']},
            {'Metric': 'Productive',     label_curr: curr_m['productive'],   label_prev: prev_m['productive'],   'Change': curr_m['productive'] - prev_m['productive']},
            {'Metric': 'Productive %',   label_curr: f"{curr_m['prod_pct']}%",  label_prev: f"{prev_m['prod_pct']}%",  'Change': f"{round(curr_m['prod_pct'] - prev_m['prod_pct'],1)}%"},
            {'Metric': 'Unproductive',   label_curr: curr_m['unproductive'], label_prev: prev_m['unproductive'], 'Change': curr_m['unproductive'] - prev_m['unproductive']},
            {'Metric': 'Unprod %',       label_curr: f"{curr_m['unprod_pct']}%", label_prev: f"{prev_m['unprod_pct']}%", 'Change': f"{round(curr_m['unprod_pct'] - prev_m['unprod_pct'],1)}%"},
            {'Metric': 'Converted',      label_curr: curr_m['converted'],    label_prev: prev_m['converted'],    'Change': curr_m['converted'] - prev_m['converted']},
            {'Metric': 'Conversion %',   label_curr: f"{curr_m['conv_pct']}%",  label_prev: f"{prev_m['conv_pct']}%",  'Change': f"{round(curr_m['conv_pct'] - prev_m['conv_pct'],1)}%"},
        ])
        st.dataframe(comp_df, hide_index=True, use_container_width=True)

        st.download_button(
            "📥 Download Comparison Report",
            data=df_to_excel({'Period Comparison': comp_df}),
            file_name=f"Caliber_Comparison_{datetime.today().strftime('%Y_%m')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
