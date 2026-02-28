<p align="center">
  <h1 align="center">🧠 NeuraEdge IP Platform</h1>
  <p align="center">
    <b>A professional neuromorphic computing simulation platform</b><br>
    Analog/memristive core · Event-driven SNN · Hybrid compute · Real-time dashboard
  </p>
  <p align="center">
    <a href="#quick-start">Quick Start</a> •
    <a href="#features">Features</a> •
    <a href="#interactive-dashboard">Dashboard</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#api-reference">API</a> •
    <a href="#license">License</a>
  </p>
</p>

---

## ✨ Features

| Category | Details |
|---|---|
| **Memristive Computing** | ReRAM, PCM & SRAM device models with conductance noise, temporal drift, and stuck-at fault injection |
| **Event-Driven SNN** | Leaky Integrate-and-Fire (LIF) neurons with spike-timing computation |
| **Hybrid Mode** | Automatic switching between SNN spike-based and dense MAC inference |
| **Multi-Tile Scaling** | 2D mesh spike routing, round-robin arbitration, inter-tile communication |
| **Power Modeling** | Per-component energy breakdown (DAC / ADC / crossbar / neurons) |
| **Interactive Dashboard** | Streamlit + Plotly real-time dashboard with dark/light theme toggle |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/anykrver/reneuraa.git
cd reneuraa

# Install dependencies
pip install -r requirements.txt
```

### Launch the Dashboard

```bash
streamlit run streamlit_app.py
```

Open **http://localhost:8501** — the dashboard starts in light mode by default. Toggle 🌙 **Dark Mode** from the sidebar.

### Python API

```python
from api.neuraedge_api import NeuraEdge

# Initialize the platform
ne = NeuraEdge(config={
    "num_tiles": 4,
    "tile_size": 64,
    "device_type": "reram",   # reram | pcm | sram
    "mode": "snn"             # snn | dense
})

# Program a weight matrix onto tile 0
ne.program_weights(tile_id=0, weights=weight_matrix)

# Run inference (100 SNN timesteps)
outputs = ne.run_inference(tile_id=0, inputs=input_data, timesteps=100)

# Get per-component energy report
power = ne.get_power_report()
print(f"Total energy: {power['total_energy_mj']:.2f} mJ")
print(f"Efficiency:   {power['efficiency_ops_per_mj']:.1f} ops/mJ")
```

---

## 📊 Interactive Dashboard

The Streamlit dashboard provides **12+ interactive Plotly charts** across four tabs:

| Tab | Visualizations |
|---|---|
| **📊 Dashboard** | Energy gauge, power-breakdown donut, crossbar heatmap, tile comparison bar chart |
| **⚡ Inference** | Per-neuron spike bars, spike raster plot, membrane potential trace, run history |
| **🏆 Benchmarks** | Radar chart (accuracy/latency/power), scaling grouped bars, noise error-band line, energy horizontal bars |
| **📖 Documentation** | Getting started, architecture overview, API reference, config templates |

**Theme toggle** — switch between a clean light mode (indigo/pink accents) and a premium dark mode (cyan/magenta neon) from the sidebar.

---

## 🏗️ Architecture

```
neuraedge-ip/
├── api/                # Public SDK interface (NeuraEdge class)
├── architecture/       # NeuraTile, crossbar arrays, tile manager
├── benchmarks/         # MNIST, scaling, noise robustness tests
├── configs/            # YAML configuration templates
├── device_layer/       # ReRAM / PCM / SRAM device models
├── docs/               # Architecture spec, device models, power model
├── hybrid_compute/     # SNN ↔ Dense mode switching
├── memory/             # Global SRAM, per-tile buffers, quantization
├── power_engine/       # DAC/ADC/crossbar/neuron energy modeling
├── routing/            # 2D mesh spike router, arbitration
├── simulation/         # Full system simulator
├── tests/              # Unit tests
├── ui/                 # Dashboard module & Streamlit app
├── streamlit_app.py    # Main dashboard entry point
└── requirements.txt    # Python dependencies
```

### Key Specifications

| Metric | Value |
|---|---|
| Energy efficiency | 1 250+ ops/mJ |
| Inference latency | 10.2 ms |
| Full-power draw | 125 mW |
| Sparse (10%) power | 12 mW |
| Tile sizes | 32×32 — 256×256 |
| Max tiles | 16 |

---

## 📦 API Reference

### `NeuraEdge(config)`

Create & initialize the neuromorphic platform.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `num_tiles` | int | 4 | Number of NeuraTile instances |
| `tile_size` | int | 64 | Crossbar array dimension (N×N) |
| `device_type` | str | `"reram"` | `"reram"`, `"pcm"`, or `"sram"` |
| `mode` | str | `"snn"` | `"snn"` or `"dense"` |

### Core Methods

| Method | Description |
|---|---|
| `program_weights(tile_id, weights)` | Write an N×N weight matrix to the specified tile |
| `run_inference(tile_id, inputs, timesteps)` | Execute spike-based or dense inference |
| `get_power_report()` | Returns `total_energy_mj`, `efficiency_ops_per_mj` |
| `reset()` | Reset all tiles and counters |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📁 Configuration Templates

| File | Description | Config |
|---|---|---|
| `default.yaml` | Balanced performance | 4 tiles, 64×64, ReRAM |
| `low_power.yaml` | Ultra-low power | 2 tiles, 32×32, SRAM |
| `high_accuracy.yaml` | Maximum resources | 8 tiles, 128×128, ReRAM |
| `research_mode.yaml` | Experimental | 4 tiles, 64×64, PCM |

---

## 🛠️ Tech Stack

- **Python** 3.9+
- **NumPy** / **SciPy** — numerical simulation
- **Streamlit** — web dashboard framework
- **Plotly** — interactive charting
- **Matplotlib** — static plots & analysis
- **PyYAML** — configuration management

---

## 👤 Author

**Rahul Verma**
4th-year Electronics Student, LNCT Bhopal

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
