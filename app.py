
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io, base64
 
# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Caliber Lead Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ─── Caliber logo embedded (no upload needed) ───────────────────────────────
CALIBER_LOGO_B64 = "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"
 
# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{ font-family:'Inter',sans-serif; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    color: white !important;
}
.main .block-container{ padding-top:1rem; padding-bottom:2rem; max-width:1400px; }
 
.logo-bar{
    display:flex; align-items:center; gap:14px;
    padding-bottom:14px; border-bottom:1px solid #eee; margin-bottom:18px;
}
.logo-bar img{ height:44px; object-fit:contain; }
.logo-bar h1{ font-size:20px; font-weight:700; color:#1a1a1a; margin:0; }
.logo-bar .month-badge{
    margin-left:auto; background:#E1F5EE; color:#0F6E56;
    padding:5px 14px; border-radius:20px; font-size:11px; font-weight:600;
}
 
[data-testid="stSidebar"]{ background:#1E293B; }
[data-testid="stSidebar"] *{ color:#E2E8F0 !important; }
[data-testid="stSidebar"] label{
    color:#94A3B8 !important; font-size:11px !important;
    text-transform:uppercase; letter-spacing:.05em; font-weight:600;
}
 
div[data-testid="metric-container"]{
    background:#F8F9FA; border:0.5px solid #EBEBEB; border-radius:10px; padding:14px 18px;
}
div[data-testid="metric-container"] label{
    font-size:10px !important; text-transform:uppercase;
    letter-spacing:.06em; color:#888 !important; font-weight:600;
}
div[data-testid="metric-container"] [data-testid="metric-value"]{
    font-size:26px !important; font-weight:700 !important; color:#1a1a1a !important;
}
 
.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid #eee; }
.stTabs [data-baseweb="tab"]{
    font-size:12px; font-weight:500; padding:8px 14px;
    border-radius:4px 4px 0 0; color:#888;
}
.stTabs [aria-selected="true"]{
    color:#3266ad !important; font-weight:600;
    background:white !important; border-bottom:2px solid #3266ad !important;
}
 
.section-title{
    font-size:13px; font-weight:600; color:#1a1a1a;
    margin-bottom:10px; padding-bottom:6px; border-bottom:.5px solid #eee;
}
.info-box{
    background:#F0F7FF; border:.5px solid #C3DCFB; border-radius:8px;
    padding:10px 14px; font-size:12px; color:#185FA5; margin-bottom:14px;
}
 
/* Insight cards */
.insight-grid{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px; }
.insight-card{
    flex:1; min-width:200px; border-radius:10px; padding:12px 14px;
    border-left:4px solid; font-size:12px; line-height:1.5;
}
.insight-good { background:#F0FBF7; border-color:#1D9E75; }
.insight-warn { background:#FEF9EC; border-color:#BA7517; }
.insight-bad  { background:#FEF0F0; border-color:#D85A30; }
.insight-info { background:#F0F7FF; border-color:#3266ad; }
.insight-icon { font-size:16px; margin-bottom:4px; }
.insight-title{ font-weight:700; font-size:12px; margin-bottom:3px; }
.insight-text { color:#555; font-size:11px; }
 
hr.subtle{ border:none; border-top:.5px solid #eee; margin:14px 0; }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
PRODUCTIVE_STATUSES   = ['Contacted - Interested','Meeting Schedule',
                          'Budget Constraint','Deferred Interest']
UNPRODUCTIVE_STATUSES = ['Contacted - Irrelevant','Knowledge / Job - Irrelevant',
                          'Contacted - Not Interested','Already In - Funnel','Unresponsive']
COLORS = {
    'productive':'#3266ad','unproductive':'#D85A30','converted':'#1D9E75',
    'pursuing':'#BA7517','business':'#185FA5','marketing':'#1D9E75','neutral':'#B4B2A9',
}
CHART_COLORS = ['#3266ad','#1D9E75','#D85A30','#BA7517','#8B5CF6','#0F6E56','#993556','#185FA5']
STAGE_ORDER  = ['Discovery/Teaser Demo','Demo','Technical Evaluation',
                'Negotiation/Review','CP wrt SOW','Closed Won']
CHART_LAYOUT = dict(
    font_family='Inter', plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(l=10,r=10,t=30,b=10),
    legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1),
    height=280,
)
 
# ─────────────────────────────────────────
# INSIGHT HELPER
# ─────────────────────────────────────────
def insight_card(icon, title, text, kind='info'):
    return f"""
    <div class="insight-card insight-{kind}">
        <div class="insight-icon">{icon}</div>
        <div class="insight-title">{title}</div>
        <div class="insight-text">{text}</div>
    </div>"""
 
def show_insights(cards_html: list):
    st.markdown(
        '<div class="insight-grid">' + ''.join(cards_html) + '</div>',
        unsafe_allow_html=True
    )
 
# ─────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────
def normalize_region(r):
    if not r or str(r).strip() in ('','nan'): return 'Unknown'
    r = str(r).strip()
    if any(x in r for x in ['Guj','Gujarat','North']): return 'Guj & North'
    if 'South'   in r: return 'South'
    if any(x in r for x in ['Maharashtra','Goa','Mah']): return 'Mah & Goa'
    if 'APAC'    in r: return 'APAC'
    if 'MENA'    in r: return 'MENA'
    return r
 
def normalize_product(p):
    if not p or str(p).strip() in ('','nan'): return 'Unknown'
    p = str(p).strip()
    if any(x in p for x in ['D&I','DSG','D & I']): return 'D&I / DSG'
    if ';' in p: return p.split(';')[0].strip()
    return p
 
def pct(num, den, d=1):
    return round(num/den*100, d) if den > 0 else 0.0
 
def compute_metrics(df):
    total        = len(df)
    productive   = int(df['is_productive'].sum()) + int(df['is_potential'].sum())
    unproductive = int(df['is_unproductive'].sum())
    pursuing     = int(df['is_pursuing'].sum())
    converted    = int(df['is_potential'].sum())
    return dict(total=total, productive=productive, unproductive=unproductive,
                pursuing=pursuing, converted=converted,
                prod_pct=pct(productive,total),
                unprod_pct=pct(unproductive,total),
                conv_pct=pct(converted,productive))
 
def breakdown_stats(df, col):
    rows = []
    for val in df[col].unique():
        sub = df[df[col]==val]
        m   = compute_metrics(sub)
        rows.append({col:val,'Total':m['total'],'Productive':m['productive'],
                     'Prod %':m['prod_pct'],'Unproductive':m['unproductive'],
                     'Unprod %':m['unprod_pct'],'Converted':m['converted'],
                     'Conv %':m['conv_pct']})
    return pd.DataFrame(rows).sort_values('Total',ascending=False).reset_index(drop=True)
 
def df_to_excel(sheets:dict):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf,engine='openpyxl') as w:
        for name,df in sheets.items():
            df.to_excel(w,sheet_name=name[:31],index=False)
    return buf.getvalue()
 
# ─────────────────────────────────────────
# LOAD EXCEL
# ─────────────────────────────────────────
def load_excel(file) -> pd.DataFrame:

    xl = pd.ExcelFile(file)

    # ---------- LEAD SHEET ----------
    lead_col_map = {
        'full name': 'full_name',
        'name': 'full_name',
        'company': 'company',
        'region': 'region',
        'territory': 'region',
        'product group': 'product_group',
        'product': 'product_group',
        'lead status': 'lead_status',
        'status': 'lead_status',
        'type of source': 'type_of_source',
        'source': 'type_of_source',
        'conversion source': 'conversion_source',
        'channel': 'conversion_source',
        'created time': 'created_time',
        'date': 'created_time',
    }

    lead_df = xl.parse(sheet_name=0, dtype=str).fillna('')

    lead_df.columns = [
        str(c).strip().lower()
        for c in lead_df.columns
    ]

    lead_df.columns = [
        lead_col_map[c] if c in lead_col_map else c
        for c in lead_df.columns
    ]

    lead_df = lead_df.loc[:, ~pd.Index(lead_df.columns).duplicated()]

    lead_df['sheet'] = 'Lead'
    lead_df['stage'] = ''

    if 'full_name' not in lead_df.columns:
        lead_df['full_name'] = ''

    # ---------- POTENTIAL SHEET ----------
    pot_col_map = {
        'potential name': 'full_name',
        'account name': 'full_name',
        'name': 'full_name',
        'region': 'region',
        'product group': 'product_group',
        'prod category': 'product_group',
        'stage': 'stage',
        'pipeline stage': 'stage',
        'type of source': 'type_of_source',
        'conversion source': 'conversion_source',
        'created time': 'created_time',
    }

    pot_df = xl.parse(sheet_name=1, dtype=str).fillna('')

    pot_df.columns = [
        str(c).strip().lower()
        for c in pot_df.columns
    ]

    pot_df.columns = [
        pot_col_map[c] if c in pot_col_map else c
        for c in pot_df.columns
    ]

    pot_df = pot_df.loc[:, ~pd.Index(pot_df.columns).duplicated()]

    pot_df['sheet'] = 'Potential'
    pot_df['lead_status'] = ''

    # ---------- REQUIRED COLUMNS ----------
    required = [
        'full_name',
        'region',
        'product_group',
        'lead_status',
        'type_of_source',
        'conversion_source',
        'created_time',
        'stage',
        'sheet'
    ]

    for col in required:
        if col not in lead_df.columns:
            lead_df[col] = ''

        if col not in pot_df.columns:
            pot_df[col] = ''

    # ---------- COMBINE ----------
    df = pd.concat(
        [
            lead_df[required],
            pot_df[required]
        ],
        ignore_index=True
    )

    # ---------- CLEAN ----------
    df['region'] = df['region'].apply(normalize_region)

    df['product_group'] = df['product_group'].apply(normalize_product)

    # ---------- FLAGS ----------
    df['is_productive'] = df['lead_status'].isin(PRODUCTIVE_STATUSES)

    df['is_unproductive'] = df['lead_status'].isin(UNPRODUCTIVE_STATUSES)

    df['is_pursuing'] = df['lead_status'] == 'Pursuing'

    df['is_potential'] = df['sheet'] == 'Potential'

    return df
 
# ─────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────
def bar_chart(df,x,y,title='',horizontal=False,colors=None,height=280):
    kw = dict(text_auto=True,title=title,color_discrete_sequence=colors or CHART_COLORS)
    if horizontal:
        fig = px.bar(df,x=y,y=x,orientation='h',**kw)
        fig.update_xaxes(showgrid=True,gridcolor='#F0F0F0',zeroline=False)
        fig.update_yaxes(showgrid=False)
    else:
        fig = px.bar(df,x=x,y=y,**kw)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True,gridcolor='#F0F0F0',zeroline=False)
    fig.update_traces(textfont_size=10,textposition='outside')
    fig.update_layout(**{**CHART_LAYOUT,'height':height})
    return fig
 
def donut_chart(labels,values,colors=None,height=260):
    fig = go.Figure(go.Pie(
        labels=labels,values=values,hole=0.62,
        marker_colors=colors or CHART_COLORS,
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
    ))
    fig.update_layout(**{**CHART_LAYOUT,'height':height,'showlegend':True})
    return fig
 
def grouped_bar(categories,datasets,title='',height=300):
    fig = go.Figure()
    for ds in datasets:
        fig.add_trace(go.Bar(
            name=ds['name'],x=categories,y=ds['data'],
            marker_color=ds['color'],
            text=ds['data'],textposition='outside',textfont_size=10
        ))
    fig.update_layout(**{**CHART_LAYOUT,'height':height,'title':title,'barmode':'group'})
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True,gridcolor='#F0F0F0',zeroline=False)
    return fig
 
def trend_line(months,datasets,title='',height=320,pct_axis=False):
    fig = go.Figure()
    palette=['#3266ad','#1D9E75','#D85A30','#BA7517','#8B5CF6']
    for i,ds in enumerate(datasets):
        fig.add_trace(go.Scatter(
            x=months,y=ds['data'],mode='lines+markers+text',
            name=ds['name'],line=dict(color=palette[i%len(palette)],width=2.5),
            marker=dict(size=8),text=ds['data'],
            textposition='top center',textfont_size=10
        ))
    fig.update_layout(**{**CHART_LAYOUT,'height':height,'title':title,'hovermode':'x unified'})
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True,gridcolor='#F0F0F0',zeroline=False,
                     ticksuffix='%' if pct_axis else '')
    return fig
 
# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Lead Analytics")
    st.markdown("---")
    st.markdown("### Monthly Data")
    uploaded_files = st.file_uploader(
        "Upload Excel files (.xlsx)",type=['xlsx'],
        accept_multiple_files=True,
        help="Upload one or more monthly Zoho CRM Excel exports. Each must have Lead and Potential sheets."
    )
    st.markdown("---")
    if uploaded_files:
        st.markdown("### Filters")
        region_filter  = st.multiselect("Region",['Guj & North','South','Mah & Goa','APAC','MENA'],
                                         default=[],placeholder="All regions")
        channel_filter = st.selectbox("Channel",["All","Business","Marketing"])
    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#64748B;line-height:1.8;'>
    <b>Formulas</b><br>
    Productive = Interested + Meeting + Budget + Deferred + Potential<br>
    Unproductive = Not Interested + Irrelevant + Job/Knowledge + Unresponsive + In Funnel<br>
    Conversion % = Potential / Productive
    </div>""",unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# WELCOME SCREEN
# ─────────────────────────────────────────
if not uploaded_files:
    st.markdown(f"""
    <div style='text-align:center;padding:50px 20px;'>
        <img src="data:image/jpeg;base64,{CALIBER_LOGO_B64}" style='height:60px;margin-bottom:20px;'>
        <h2 style='font-size:22px;font-weight:700;color:#1a1a1a;margin-bottom:8px;'>
            Lead Analytics Dashboard
        </h2>
        <p style='font-size:13px;color:#888;max-width:440px;margin:0 auto 24px;'>
            Upload your monthly Zoho CRM Excel export from the sidebar.
            Supports multiple months for trend analysis.
        </p>
        <div style='display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:20px;'>
            <div style='background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;'>
                <div style='font-size:20px;'>⬆️</div>
                <div style='font-size:12px;font-weight:600;margin-top:6px;'>Upload Excel</div>
                <div style='font-size:11px;color:#888;'>Lead + Potential sheets</div>
            </div>
            <div style='background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;'>
                <div style='font-size:20px;'>📊</div>
                <div style='font-size:12px;font-weight:600;margin-top:6px;'>Auto Dashboard</div>
                <div style='font-size:11px;color:#888;'>All 7 tabs fill instantly</div>
            </div>
            <div style='background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;'>
                <div style='font-size:20px;'>💡</div>
                <div style='font-size:12px;font-weight:600;margin-top:6px;'>Smart Insights</div>
                <div style='font-size:11px;color:#888;'>Auto alerts & trends</div>
            </div>
            <div style='background:#F8F9FA;border-radius:8px;padding:16px 20px;min-width:130px;'>
                <div style='font-size:20px;'>📥</div>
                <div style='font-size:12px;font-weight:600;margin-top:6px;'>Download</div>
                <div style='font-size:11px;color:#888;'>Excel or PDF report</div>
            </div>
        </div>
    </div>""",unsafe_allow_html=True)
    st.stop()
 
# ─────────────────────────────────────────
# LOAD FILES
# ─────────────────────────────────────────
monthly_data = {}
for f in uploaded_files:
    label = f.name.replace('.xlsx','').replace('_',' ').replace('-',' ').strip()
    try:
        monthly_data[label] = load_excel(f)
    except Exception as e:
        st.error(f"⚠️ {f.name}: {e}")
 
if not monthly_data:
    st.warning("No valid files loaded. Each Excel must have 'Lead' and 'Potential' sheets.")
    st.stop()
 
month_labels  = sorted(monthly_data.keys(),reverse=True)
current_label = month_labels[0]
df_current    = monthly_data[current_label]
 
def apply_filters(df):
    out = df.copy()
    if 'region_filter' in dir() and region_filter:
        out = out[out['region'].isin(region_filter)]
    if 'channel_filter' in dir() and channel_filter != 'All':
        out = out[out['conversion_source']==channel_filter]
    return out
 
filtered = apply_filters(df_current)
m        = compute_metrics(filtered)
 
# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="logo-bar">
    <img src="data:image/jpeg;base64,{CALIBER_LOGO_B64}" alt="Caliber Logo">
    <h1>Lead Analytics Dashboard</h1>
    <span class="month-badge">{current_label} &nbsp;·&nbsp; {m['total']} leads</span>
</div>""",unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
    "📋 Overview","📡 Channel Performance","🔗 Source Performance",
    "🗺️ Region Performance","📦 Product Performance",
    "🔄 Funnel Movement","📅 Period Comparison"
])
 
# ════════════════════════════════════════════
# TAB 1  OVERVIEW
# ════════════════════════════════════════════
with tab1:
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total Leads",  m['total'])
    c2.metric("Productive",   m['productive'],  f"{m['prod_pct']}%")
    c3.metric("Unproductive", m['unproductive'], f"-{m['unprod_pct']}%")
    c4.metric("Pursuing",     m['pursuing'])
    c5.metric("Converted",    m['converted'])
    c6.metric("Conversion %", f"{m['conv_pct']}%")
 
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    # ── Smart insights ─────────────────────────────────────────────────
    st.markdown("<div class='section-title'>💡 Key Insights</div>",unsafe_allow_html=True)
    cards = []
    if m['unprod_pct'] > 50:
        cards.append(insight_card("🔴","High Unproductive Rate",
            f"{m['unprod_pct']}% of leads are unproductive — review lead quality from top sources.","bad"))
    elif m['unprod_pct'] > 35:
        cards.append(insight_card("🟡","Moderate Unproductive Rate",
            f"{m['unprod_pct']}% unproductive. Consider refining targeting criteria.","warn"))
    else:
        cards.append(insight_card("🟢","Good Lead Quality",
            f"Only {m['unprod_pct']}% unproductive leads. Keep up the quality targeting!","good"))
 
    if m['conv_pct'] >= 80:
        cards.append(insight_card("🏆","Strong Conversion Rate",
            f"{m['conv_pct']}% conversion from productive to potential. Excellent pipeline health!","good"))
    elif m['conv_pct'] >= 50:
        cards.append(insight_card("📈","Healthy Conversion",
            f"{m['conv_pct']}% conversion rate. Scope to improve further through follow-ups.","info"))
    else:
        cards.append(insight_card("⚠️","Low Conversion Rate",
            f"Only {m['conv_pct']}% productive leads converting. Review engagement quality.","bad"))
 
    biz_count = filtered[filtered['conversion_source']=='Business'].shape[0]
    mkt_count = filtered[filtered['conversion_source']=='Marketing'].shape[0]
    if mkt_count > 0:
        biz_pct_share = pct(biz_count, m['total'])
        if biz_pct_share < 20:
            cards.append(insight_card("📌","Business Channel Underrepresented",
                f"Business leads are only {biz_pct_share}% of total. Strong marketing volume but lower conversion rate.","warn"))
        else:
            cards.append(insight_card("✅","Balanced Channel Mix",
                f"Business {biz_pct_share}% | Marketing {100-biz_pct_share}% — healthy mix between channels.","good"))
 
    if m['pursuing'] > 0:
        cards.append(insight_card("🔄","Active Pursuing Leads",
            f"{m['pursuing']} leads in Pursuing stage — prioritise follow-ups to move them to productive.","info"))
 
    show_insights(cards)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Lead Quality Distribution</div>",unsafe_allow_html=True)
        prod_only = max(m['productive']-m['converted'],0)
        fig = donut_chart(
            ['Converted','Productive','Unproductive','Pursuing'],
            [m['converted'],prod_only,m['unproductive'],m['pursuing']],
            colors=[COLORS['converted'],COLORS['productive'],COLORS['unproductive'],COLORS['pursuing']]
        )
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    with col2:
        st.markdown("<div class='section-title'>Conversion Contribution by Channel</div>",unsafe_allow_html=True)
        biz_c = filtered[(filtered['conversion_source']=='Business')&filtered['is_potential']].shape[0]
        mkt_c = filtered[(filtered['conversion_source']=='Marketing')&filtered['is_potential']].shape[0]
        fig = donut_chart(['Business','Marketing'],[biz_c,mkt_c],
                          colors=[COLORS['business'],COLORS['marketing']])
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
 
    st.markdown("<div class='section-title'>Unproductive Lead Breakdown</div>",unsafe_allow_html=True)
    ub = filtered[filtered['is_unproductive']]['lead_status'].value_counts().reset_index()
    ub.columns = ['Status','Count']
    ub['Status'] = ub['Status'].str.replace('Contacted - ','').str.replace('Knowledge / ','')
    fig = bar_chart(ub,'Status','Count',horizontal=True,
                    colors=['#F09595','#ED93B1','#EF9F27','#AFA9EC','#B4B2A9'],height=180)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
 
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
    st.download_button("📥 Download Full Report (Excel)",
        data=df_to_excel({'Data':filtered[['full_name','region','product_group',
                                            'lead_status','type_of_source','conversion_source','stage']]}),
        file_name=f"Caliber_Report_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
# ════════════════════════════════════════════
# TAB 2  CHANNEL PERFORMANCE
# ════════════════════════════════════════════
with tab2:
    biz_m = compute_metrics(filtered[filtered['conversion_source']=='Business'])
    mkt_m = compute_metrics(filtered[filtered['conversion_source']=='Marketing'])
 
    # Insights
    cards = []
    if biz_m['conv_pct'] > mkt_m['conv_pct']:
        gap = round(biz_m['conv_pct']-mkt_m['conv_pct'],1)
        cards.append(insight_card("💼","Business Channel Converts Better",
            f"Business conversion is {biz_m['conv_pct']}% vs Marketing {mkt_m['conv_pct']}% — {gap}% gap. Business leads are higher quality.","good"))
    if mkt_m['unprod_pct'] > 60:
        cards.append(insight_card("⚠️","Marketing Unproductive Rate is High",
            f"{mkt_m['unprod_pct']}% of marketing leads are unproductive. Review campaign targeting and lead qualification criteria.","bad"))
    if mkt_m['total'] > biz_m['total']*2:
        cards.append(insight_card("📣","Marketing Driving Volume",
            f"Marketing brings {mkt_m['total']} leads vs Business {biz_m['total']}. High volume but needs quality improvement.","info"))
    show_insights(cards)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>🔵 Business Channel</div>",unsafe_allow_html=True)
        b1,b2,b3,b4 = st.columns(4)
        b1.metric("Total",       biz_m['total'])
        b2.metric("Productive",  biz_m['productive'],  f"{biz_m['prod_pct']}%")
        b3.metric("Unproductive",biz_m['unproductive'])
        b4.metric("Converted",   biz_m['converted'],   f"Conv {biz_m['conv_pct']}%")
        biz_st = (filtered[filtered['conversion_source']=='Business']['lead_status']
                  .value_counts().reset_index())
        biz_st.columns=['Status','Count']
        st.dataframe(biz_st,hide_index=True,use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>🟢 Marketing Channel</div>",unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Total",       mkt_m['total'])
        m2.metric("Productive",  mkt_m['productive'],  f"{mkt_m['prod_pct']}%")
        m3.metric("Unproductive",mkt_m['unproductive'])
        m4.metric("Converted",   mkt_m['converted'],   f"Conv {mkt_m['conv_pct']}%")
        mkt_st = (filtered[filtered['conversion_source']=='Marketing']['lead_status']
                  .value_counts().reset_index())
        mkt_st.columns=['Status','Count']
        st.dataframe(mkt_st,hide_index=True,use_container_width=True)
 
    st.markdown("<div class='section-title'>Side-by-Side Comparison</div>",unsafe_allow_html=True)
    fig = grouped_bar(
        ['Total','Productive','Unproductive','Converted'],
        [{'name':'Business','data':[biz_m['total'],biz_m['productive'],biz_m['unproductive'],biz_m['converted']],'color':COLORS['business']},
         {'name':'Marketing','data':[mkt_m['total'],mkt_m['productive'],mkt_m['unproductive'],mkt_m['converted']],'color':COLORS['marketing']}])
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    ch_df = pd.DataFrame([{'Channel':'Business',**biz_m},{'Channel':'Marketing',**mkt_m}])
    st.download_button("📥 Download Channel Data",
        data=df_to_excel({'Channel Performance':ch_df}),
        file_name=f"Caliber_Channel_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
# ════════════════════════════════════════════
# TAB 3  SOURCE PERFORMANCE
# ════════════════════════════════════════════
with tab3:
    src_df = (filtered.groupby('type_of_source')
              .agg(Total=('type_of_source','count'),
                   Productive=('is_productive','sum'),
                   Unproductive=('is_unproductive','sum'),
                   Pursuing=('is_pursuing','sum'))
              .reset_index().rename(columns={'type_of_source':'Source'})
              .sort_values('Total',ascending=False))
    src_df['Prod %']   = src_df.apply(lambda r:pct(r['Productive'],r['Total']),axis=1)
    src_df['Unprod %'] = src_df.apply(lambda r:pct(r['Unproductive'],r['Total']),axis=1)
 
    # Insights
    cards = []
    if len(src_df) > 0:
        best_src = src_df.sort_values('Prod %',ascending=False).iloc[0]
        worst_src = src_df.sort_values('Unprod %',ascending=False).iloc[0]
        top_vol   = src_df.iloc[0]
        cards.append(insight_card("🌟","Best Quality Source",
            f"<b>{best_src['Source']}</b> has the highest productive rate at {best_src['Prod %']}%. Prioritise and scale this source.","good"))
        if worst_src['Unprod %'] > 60:
            cards.append(insight_card("🔴","Highest Unproductive Source",
                f"<b>{worst_src['Source']}</b> has {worst_src['Unprod %']}% unproductive leads. Review or reduce investment in this channel.","bad"))
        if top_vol['Source'] != best_src['Source']:
            cards.append(insight_card("📊","Volume vs Quality Gap",
                f"<b>{top_vol['Source']}</b> drives most volume ({top_vol['Total']} leads) but <b>{best_src['Source']}</b> gives better quality. Balance strategy.","warn"))
    show_insights(cards)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    cols = st.columns(min(len(src_df),5))
    for i,(_,row) in enumerate(src_df.head(5).iterrows()):
        cols[i].metric(row['Source'],int(row['Total']),f"Prod {row['Prod %']}%")
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Lead Volume by Source</div>",unsafe_allow_html=True)
        fig = donut_chart(src_df['Source'].tolist(),src_df['Total'].tolist(),colors=CHART_COLORS)
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    with col2:
        st.markdown("<div class='section-title'>Productive % by Source</div>",unsafe_allow_html=True)
        fig = bar_chart(src_df.sort_values('Prod %'),'Source','Prod %',
                        horizontal=True,colors=CHART_COLORS)
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
 
    st.markdown("<div class='section-title'>Detailed View</div>",unsafe_allow_html=True)
    st.dataframe(src_df[['Source','Total','Productive','Prod %','Unproductive','Unprod %','Pursuing']],
                 hide_index=True,use_container_width=True)
    st.download_button("📥 Download Source Data",
        data=df_to_excel({'Source Performance':src_df}),
        file_name=f"Caliber_Source_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
# ════════════════════════════════════════════
# TAB 4  REGION PERFORMANCE
# ════════════════════════════════════════════
with tab4:
    st.markdown("<div class='info-box'>📌 <b>Marketing Channel Only</b></div>",unsafe_allow_html=True)
    mkt_df = filtered[filtered['conversion_source']=='Marketing']
    rg_df  = breakdown_stats(mkt_df,'region')
 
    # Insights
    cards = []
    if len(rg_df) > 0:
        best_rg  = rg_df.sort_values('Prod %',ascending=False).iloc[0]
        worst_rg = rg_df.sort_values('Unprod %',ascending=False).iloc[0]
        top_rg   = rg_df.iloc[0]
        cards.append(insight_card("🌍","Best Performing Region",
            f"<b>{best_rg['region']}</b> leads in productive rate ({best_rg['Prod %']}%). Focus campaigns here for better ROI.","good"))
        if worst_rg['Unprod %'] > 70:
            cards.append(insight_card("🔴","Region Needs Attention",
                f"<b>{worst_rg['region']}</b> has {worst_rg['Unprod %']}% unproductive leads. Review lead sources and targeting for this region.","bad"))
        cards.append(insight_card("📍","Highest Volume Region",
            f"<b>{top_rg['region']}</b> brings the most leads ({top_rg['Total']}). Ensure quality is maintained while scaling volume.","info"))
    show_insights(cards)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    cols = st.columns(min(len(rg_df),5))
    for i,(_,row) in enumerate(rg_df.head(5).iterrows()):
        cols[i].metric(row['region'],int(row['Total']),f"Prod {row['Prod %']}%")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Region Distribution</div>",unsafe_allow_html=True)
        fig = bar_chart(rg_df,'region','Total',colors=[COLORS['marketing']])
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    with col2:
        st.markdown("<div class='section-title'>Productive % by Region</div>",unsafe_allow_html=True)
        fig = bar_chart(rg_df.sort_values('Prod %'),'region','Prod %',
                        horizontal=True,colors=CHART_COLORS)
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    st.markdown("<div class='section-title'>Region-Wise Performance</div>",unsafe_allow_html=True)
    st.dataframe(rg_df.rename(columns={'region':'Region'}),hide_index=True,use_container_width=True)
    st.download_button("📥 Download Region Data",
        data=df_to_excel({'Region Performance':rg_df}),
        file_name=f"Caliber_Region_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
# ════════════════════════════════════════════
# TAB 5  PRODUCT PERFORMANCE
# ════════════════════════════════════════════
with tab5:
    st.markdown("<div class='info-box'>📌 <b>Marketing Channel Only</b></div>",unsafe_allow_html=True)
    mkt_df = filtered[filtered['conversion_source']=='Marketing']
    pg_df  = breakdown_stats(mkt_df,'product_group')
 
    # Insights
    cards = []
    if len(pg_df) > 0:
        best_pg  = pg_df.sort_values('Conv %',ascending=False).iloc[0]
        worst_pg = pg_df[pg_df['Total']>1].sort_values('Unprod %',ascending=False).iloc[0] if len(pg_df[pg_df['Total']>1])>0 else None
        top_pg   = pg_df.iloc[0]
        cards.append(insight_card("🏅","Highest Conversion Product",
            f"<b>{best_pg['product_group']}</b> has {best_pg['Conv %']}% conversion rate. This product resonates best with marketing leads.","good"))
        if worst_pg is not None and worst_pg['Unprod %'] > 70:
            cards.append(insight_card("📦","Product Needs Lead Quality Improvement",
                f"<b>{worst_pg['product_group']}</b> — {worst_pg['Unprod %']}% unproductive. Marketing messaging for this product may need revision.","warn"))
        cards.append(insight_card("📈","Highest Volume Product",
            f"<b>{top_pg['product_group']}</b> attracts the most marketing leads ({top_pg['Total']}). Ensure follow-up capacity matches demand.","info"))
    show_insights(cards)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    cols = st.columns(min(len(pg_df),6))
    for i,(_,row) in enumerate(pg_df.head(6).iterrows()):
        cols[i].metric(row['product_group'],int(row['Total']),f"Prod {row['Prod %']}%")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Product Distribution</div>",unsafe_allow_html=True)
        fig = bar_chart(pg_df,'product_group','Total',colors=CHART_COLORS[:len(pg_df)])
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    with col2:
        st.markdown("<div class='section-title'>Productive % by Product</div>",unsafe_allow_html=True)
        fig = bar_chart(pg_df.sort_values('Prod %'),'product_group','Prod %',
                        horizontal=True,colors=CHART_COLORS)
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    st.markdown("<div class='section-title'>Product-Wise Performance</div>",unsafe_allow_html=True)
    st.dataframe(pg_df.rename(columns={'product_group':'Product'}),hide_index=True,use_container_width=True)
    st.download_button("📥 Download Product Data",
        data=df_to_excel({'Product Performance':pg_df}),
        file_name=f"Caliber_Product_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
# ════════════════════════════════════════════
# TAB 6  FUNNEL MOVEMENT
# ════════════════════════════════════════════
with tab6:
    potentials = filtered[filtered['is_potential']&(filtered['stage']!='')]
    sc = potentials['stage'].value_counts().reset_index()
    sc.columns = ['Stage','Count']
 
    # Insights
    cards = []
    total_pot = len(potentials)
    if total_pot > 0:
        demo_cnt = sc[sc['Stage'].str.contains('Demo',na=False)]['Count'].sum()
        negot_cnt= sc[sc['Stage'].str.contains('Negot',na=False)]['Count'].sum()
        won_cnt  = sc[sc['Stage']=='Closed Won']['Count'].sum() if 'Closed Won' in sc['Stage'].values else 0
        if demo_cnt > 0:
            demo_pct = pct(demo_cnt,total_pot)
            cards.append(insight_card("📋","Leads Concentrated in Demo Stage",
                f"{demo_cnt} leads ({demo_pct}%) are in Demo stage. Strong demo pipeline — ensure capacity to move them forward.","info"))
        if negot_cnt > 0:
            cards.append(insight_card("🤝","Leads in Negotiation",
                f"{negot_cnt} leads in Negotiation/Review — these are close to conversion. Prioritise attention here.","good"))
        if won_cnt > 0:
            cards.append(insight_card("🏆","Closed Won This Period",
                f"{won_cnt} deal(s) closed this period. Great outcome!","good"))
        early_stage = sc[sc['Stage'].isin(['Discovery/Teaser Demo','Demo'])]['Count'].sum()
        late_stage  = sc[sc['Stage'].isin(['Negotiation/Review','CP wrt SOW','Closed Won'])]['Count'].sum()
        if early_stage > late_stage*2:
            cards.append(insight_card("⚠️","Funnel Top-Heavy",
                f"Most leads are in early stages ({early_stage} early vs {late_stage} late). Focus on moving deals through mid-funnel.","warn"))
    show_insights(cards)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    fc = st.columns(len(STAGE_ORDER))
    for i,stage in enumerate(STAGE_ORDER):
        cnt = sc[sc['Stage']==stage]['Count'].values
        fc[i].metric(stage.split('/')[0],int(cnt[0]) if len(cnt) else 0)
    st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Stage Distribution</div>",unsafe_allow_html=True)
        order_map = {s:i for i,s in enumerate(STAGE_ORDER)}
        sc['order'] = sc['Stage'].map(lambda x:order_map.get(x,99))
        sc_ord = sc.sort_values('order')
        colors_stage=['#B5D4F4','#3266ad','#BA7517','#D85A30','#993556','#1D9E75']
        fig = bar_chart(sc_ord,'Stage','Count',horizontal=True,
                        colors=colors_stage[:len(sc_ord)])
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    with col2:
        st.markdown("<div class='section-title'>Stage Donut</div>",unsafe_allow_html=True)
        fig = donut_chart(sc_ord['Stage'].tolist(),sc_ord['Count'].tolist(),
                          colors=colors_stage[:len(sc_ord)])
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
 
    st.markdown("<div class='section-title'>All Potential Leads</div>",unsafe_allow_html=True)
    pot_show = potentials[['full_name','region','product_group','stage','conversion_source']].copy()
    pot_show.columns=['Name','Region','Product','Stage','Channel']
    st.dataframe(pot_show,hide_index=True,use_container_width=True)
    st.download_button("📥 Download Funnel Data",
        data=df_to_excel({'Funnel':pot_show}),
        file_name=f"Caliber_Funnel_{current_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
# ════════════════════════════════════════════
# TAB 7  PERIOD COMPARISON + TRENDS
# ════════════════════════════════════════════
with tab7:
    if len(monthly_data) < 2:
        st.markdown("""
        <div class='info-box'>
        💡 <b>Upload more monthly files to activate trend analysis.</b><br>
        From the sidebar, select and upload 2 or more monthly Excel files together.
        All months will appear as trend lines automatically.
        </div>""",unsafe_allow_html=True)
 
    summary_rows = []
    for label in sorted(monthly_data.keys()):
        mm = compute_metrics(monthly_data[label])
        summary_rows.append({'Month':label,'Total':mm['total'],
            'Productive':mm['productive'],'Prod %':mm['prod_pct'],
            'Unproductive':mm['unproductive'],'Unprod %':mm['unprod_pct'],
            'Converted':mm['converted'],'Conv %':mm['conv_pct'],'Pursuing':mm['pursuing']})
    summary = pd.DataFrame(summary_rows)
    months  = summary['Month'].tolist()
 
    # KPI delta
    if len(summary) >= 2:
        curr_r = summary.iloc[-1]; prev_r = summary.iloc[-2]
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Leads",  int(curr_r['Total']),      int(curr_r['Total']-prev_r['Total']))
        c2.metric("Productive",   int(curr_r['Productive']),  int(curr_r['Productive']-prev_r['Productive']))
        c3.metric("Unproductive", int(curr_r['Unproductive']),int(-(curr_r['Unproductive']-prev_r['Unproductive'])))
        c4.metric("Converted",    int(curr_r['Converted']),   int(curr_r['Converted']-prev_r['Converted']))
        c5.metric("Conversion %", f"{curr_r['Conv %']}%",     f"{round(curr_r['Conv %']-prev_r['Conv %'],1)}%")
 
        # Trend insights
        cards = []
        tot_trend = int(curr_r['Total']-prev_r['Total'])
        conv_trend= round(curr_r['Conv %']-prev_r['Conv %'],1)
        unprod_trend = round(curr_r['Unprod %']-prev_r['Unprod %'],1)
        if tot_trend > 0:
            cards.append(insight_card("📈","Lead Volume Growing",
                f"Total leads up by {tot_trend} vs last period. Pipeline is expanding.","good"))
        elif tot_trend < 0:
            cards.append(insight_card("📉","Lead Volume Declining",
                f"Total leads down by {abs(tot_trend)} vs last period. Check campaign activity.","bad"))
        if conv_trend > 0:
            cards.append(insight_card("🚀","Conversion Rate Improving",
                f"Conversion rate up {conv_trend}% vs last period. Lead quality is improving.","good"))
        elif conv_trend < -5:
            cards.append(insight_card("⚠️","Conversion Rate Dropped",
                f"Conversion rate fell {abs(conv_trend)}% vs last period. Review follow-up process.","warn"))
        if unprod_trend > 5:
            cards.append(insight_card("🔴","Unproductive Rate Worsening",
                f"Unproductive % increased by {unprod_trend}% vs last period. Lead targeting may have weakened.","bad"))
        elif unprod_trend < -5:
            cards.append(insight_card("✅","Lead Quality Improving",
                f"Unproductive % fell by {abs(unprod_trend)}% vs last period. Good improvement in lead quality!","good"))
        show_insights(cards)
        st.markdown("<hr class='subtle'>",unsafe_allow_html=True)
 
    st.markdown("<div class='section-title'>📈 Trend — Volume over Months</div>",unsafe_allow_html=True)
    fig = trend_line(months,
        [{'name':'Total Leads',  'data':summary['Total'].tolist()},
         {'name':'Productive',   'data':summary['Productive'].tolist()},
         {'name':'Unproductive', 'data':summary['Unproductive'].tolist()},
         {'name':'Converted',    'data':summary['Converted'].tolist()}],
        height=340)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
 
    st.markdown("<div class='section-title'>📈 Trend — Rates over Months</div>",unsafe_allow_html=True)
    fig2 = trend_line(months,
        [{'name':'Productive %',   'data':summary['Prod %'].tolist()},
         {'name':'Unproductive %', 'data':summary['Unprod %'].tolist()},
         {'name':'Conversion %',   'data':summary['Conv %'].tolist()}],
        height=300,pct_axis=True)
    st.plotly_chart(fig2,use_container_width=True,config={'displayModeBar':False})
 
    if len(summary) >= 2:
        st.markdown("<div class='section-title'>📊 Month-on-Month Comparison</div>",unsafe_allow_html=True)
        last2 = summary.tail(2)
        fig3 = grouped_bar(
            ['Total','Productive','Unproductive','Converted','Pursuing'],
            [{'name':last2.iloc[-1]['Month'],
              'data':[int(last2.iloc[-1][c]) for c in ['Total','Productive','Unproductive','Converted','Pursuing']],
              'color':'#3266ad'},
             {'name':last2.iloc[-2]['Month'],
              'data':[int(last2.iloc[-2][c]) for c in ['Total','Productive','Unproductive','Converted','Pursuing']],
              'color':'#B4B2A9'}],height=300)
        st.plotly_chart(fig3,use_container_width=True,config={'displayModeBar':False})
 
    st.markdown("<div class='section-title'>All Months Summary</div>",unsafe_allow_html=True)
    st.dataframe(summary,hide_index=True,use_container_width=True)
    st.download_button("📥 Download Comparison Report",
        data=df_to_excel({'Period Comparison':summary}),
        file_name="Caliber_Period_Comparison.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
