# NeuraEdge IP Platform

Professional neuromorphic computing platform with analog/memristive core and event-driven scalability.

## Architecture

```
neuraedge-ip/
├── device_layer/       # ReRAM/PCM/SRAM models
├── architecture/       # NeuraTile, crossbar, neurons
├── power_engine/       # Energy/power modeling
├── hybrid_compute/     # SNN/Dense mode switching
├── routing/            # Multi-tile spike routing
├── memory/             # Global SRAM, buffers, quantization
├── benchmarks/         # MNIST, scaling, noise tests
├── simulation/         # Full system simulator
├── api/                # Public SDK interface
├── ui/                 # Dashboard & Streamlit
└── tests/              # Unit tests
```

## Quick Start

```python
from api.neuraedge_api import NeuraEdge

# Initialize platform
ne = NeuraEdge(config={
    "num_tiles": 4,
    "tile_size": 64,
    "device_type": "reram",
    "mode": "snn"
})

# Program weights
ne.program_weights(tile_id=0, weights=weights_matrix)

# Run inference
outputs = ne.run_inference(
    tile_id=0,
    inputs=input_data,
    timesteps=100
)

# Get power report
power = ne.get_power_report()
```

## Features

- **Memristive Computing**: ReRAM/PCM device models with noise/drift
- **Event-Driven SNN**: Spike-based computation with LIF neurons
- **Hybrid Mode**: Automatic switching between SNN and dense MAC
- **Multi-Tile Scaling**: Mesh routing, arbitration, inter-tile communication
- **Power Modeling**: DAC/ADC/crossbar energy breakdown
- **Device Variation**: Conductance noise, temporal drift, stuck-at faults

## Installation

```bash
pip install -r requirements.txt
```

## Documentation

See `docs/` for:
- Architecture specification
- Device models
- Power model
- Integration guide

## License

See LICENSE file.
