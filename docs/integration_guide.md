# NeuraEdge Integration Guide

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/neuraedge/ip.git
cd neuraedge-ip

# Install dependencies
pip install -r requirements.txt

# Optional: Install with UI
pip install -e ".[ui]"
```

### First Run

```python
from api.neuraedge_api import NeuraEdge
import numpy as np

# Initialize platform with default config
ne = NeuraEdge()

# Create random weights
weights = np.random.randn(64, 64)
weights = (weights - weights.min()) / (weights.max() - weights.min())

# Program tile 0
ne.program_weights(tile_id=0, weights=weights)

# Create random input
inputs = np.random.rand(64)

# Run inference
outputs = ne.run_inference(tile_id=0, inputs=inputs, timesteps=100)

# Check power
print(ne.get_power_report())
```

## Configuration

### Using Config Files

```python
from api.sdk_interface import NeuraEdgeSDK

# Load from YAML config
sdk = NeuraEdgeSDK(config_path="configs/default.yaml")

# Run inference
outputs = sdk.infer("model_name", inputs)
```

### Creating Custom Configs

```python
config = {
    "num_tiles": 4,
    "tile_size": 64,
    "device_type": "pcm",
    "mode": "hybrid",
    "timesteps": 100,
}

ne = NeuraEdge(config=config)
```

## Multi-Tile Programming

```python
from architecture.tile_manager import TileManager
from device_layer.device_config import DeviceConfig, DeviceFactory

# Create device
device_config = DeviceConfig(device_type="reram")
device = DeviceFactory.create(device_config)

# Create tile manager
tile_manager = TileManager(
    num_tiles=4,
    tile_size=64,
    device_model=device
)

# Program each tile with different weights
for tile_id in range(4):
    weights = np.random.randn(64, 64)
    tile_manager.program_tile(tile_id, weights)

# Execute on specific tile
inputs = np.random.rand(64)
outputs = tile_manager.execute(tile_id=0, inputs=inputs)
```

## Custom Device Models

```python
from device_layer.base_device import DeviceModel
import numpy as np

class CustomDevice(DeviceModel):
    def __init__(self):
        super().__init__("custom")
        self.conductance = 1e-5

    def program(self, conductance: float) -> float:
        self.conductance = conductance
        return conductance

    def read(self, voltage: float) -> float:
        return self.conductance * voltage

    def update_drift(self, time_elapsed: float):
        pass  # No drift

    def inject_noise(self) -> float:
        return 0.0  # No noise

# Use custom device
custom_device = CustomDevice()
tile_manager = TileManager(4, 64, custom_device)
```

## Benchmarking

```python
from benchmarks.mnist_test import MNISTBenchmark
from benchmarks.scaling_analysis import ScalingAnalysis
from benchmarks.energy_benchmark import EnergyBenchmark

# MNIST test
mnist = MNISTBenchmark(num_samples=100)
results = mnist.run(model=ne, test_data=data, test_labels=labels)

# Scaling analysis
scaling = ScalingAnalysis.power_vs_tile_size(
    tile_sizes=[32, 64, 128],
    model_instance=ne
)

# Energy measurement
energy = EnergyBenchmark()
total_energy = energy.measure_inference_energy(
    model=ne,
    inputs=inputs,
    timesteps=100
)
```

## System Simulation

```python
from simulation.full_system_sim import FullSystemSimulator
from simulation.multi_tile_sim import MultiTileSimulator

# Create simulator
simulator = FullSystemSimulator(
    execution_engine=ne.execution_engine,
    num_tiles=4
)

# Define workload
layer_configs = [
    {
        "tile_id": 0,
        "inputs": np.random.rand(64, 100),  # 100 timesteps
        "weights": weights0,
        "timesteps": 100,
    },
    {
        "tile_id": 1,
        "inputs": np.random.rand(64, 100),
        "weights": weights1,
        "timesteps": 100,
    },
]

# Run simulation
results = simulator.run_inference(layer_configs)
stats = simulator.get_statistics()
```

## Power Management

```python
from power_engine.power_estimator import PowerEstimator
from power_engine.voltage_model import VoltageModel

# Create power estimator
estimator = PowerEstimator()

# Estimate power for activity pattern
power = estimator.estimate_power(
    activity_rate=0.5,   # 50% of crossbar active
    matrix_size=64,
    spike_rate=0.3,      # 30% of neurons spiking
    frequency_mhz=100
)

# Voltage scaling
voltage_model = VoltageModel(nominal_voltage=0.8)
voltage_model.set_voltage(0.6)  # Reduce to 0.6V

power_scaled = power * voltage_model.power_scaling_factor()
freq_scaled = 100 * voltage_model.frequency_scaling_factor()
```

## Monitoring & Telemetry

```python
from ui.dashboard import Dashboard

# Create dashboard
dashboard = Dashboard(ne)

# Update metrics
dashboard.update()

# Get current metrics
metrics = dashboard.get_metrics()
print(f"Power: {metrics['power']['total_energy_mj']} mJ")

# Get historical data
history = dashboard.get_history(window=100)
```

## Testing

```bash
# Run unit tests
pytest tests/

# Run specific test
pytest tests/test_crossbar.py -v

# Coverage analysis
pytest --cov=architecture tests/
```

## Troubleshooting

### Import Errors
Ensure all packages are installed:
```bash
pip install -r requirements.txt
python -m pytest  # Validate installation
```

### Configuration Issues
Validate config file:
```python
from api.config_parser import ConfigParser
config = ConfigParser.load("path/to/config.yaml")
is_valid = ConfigParser.validate(config)
```

### Performance Issues
Profile execution:
```python
import cProfile
cProfile.run('ne.run_inference(0, inputs, 100)')
```

## Documentation

- Architecture: `docs/architecture_spec.md`
- Device models: `docs/device_model_spec.md`
- Power modeling: `docs/power_model_spec.md`
- NeuraTile details: `docs/neuratile_spec.md`

## Support & Issues

Report issues at: https://github.com/neuraedge/ip/issues
