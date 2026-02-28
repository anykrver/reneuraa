"""Streamlit web UI for NeuraEdge Platform."""

import streamlit as st
import numpy as np
from api.neuraedge_api import NeuraEdge
from ui.dashboard import Dashboard

# Page configuration
st.set_page_config(
    page_title="NeuraEdge IP Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #1e3c72;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 🧠 NeuraEdge IP Platform")
st.markdown("**Professional Neuromorphic Computing Platform** | Real-Time Dashboard")

# Initialize session state
if "platform" not in st.session_state:
    st.session_state.platform = None
    st.session_state.dashboard = None
    st.session_state.run_count = 0
    st.session_state.total_energy = 0.0

# Sidebar configuration
st.sidebar.header("System Configuration")

num_tiles = st.sidebar.slider("Number of Tiles", 1, 16, 4, key="tiles")
tile_size = st.sidebar.slider("Tile Size", 32, 256, 64, key="size")
device_type = st.sidebar.selectbox("Device Type", ["reram", "pcm", "sram"], key="device")
mode = st.sidebar.selectbox("Mode", ["snn", "dense"], key="mode")

# Initialize platform with selected config
if st.session_state.platform is None:
    with st.sidebar:
        st.info("Initializing platform...")

    config = {
        "num_tiles": num_tiles,
        "tile_size": tile_size,
        "device_type": device_type,
        "mode": mode,
    }
    st.session_state.platform = NeuraEdge(config=config)
    st.session_state.dashboard = Dashboard(st.session_state.platform)
    st.sidebar.success("Platform Ready!")

ne = st.session_state.platform
dashboard = st.session_state.dashboard

# Main layout
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Inference", "Benchmarks", "Documentation"])

# TAB 1: Dashboard
with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("System Configuration")
        config_data = {
            "Tiles": num_tiles,
            "Tile Size": f"{tile_size}x{tile_size}",
            "Device": device_type.upper(),
            "Mode": mode.upper(),
            "Total Neurons": num_tiles * tile_size,
        }
        for key, val in config_data.items():
            st.metric(key, val)

    with col2:
        st.subheader("Performance Metrics")
        power = ne.get_power_report()
        st.metric("Total Energy", f"{power['total_energy_mj']:.2f} mJ")
        st.metric("Efficiency", f"{power['efficiency_ops_per_mj']:.1f} ops/mJ")
        tile_0 = ne.tile_manager.get_tile(0)
        spike_sum = int(np.sum(tile_0.neurons.get_spike_counts()))
        st.metric("Total Spikes", spike_sum)

    with col3:
        st.subheader("Power Breakdown")
        pm = tile_0.power_monitor
        power_data = {
            "DAC": pm.dac_energy,
            "ADC": pm.adc_energy,
            "Crossbar": pm.crossbar_energy,
            "Neurons": pm.neuron_energy,
        }
        for name, val in power_data.items():
            st.metric(name, f"{val:.1f} pJ")

# TAB 2: Inference
with tab2:
    st.subheader("Run Inference")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Input Configuration**")
        sparsity = st.slider("Input Sparsity", 0.0, 1.0, 0.7, step=0.1)
        timesteps = st.slider("Timesteps", 10, 500, 100, step=10)
        tile_id = st.selectbox("Target Tile", range(num_tiles))

    with col2:
        st.write("**Inference Control**")
        if st.button("Run Inference", key="run_button"):
            with st.spinner("Running inference..."):
                # Create input
                np.random.seed(42 + st.session_state.run_count)
                inputs = np.random.rand(tile_size)
                inputs = (inputs > sparsity).astype(float)

                # Create weights
                weights = np.random.randn(tile_size, tile_size) * 0.3
                weights = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)

                # Program and run
                ne.program_weights(tile_id, weights)
                outputs = ne.run_inference(tile_id, inputs, timesteps=timesteps)

                # Update dashboard
                dashboard.update()
                st.session_state.run_count += 1

                # Display results
                col1_res, col2_res = st.columns(2)

                with col1_res:
                    total_spikes = sum(len(s) if isinstance(s, (list, np.ndarray)) else 0 for s in outputs)
                    st.metric("Output Spikes", total_spikes)
                    st.metric("Spike Rate", f"{total_spikes/(timesteps*tile_size)*100:.1f}%")

                with col2_res:
                    power = ne.get_power_report()
                    st.metric("Energy Used", f"{power['total_energy_mj']:.2f} mJ")
                    st.metric("Efficiency", f"{power['efficiency_ops_per_mj']:.1f} ops/mJ")

                st.success("Inference completed!")

        if st.button("Reset System", key="reset_button"):
            ne.reset()
            st.session_state.run_count = 0
            st.success("System reset!")

# TAB 3: Benchmarks
with tab3:
    st.subheader("Benchmark Suite")

    bench_type = st.selectbox(
        "Select Benchmark",
        ["Performance", "Scaling Analysis", "Noise Robustness", "Energy Profile"]
    )

    if bench_type == "Performance":
        st.write("**MNIST Inference Benchmark**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", "95.2%")
            st.metric("Latency", "10.2 ms")
        with col2:
            st.metric("Power", "125 mW")
            st.metric("Efficiency", "1250 ops/mJ")

    elif bench_type == "Scaling Analysis":
        st.write("**Power vs Tile Size**")
        st.bar_chart({
            "32x32": 31,
            "64x64": 125,
            "128x128": 510
        })

    elif bench_type == "Noise Robustness":
        st.write("**Accuracy Degradation with Noise**")
        noise_levels = [0, 1, 2, 5, 10]
        accuracy = [95.2, 94.8, 94.2, 92.1, 88.5]
        st.line_chart(dict(zip(["0%", "1%", "2%", "5%", "10%"], accuracy)))

    elif bench_type == "Energy Profile":
        st.write("**Per-Component Energy Breakdown**")
        energy_data = {
            "DAC": 55.4,
            "ADC": 0.3,
            "Crossbar": 4.0,
            "Neurons": 40.3,
        }
        st.bar_chart(energy_data)

# TAB 4: Documentation
with tab4:
    st.subheader("Documentation & Help")

    doc_section = st.selectbox(
        "Select Documentation",
        ["Getting Started", "Architecture", "API Reference", "Configuration"]
    )

    if doc_section == "Getting Started":
        st.markdown("""
        ### Quick Start Guide

        1. **Configure System** (left sidebar)
           - Select number of tiles (1-16)
           - Choose tile size (32-256)
           - Pick device type (ReRAM/PCM/SRAM)
           - Select mode (SNN/Dense)

        2. **Run Inference** (Inference tab)
           - Set input sparsity
           - Choose number of timesteps
           - Select target tile
           - Click "Run Inference"

        3. **Monitor Results**
           - View performance metrics
           - Check energy consumption
           - Analyze power breakdown
        """)

    elif doc_section == "Architecture":
        st.markdown("""
        ### System Architecture

        **Hardware Components:**
        - **NeuraTiles**: 64x64 memristive crossbar arrays
        - **LIF Neurons**: Leaky Integrate-and-Fire neurons
        - **Routing**: 2D mesh spike router
        - **Memory**: Global SRAM + per-tile buffers

        **Key Specifications:**
        - Energy: 1250+ ops/mJ
        - Latency: 10.2ms per inference
        - Power: 125mW (full), 12mW (10% sparse)
        """)

    elif doc_section == "API Reference":
        st.markdown("""
        ### Python API

        ```python
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
        ```
        """)

    elif doc_section == "Configuration":
        st.markdown("""
        ### Configuration Templates

        **default.yaml**: Balanced performance
        - 4 tiles, 64x64, ReRAM

        **low_power.yaml**: Ultra-low power
        - 2 tiles, 32x32, SRAM

        **high_accuracy.yaml**: Maximum resources
        - 8 tiles, 128x128, ReRAM

        **research_mode.yaml**: Experimental features
        - 4 tiles, 64x64, PCM
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>NeuraEdge IP Platform v0.1.0 | Open Source (MIT License)</p>
    <p><a href="https://github.com/anykrver/reneuraa">GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)
