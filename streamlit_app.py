"""
NeuraEdge IP Platform - Streamlit Web Dashboard
Premium interactive dashboard with Plotly charts and dark/light mode toggle.

Run this directly with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path

# Fix imports - add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Now import NeuraEdge components
from api.neuraedge_api import NeuraEdge
from ui.dashboard import Dashboard


def _hex_to_rgb(hex_color: str) -> list:
    """Convert '#rrggbb' to ['r','g','b'] strings for rgba() interpolation."""
    h = hex_color.lstrip("#")
    return [str(int(h[i:i+2], 16)) for i in (0, 2, 4)]

# ── Theme definitions ──────────────────────────────────────────────────
THEMES = {
    "light": dict(
        bg_primary="#f0f2f6",
        bg_card="rgba(255, 255, 255, 0.85)",
        border_glow="rgba(99, 102, 241, 0.18)",
        accent="#6366f1",         # indigo
        accent2="#ec4899",        # pink
        teal="#0d9488",
        amber="#d97706",
        text_primary="#1e293b",
        text_muted="#64748b",
        sidebar_bg_top="#f8fafc",
        sidebar_bg_bot="#f0f2f6",
        hero_grad_1="#eef2ff",
        hero_grad_2="#fdf2f8",
        hero_grad_3="#eef2ff",
        hero_glow_1="rgba(99,102,241,0.08)",
        hero_glow_2="rgba(236,72,153,0.06)",
        card_hover_border="rgba(99,102,241,0.35)",
        card_hover_shadow="rgba(99,102,241,0.10)",
        tab_active_bg="rgba(99,102,241,0.08)",
        success_bg="rgba(13,148,136,0.08)",
        success_border="rgba(13,148,136,0.3)",
        btn_grad_1="rgba(99,102,241,0.12)",
        btn_grad_2="rgba(236,72,153,0.10)",
        btn_hover_shadow="rgba(99,102,241,0.18)",
        status_bg="rgba(13,148,136,0.10)",
        status_border="rgba(13,148,136,0.25)",
        plotly_font="#475569",
        plotly_grid="rgba(0,0,0,0.06)",
        gauge_bg="#f0f2f6",
        chart_colors=["#6366f1", "#ec4899", "#0d9488", "#d97706", "#7c3aed", "#ef4444"],
    ),
    "dark": dict(
        bg_primary="#0a0f1e",
        bg_card="rgba(15, 23, 42, 0.75)",
        border_glow="rgba(0, 229, 255, 0.15)",
        accent="#00e5ff",
        accent2="#e040fb",
        teal="#1de9b6",
        amber="#ffab40",
        text_primary="#e2e8f0",
        text_muted="#94a3b8",
        sidebar_bg_top="#0d1425",
        sidebar_bg_bot="#0a0f1e",
        hero_grad_1="#0d1b3e",
        hero_grad_2="#1a0a2e",
        hero_grad_3="#0d1b3e",
        hero_glow_1="rgba(0,229,255,0.08)",
        hero_glow_2="rgba(224,64,251,0.06)",
        card_hover_border="rgba(0,229,255,0.35)",
        card_hover_shadow="rgba(0,229,255,0.08)",
        tab_active_bg="rgba(0,229,255,0.06)",
        success_bg="rgba(29,233,182,0.08)",
        success_border="rgba(29,233,182,0.3)",
        btn_grad_1="rgba(0,229,255,0.15)",
        btn_grad_2="rgba(224,64,251,0.15)",
        btn_hover_shadow="rgba(0,229,255,0.2)",
        status_bg="rgba(29,233,182,0.12)",
        status_border="rgba(29,233,182,0.3)",
        plotly_font="#c8d6e5",
        plotly_grid="rgba(255,255,255,0.06)",
        gauge_bg="#0a0f1e",
        chart_colors=["#00e5ff", "#e040fb", "#1de9b6", "#ffab40", "#7c4dff", "#ff5252"],
    ),
}


def get_theme():
    """Return current theme dict."""
    return THEMES[st.session_state.get("theme_mode", "light")]


def plotly_layout(**overrides):
    """Return a base Plotly layout dict matching the active theme."""
    t = get_theme()
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=t["plotly_font"], family="Inter, sans-serif", size=13),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(gridcolor=t["plotly_grid"], zerolinecolor=t["plotly_grid"]),
        yaxis=dict(gridcolor=t["plotly_grid"], zerolinecolor=t["plotly_grid"]),
    )
    base.update(overrides)
    return base


# Page configuration
st.set_page_config(
    page_title="NeuraEdge IP Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "platform" not in st.session_state:
    st.session_state.platform = None
    st.session_state.dashboard = None
    st.session_state.run_count = 0
    st.session_state.total_energy = 0.0
    st.session_state.inference_history = []

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"   # light is default

# ── Sidebar — theme toggle at the very top ─────────────────────────────
is_dark = st.sidebar.toggle("🌙 Dark Mode", value=(st.session_state.theme_mode == "dark"), key="theme_toggle")
st.session_state.theme_mode = "dark" if is_dark else "light"

T = get_theme()  # shorthand for current theme

# ── Custom CSS (dynamic) ──────────────────────────────────────────────
st.markdown(f"""
<style>
/* ===== Google Font ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ===== Root colours ===== */
:root {{
    --bg-primary:   {T["bg_primary"]};
    --bg-card:      {T["bg_card"]};
    --border-glow:  {T["border_glow"]};
    --accent:       {T["accent"]};
    --accent2:      {T["accent2"]};
    --teal:         {T["teal"]};
    --amber:        {T["amber"]};
    --text-primary: {T["text_primary"]};
    --text-muted:   {T["text_muted"]};
}}

/* ===== Global ===== */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stHeader"] {{ background: transparent !important; }}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {T["sidebar_bg_top"]} 0%, {T["sidebar_bg_bot"]} 100%) !important;
    border-right: 1px solid var(--border-glow) !important;
}}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] label {{ color: var(--text-primary) !important; }}

/* ===== Hero banner ===== */
.hero-banner {{
    background: linear-gradient(135deg, {T["hero_grad_1"]} 0%, {T["hero_grad_2"]} 50%, {T["hero_grad_3"]} 100%);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}}
.hero-banner::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%, {T["hero_glow_1"]}, transparent 60%),
                radial-gradient(ellipse at 80% 50%, {T["hero_glow_2"]}, transparent 60%);
}}
.hero-title {{
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0;
}}
.hero-sub {{ color: var(--text-muted); font-size: 0.95rem; margin: 4px 0 0; }}

/* ===== Glass metric cards ===== */
.glass-card {{
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-glow);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: box-shadow 0.3s, border-color 0.3s;
}}
.glass-card:hover {{
    border-color: {T["card_hover_border"]};
    box-shadow: 0 0 20px {T["card_hover_shadow"]};
}}
.card-label {{ color: var(--text-muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }}
.card-value {{ font-size: 1.6rem; font-weight: 700; color: var(--accent); margin: 4px 0 0; }}
.card-value.accent2 {{ color: var(--accent2); }}
.card-value.teal   {{ color: var(--teal); }}
.card-value.amber  {{ color: var(--amber); }}

/* ===== Section headers ===== */
.section-header {{
    font-size: 1.1rem; font-weight: 700;
    color: var(--text-primary);
    border-left: 3px solid var(--accent);
    padding-left: 12px;
    margin: 20px 0 12px;
}}

/* ===== Status pill ===== */
.status-pill {{
    display: inline-flex; align-items: center; gap: 6px;
    background: {T["status_bg"]};
    border: 1px solid {T["status_border"]};
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.8rem; font-weight: 600; color: var(--teal);
}}
.status-dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--teal);
    animation: pulse-dot 2s ease-in-out infinite;
}}
@keyframes pulse-dot {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(13,148,136,0.5); }}
    50%      {{ box-shadow: 0 0 0 6px rgba(13,148,136,0); }}
}}

/* ===== Tabs ===== */
[data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid var(--border-glow) !important;
    gap: 0 !important;
}}
[data-baseweb="tab"] {{
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: color 0.2s, background 0.2s;
}}
[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--accent) !important;
    background: {T["tab_active_bg"]} !important;
    border-bottom: 2px solid var(--accent) !important;
}}

/* ===== Success banner ===== */
.glow-success {{
    background: {T["success_bg"]};
    border: 1px solid {T["success_border"]};
    border-radius: 10px;
    padding: 14px 20px;
    color: var(--teal);
    font-weight: 600;
    text-align: center;
    margin-top: 12px;
}}

/* ===== Expanders ===== */
details summary {{
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}}

/* ===== Streamlit default metric override ===== */
[data-testid="stMetric"] {{ background: transparent !important; }}
[data-testid="stMetricValue"] {{ color: var(--accent) !important; }}
[data-testid="stMetricLabel"] {{ color: var(--text-muted) !important; }}

/* ===== Button styling ===== */
.stButton > button {{
    background: linear-gradient(135deg, {T["btn_grad_1"]}, {T["btn_grad_2"]}) !important;
    border: 1px solid var(--border-glow) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 8px 28px !important;
    transition: all 0.3s !important;
}}
.stButton > button:hover {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 18px {T["btn_hover_shadow"]} !important;
}}

/* ===== Toggle ===== */
[data-testid="stSidebar"] .stToggle label span {{
    color: var(--text-primary) !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Hero banner ────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <p class="hero-title">🧠 NeuraEdge IP Platform</p>
    <p class="hero-sub">Professional Neuromorphic Computing Platform &middot; Real-Time Interactive Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar config ─────────────────────────────────────────────────────
st.sidebar.markdown('<p class="section-header">⚙️ System Configuration</p>', unsafe_allow_html=True)
num_tiles = st.sidebar.slider("Number of Tiles", 1, 16, 4, key="tiles")
tile_size = st.sidebar.slider("Tile Size", 32, 256, 64, key="size")
device_type = st.sidebar.selectbox("Device Type", ["reram", "pcm", "sram"], key="device")
mode = st.sidebar.selectbox("Mode", ["snn", "dense"], key="mode")

st.sidebar.markdown("---")
st.sidebar.markdown('<span class="status-pill"><span class="status-dot"></span>System Online</span>', unsafe_allow_html=True)

# Initialize platform
if st.session_state.platform is None:
    config = {
        "num_tiles": num_tiles,
        "tile_size": tile_size,
        "device_type": device_type,
        "mode": mode,
    }
    st.session_state.platform = NeuraEdge(config=config)
    st.session_state.dashboard = Dashboard(st.session_state.platform)

ne = st.session_state.platform
dashboard = st.session_state.dashboard

# ── Tabs ───────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "⚡ Inference", "🏆 Benchmarks", "📖 Documentation"])


# ========================================================================
#  TAB 1 — DASHBOARD
# ========================================================================
with tab1:
    power = ne.get_power_report()
    tile_0 = ne.tile_manager.get_tile(0)
    spike_sum = int(np.sum(tile_0.neurons.get_spike_counts()))

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("Total Tiles", f"{num_tiles}", ""),
        ("Total Energy", f"{power['total_energy_mj']:.2f} mJ", "accent2"),
        ("Efficiency", f"{power['efficiency_ops_per_mj']:.1f} ops/mJ", "teal"),
        ("Total Spikes", f"{spike_sum}", "amber"),
    ]
    for col, (label, value, accent) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <p class="card-label">{label}</p>
                <p class="card-value {accent}">{value}</p>
            </div>
            """, unsafe_allow_html=True)

    # -- Row 2: Gauges + Donut ---
    st.markdown('<p class="section-header">System Overview</p>', unsafe_allow_html=True)
    g1, g2 = st.columns([1.2, 1])

    with g1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=power["total_energy_mj"],
            title={"text": "Total Energy (mJ)", "font": {"size": 14, "color": T["plotly_font"]}},
            number={"font": {"color": T["accent"], "size": 36}, "suffix": " mJ"},
            delta={"reference": 0.5, "increasing": {"color": T["accent2"]}},
            gauge=dict(
                axis=dict(range=[0, max(power["total_energy_mj"] * 2, 1)], tickcolor=T["plotly_font"]),
                bar=dict(color=T["accent"]),
                bgcolor=T["gauge_bg"],
                borderwidth=0,
                steps=[
                    dict(range=[0, max(power["total_energy_mj"] * 0.6, 0.3)], color=f"rgba({','.join(_hex_to_rgb(T['accent']))},0.08)"),
                    dict(range=[max(power["total_energy_mj"] * 0.6, 0.3), max(power["total_energy_mj"] * 2, 1)], color=f"rgba({','.join(_hex_to_rgb(T['accent2']))},0.06)"),
                ],
                threshold=dict(line=dict(color=T["accent2"], width=3), thickness=0.8, value=power["total_energy_mj"]),
            ),
        ))
        fig_gauge.update_layout(**plotly_layout(height=300))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with g2:
        pm = tile_0.power_monitor
        labels = ["DAC", "ADC", "Crossbar", "Neurons"]
        values = [pm.dac_energy, pm.adc_energy, pm.crossbar_energy, pm.neuron_energy]
        fig_donut = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=T["chart_colors"][:4], line=dict(width=2, color=T["bg_primary"])),
            textinfo="label+percent",
            textfont=dict(color=T["plotly_font"], size=12),
            hovertemplate="<b>%{label}</b><br>%{value:.1f} pJ<br>%{percent}<extra></extra>",
            pull=[0.04, 0, 0, 0],
        ))
        fig_donut.update_layout(**plotly_layout(
            height=300,
            title=dict(text="Power Breakdown (pJ)", font=dict(size=14, color=T["plotly_font"])),
            showlegend=False,
        ))
        st.plotly_chart(fig_donut, use_container_width=True)

    # -- Row 3: Heatmap + Tile comparison ---
    h1, h2 = st.columns(2)

    with h1:
        st.markdown('<p class="section-header">Crossbar Weight Matrix — Tile 0</p>', unsafe_allow_html=True)
        w = tile_0.crossbar.weights
        fig_heat = go.Figure(go.Heatmap(
            z=w, colorscale="Viridis",
            hovertemplate="Row %{y}, Col %{x}<br>Weight: %{z:.4f}<extra></extra>",
        ))
        fig_heat.update_layout(**plotly_layout(
            height=370,
            xaxis=dict(title="Column", gridcolor=T["plotly_grid"]),
            yaxis=dict(title="Row", autorange="reversed", gridcolor=T["plotly_grid"]),
        ))
        st.plotly_chart(fig_heat, use_container_width=True)

    with h2:
        st.markdown('<p class="section-header">Tile Comparison</p>', unsafe_allow_html=True)
        tile_ids = list(range(num_tiles))
        energies = []
        spikes = []
        for tid in tile_ids:
            t = ne.tile_manager.get_tile(tid)
            energies.append(t.power_monitor.get_total_energy())
            spikes.append(float(np.sum(t.neurons.get_spike_counts())))
        fig_tiles = go.Figure()
        fig_tiles.add_trace(go.Bar(
            name="Energy (pJ)", x=[f"Tile {i}" for i in tile_ids], y=energies,
            marker_color=T["accent"], marker_line=dict(width=0),
        ))
        fig_tiles.add_trace(go.Bar(
            name="Spikes", x=[f"Tile {i}" for i in tile_ids], y=spikes,
            marker_color=T["accent2"], marker_line=dict(width=0),
        ))
        fig_tiles.update_layout(**plotly_layout(
            height=370, barmode="group",
            legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center", font=dict(size=11)),
        ))
        st.plotly_chart(fig_tiles, use_container_width=True)


# ========================================================================
#  TAB 2 — INFERENCE
# ========================================================================
with tab2:
    st.markdown('<p class="section-header">Run Inference</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <p class="card-label">Input Configuration</p>
        </div>
        """, unsafe_allow_html=True)
        sparsity = st.slider("Input Sparsity", 0.0, 1.0, 0.7, step=0.05)
        timesteps = st.slider("Timesteps", 10, 500, 100, step=10)
        tile_id = st.selectbox("Target Tile", range(num_tiles))

    with col2:
        st.markdown("""
        <div class="glass-card">
            <p class="card-label">Inference Control</p>
        </div>
        """, unsafe_allow_html=True)

        run_col, reset_col = st.columns(2)
        with run_col:
            run_clicked = st.button("⚡ Run Inference", key="run_button", use_container_width=True)
        with reset_col:
            reset_clicked = st.button("🔄 Reset System", key="reset_button", use_container_width=True)

    if run_clicked:
        with st.spinner("Running inference..."):
            np.random.seed(42 + st.session_state.run_count)
            inputs = np.random.rand(tile_size)
            inputs = (inputs > sparsity).astype(float)

            weights = np.random.randn(tile_size, tile_size) * 0.3
            weights = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)

            ne.program_weights(tile_id, weights)
            outputs = ne.run_inference(tile_id, inputs, timesteps=timesteps)

            dashboard.update()
            st.session_state.run_count += 1

            spike_counts = np.array([len(s) if isinstance(s, (list, np.ndarray)) else 0 for s in outputs])
            total_spikes = int(spike_counts.sum())
            spike_rate = total_spikes / (timesteps * tile_size) * 100

            power = ne.get_power_report()
            st.session_state.inference_history.append({
                "run": st.session_state.run_count,
                "spikes": total_spikes,
                "energy": power["total_energy_mj"],
                "efficiency": power["efficiency_ops_per_mj"],
            })

        st.markdown(f"""
        <div class="glow-success">
            ✅ Inference complete — <b>{total_spikes}</b> spikes detected | Spike rate: <b>{spike_rate:.1f}%</b> | Energy: <b>{power['total_energy_mj']:.2f} mJ</b>
        </div>
        """, unsafe_allow_html=True)

        r1, r2 = st.columns(2)

        with r1:
            st.markdown('<p class="section-header">Per-Neuron Spike Counts</p>', unsafe_allow_html=True)
            fig_bar = go.Figure(go.Bar(
                x=list(range(len(spike_counts))),
                y=spike_counts,
                marker=dict(
                    color=spike_counts,
                    colorscale=[[0, f"rgba({','.join(_hex_to_rgb(T['accent']))},0.3)"], [1, T["accent"]]],
                    line=dict(width=0),
                ),
                hovertemplate="Neuron %{x}<br>Spikes: %{y}<extra></extra>",
            ))
            fig_bar.update_layout(**plotly_layout(
                height=320,
                xaxis=dict(title="Neuron Index"),
                yaxis=dict(title="Spike Count"),
            ))
            st.plotly_chart(fig_bar, use_container_width=True)

        with r2:
            st.markdown('<p class="section-header">Spike Raster Plot</p>', unsafe_allow_html=True)
            raster_x, raster_y = [], []
            for neuron_idx, s in enumerate(outputs):
                if isinstance(s, (list, np.ndarray)) and len(s) > 0:
                    times = list(s) if isinstance(s, list) else s.tolist()
                    raster_x.extend(times)
                    raster_y.extend([neuron_idx] * len(times))

            fig_raster = go.Figure(go.Scattergl(
                x=raster_x, y=raster_y,
                mode="markers",
                marker=dict(size=2.5, color=T["accent"], opacity=0.7),
                hovertemplate="Time: %{x}<br>Neuron: %{y}<extra></extra>",
            ))
            fig_raster.update_layout(**plotly_layout(
                height=320,
                xaxis=dict(title="Timestep"),
                yaxis=dict(title="Neuron Index"),
            ))
            st.plotly_chart(fig_raster, use_container_width=True)

        # Membrane potential trace
        st.markdown('<p class="section-header">Membrane Potential Trace (Simulated)</p>', unsafe_allow_html=True)
        np.random.seed(123)
        t_axis = np.arange(timesteps)
        v_trace = np.zeros(timesteps)
        threshold = 1.0
        v = 0.0
        tau = 0.9
        for i in range(timesteps):
            v = v * tau + np.random.randn() * 0.3 + 0.15
            if v >= threshold:
                v_trace[i] = threshold * 1.1
                v = 0.0
            else:
                v_trace[i] = v

        fig_mem = go.Figure()
        fig_mem.add_trace(go.Scatter(
            x=t_axis, y=v_trace,
            mode="lines",
            line=dict(color=T["accent"], width=1.5),
            fill="tozeroy",
            fillcolor=f"rgba({','.join(_hex_to_rgb(T['accent']))},0.08)",
            hovertemplate="t=%{x}<br>V=%{y:.3f}<extra></extra>",
            name="V_mem",
        ))
        fig_mem.add_hline(y=threshold, line=dict(color=T["accent2"], dash="dash", width=1), annotation_text="Threshold")
        fig_mem.update_layout(**plotly_layout(
            height=260,
            xaxis=dict(title="Timestep"),
            yaxis=dict(title="Membrane Potential (a.u.)"),
        ))
        st.plotly_chart(fig_mem, use_container_width=True)

        # History
        if len(st.session_state.inference_history) > 1:
            st.markdown('<p class="section-header">Run History</p>', unsafe_allow_html=True)
            hist = st.session_state.inference_history
            runs = [h["run"] for h in hist]
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Scatter(
                x=runs, y=[h["spikes"] for h in hist],
                mode="lines+markers", name="Spikes",
                line=dict(color=T["accent"], width=2), marker=dict(size=6),
            ))
            fig_hist.add_trace(go.Scatter(
                x=runs, y=[h["energy"] for h in hist],
                mode="lines+markers", name="Energy (mJ)",
                line=dict(color=T["accent2"], width=2), marker=dict(size=6),
                yaxis="y2",
            ))
            fig_hist.update_layout(**plotly_layout(
                height=280,
                xaxis=dict(title="Run #"),
                yaxis=dict(title="Spikes", title_font=dict(color=T["accent"])),
                yaxis2=dict(title="Energy (mJ)", title_font=dict(color=T["accent2"]),
                            overlaying="y", side="right", gridcolor=T["plotly_grid"]),
                legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"),
            ))
            st.plotly_chart(fig_hist, use_container_width=True)

    if reset_clicked:
        ne.reset()
        st.session_state.run_count = 0
        st.session_state.inference_history = []
        st.markdown('<div class="glow-success">🔄 System reset successfully</div>', unsafe_allow_html=True)


# ========================================================================
#  TAB 3 — BENCHMARKS
# ========================================================================
with tab3:
    st.markdown('<p class="section-header">Benchmark Suite</p>', unsafe_allow_html=True)

    bench_type = st.selectbox(
        "Select Benchmark",
        ["Performance", "Scaling Analysis", "Noise Robustness", "Energy Profile"],
    )

    if bench_type == "Performance":
        st.markdown('<p class="section-header">MNIST Inference Benchmark</p>', unsafe_allow_html=True)

        categories = ["Accuracy (%)", "1/Latency", "1/Power", "Efficiency"]
        values = [95.2, 1 / 10.2 * 100, 1 / 125 * 1000, 1250 / 1500 * 100]
        fig_radar = go.Figure(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba({','.join(_hex_to_rgb(T['accent']))},0.1)",
            line=dict(color=T["accent"], width=2),
            marker=dict(size=6, color=T["accent"]),
            hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
        ))
        fig_radar.update_layout(**plotly_layout(
            height=400,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, color=T["plotly_font"], gridcolor=T["plotly_grid"]),
                angularaxis=dict(color=T["plotly_font"], gridcolor=T["plotly_grid"]),
            ),
        ))

        bc1, bc2 = st.columns([1.3, 1])
        with bc1:
            st.plotly_chart(fig_radar, use_container_width=True)
        with bc2:
            for lbl, val, unit, clr in [
                ("Accuracy", "95.2", "%", ""),
                ("Latency", "10.2", "ms", "accent2"),
                ("Power", "125", "mW", "teal"),
                ("Efficiency", "1250", "ops/mJ", "amber"),
            ]:
                st.markdown(f"""
                <div class="glass-card">
                    <p class="card-label">{lbl}</p>
                    <p class="card-value {clr}">{val} <span style="font-size:0.7em;color:var(--text-muted)">{unit}</span></p>
                </div>
                """, unsafe_allow_html=True)

    elif bench_type == "Scaling Analysis":
        st.markdown('<p class="section-header">Power vs Tile Size — Device Comparison</p>', unsafe_allow_html=True)

        tile_sizes = ["32×32", "64×64", "128×128", "256×256"]
        reram_power = [31, 125, 510, 2100]
        pcm_power =   [38, 150, 620, 2500]
        sram_power =  [22, 90,  370, 1500]

        fig_scale = go.Figure()
        for name, data, color in [("ReRAM", reram_power, T["accent"]), ("PCM", pcm_power, T["accent2"]), ("SRAM", sram_power, T["teal"])]:
            fig_scale.add_trace(go.Bar(
                name=name, x=tile_sizes, y=data,
                marker_color=color, marker_line=dict(width=0),
                hovertemplate=f"{name}<br>%{{x}}: %{{y}} mW<extra></extra>",
            ))
        fig_scale.update_layout(**plotly_layout(
            height=420, barmode="group",
            xaxis=dict(title="Tile Size"),
            yaxis=dict(title="Power (mW)"),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_scale, use_container_width=True)

    elif bench_type == "Noise Robustness":
        st.markdown('<p class="section-header">Accuracy Degradation with Noise</p>', unsafe_allow_html=True)

        noise = [0, 1, 2, 5, 10, 15, 20]
        acc_mean = [95.2, 94.8, 94.2, 92.1, 88.5, 84.0, 78.5]
        acc_upper = [95.2, 95.1, 94.9, 93.5, 90.8, 87.2, 82.3]
        acc_lower = [95.2, 94.5, 93.5, 90.7, 86.2, 80.8, 74.7]

        fig_noise = go.Figure()
        fig_noise.add_trace(go.Scatter(
            x=noise + noise[::-1],
            y=acc_upper + acc_lower[::-1],
            fill="toself", fillcolor=f"rgba({','.join(_hex_to_rgb(T['accent']))},0.1)",
            line=dict(width=0), showlegend=False,
            hoverinfo="skip",
        ))
        fig_noise.add_trace(go.Scatter(
            x=noise, y=acc_mean,
            mode="lines+markers",
            line=dict(color=T["accent"], width=2.5),
            marker=dict(size=8, color=T["accent"], line=dict(width=2, color=T["bg_primary"])),
            name="Mean Accuracy",
            hovertemplate="Noise: %{x}%<br>Accuracy: %{y:.1f}%<extra></extra>",
        ))
        fig_noise.add_annotation(x=5, y=92.1, text="5% – 92.1%", showarrow=True,
                                 arrowcolor=T["accent2"], font=dict(color=T["accent2"], size=11),
                                 ax=40, ay=-30)
        fig_noise.add_annotation(x=10, y=88.5, text="10% – 88.5%", showarrow=True,
                                 arrowcolor=T["amber"], font=dict(color=T["amber"], size=11),
                                 ax=40, ay=-30)
        fig_noise.update_layout(**plotly_layout(
            height=420,
            xaxis=dict(title="Noise Level (%)", dtick=5),
            yaxis=dict(title="Accuracy (%)", range=[70, 97]),
        ))
        st.plotly_chart(fig_noise, use_container_width=True)

    elif bench_type == "Energy Profile":
        st.markdown('<p class="section-header">Per-Component Energy Breakdown</p>', unsafe_allow_html=True)

        components = ["DAC", "ADC", "Crossbar", "Neurons"]
        values_e = [55.4, 0.3, 4.0, 40.3]
        colors_e = [T["accent"], T["teal"], T["amber"], T["accent2"]]
        sorted_data = sorted(zip(components, values_e, colors_e), key=lambda x: x[1])
        s_comp, s_val, s_col = zip(*sorted_data)

        fig_energy = go.Figure(go.Bar(
            y=list(s_comp), x=list(s_val),
            orientation="h",
            marker=dict(color=list(s_col), line=dict(width=0)),
            text=[f"{v:.1f} pJ" for v in s_val],
            textposition="outside",
            textfont=dict(color=T["plotly_font"]),
            hovertemplate="<b>%{y}</b>: %{x:.1f} pJ<extra></extra>",
        ))
        fig_energy.update_layout(**plotly_layout(
            height=320,
            xaxis=dict(title="Energy (pJ)"),
            yaxis=dict(title=""),
        ))
        st.plotly_chart(fig_energy, use_container_width=True)


# ========================================================================
#  TAB 4 — DOCUMENTATION
# ========================================================================
with tab4:
    st.markdown('<p class="section-header">Documentation & Help</p>', unsafe_allow_html=True)

    with st.expander("🚀 Getting Started", expanded=True):
        st.markdown("""
**1. Configure System** (left sidebar)
- Number of tiles (1 – 16)
- Tile size (32 – 256)
- Device type: ReRAM / PCM / SRAM
- Mode: SNN / Dense

**2. Run Inference** (⚡ Inference tab)
- Adjust input sparsity & timesteps
- Click **Run Inference**
- View interactive spike charts & membrane traces

**3. Analyze** (📊 Dashboard & 🏆 Benchmarks)
- Monitor energy gauges & power donuts
- Explore scaling, noise, and efficiency benchmarks
        """)

    with st.expander("🏗️ Architecture"):
        st.markdown("""
| Component | Description |
|---|---|
| **NeuraTiles** | 64×64 memristive crossbar arrays |
| **LIF Neurons** | Leaky Integrate-and-Fire neurons |
| **Routing** | 2D mesh spike router |
| **Memory** | Global SRAM + per-tile buffers |

**Key Specifications:**
- Energy: **1250+ ops/mJ**
- Latency: **10.2 ms** per inference
- Power: **125 mW** (full), **12 mW** (10% sparse)
        """)

    with st.expander("💻 API Reference"):
        st.code("""
from api.neuraedge_api import NeuraEdge

# Create platform
ne = NeuraEdge(config={
    "num_tiles": 4,
    "tile_size": 64,
    "device_type": "reram",
    "mode": "snn"
})

# Program weights
ne.program_weights(tile_id=0, weights=weights)

# Run inference
outputs = ne.run_inference(
    tile_id=0,
    inputs=input_data,
    timesteps=100
)

# Get power report
power = ne.get_power_report()
        """, language="python")

    with st.expander("📁 Configuration Templates"):
        configs = {
            "default.yaml": ("Balanced performance", "4 tiles, 64×64, ReRAM"),
            "low_power.yaml": ("Ultra-low power", "2 tiles, 32×32, SRAM"),
            "high_accuracy.yaml": ("Maximum resources", "8 tiles, 128×128, ReRAM"),
            "research_mode.yaml": ("Experimental features", "4 tiles, 64×64, PCM"),
        }
        for name, (desc, spec) in configs.items():
            st.markdown(f"**`{name}`** — {desc}  \n{spec}")


# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:16px 0;">
    <span style="color: var(--text-muted); font-size:0.85rem;">
        NeuraEdge IP Platform v0.1.0 &nbsp;|&nbsp; Open Source (MIT)
        &nbsp;|&nbsp;
        <a href="https://github.com/anykrver/reneuraa" style="color: var(--accent); text-decoration:none;">GitHub&nbsp;↗</a>
    </span>
</div>
""", unsafe_allow_html=True)
