"""Streamlit web UI for NeuraEdge."""

# Streamlit app - requires: pip install streamlit


def create_app():
    """Create Streamlit application."""
    try:
        import streamlit as st
        from api.neuraedge_api import NeuraEdge
        from ui.dashboard import Dashboard

        st.set_page_config(page_title="NeuraEdge IP", layout="wide")

        st.title("🧠 NeuraEdge IP Platform")

        # Sidebar configuration
        with st.sidebar:
            st.header("Configuration")
            num_tiles = st.slider("Number of Tiles", 1, 16, 4)
            tile_size = st.slider("Tile Size", 32, 256, 64)
            device = st.selectbox("Device Type", ["reram", "pcm", "sram"])
            mode = st.selectbox("Mode", ["snn", "dense", "hybrid"])

        # Main content
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("System Configuration")
            config = {
                "num_tiles": num_tiles,
                "tile_size": tile_size,
                "device_type": device,
                "mode": mode,
            }
            st.json(config)

        with col2:
            st.subheader("Power Report")
            if st.button("Run Benchmark"):
                st.info("Running inference...")
                # Mock inference
                st.success("Inference completed!")

        # Monitoring
        st.subheader("Monitoring")
        col3, col4, col5 = st.columns(3)

        with col3:
            st.metric("Total Power", "125 mW", "±5%")

        with col4:
            st.metric("Latency", "10.2 ms", "↓ 2.1ms")

        with col5:
            st.metric("Efficiency", "1250 ops/mJ", "↑ 125")

    except ImportError:
        print("Streamlit not installed. Install with: pip install streamlit")


if __name__ == "__main__":
    create_app()
