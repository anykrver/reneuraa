# Device Model Specification

## Supported Devices

NeuraEdge supports multiple resistive device technologies for memristive weights.

## ReRAM (Resistive RAM)

### Characteristics
- Typical conductance range: 1e-6 to 1e-4 S
- Read voltage: 0.5V
- Programming voltage: 1-2V
- Write-to-read ratio: ~1000×

### Noise Model
- Gaussian noise (std: 2% of conductance)
- Random Telegraph Noise (RTN) for low conductance
- Conductance variation during programming (~2%)

### Drift Model
- Temporal drift: G(t) = G₀ × (1 - α × ln(t))
- Drift coefficient α: 0.001 (0.1% per decade)
- Dominant at low conductance states

### Nonlinearity
- I-V nonlinearity: I = G×V + β×V²
- Nonlinearity coefficient β: 0.1
- More evident at high voltages

## PCM (Phase Change Memory)

### Characteristics
- Conductance range: 1e-6 to 1e-4 S
- Multi-level capability: 50+ discrete states
- Reset/Set asymmetry: 10-100×
- Write energy: ~50-100 pJ per cell

### Noise Model
- Log-normal noise distribution
- Higher noise than ReRAM (3% std)
- State-dependent noise

### Drift Model
- Stronger drift than ReRAM
- α: 0.05 (0.5% per decade)
- Temperature-dependent drift

### Crystallinity
- Crystal fraction affects conductance
- Dynamic update during cycling

## SRAM (Reference Device)

### Characteristics
- Ideal linear behavior
- Minimal noise (<0.1%)
- No drift
- Used for comparison and validation

## Device Abstraction

All devices inherit from `DeviceModel` base class:

```python
class DeviceModel(ABC):
    def program(self, conductance: float) -> float
    def read(self, voltage: float) -> float
    def update_drift(self, time_elapsed: float)
    def inject_noise(self) -> float
```

## Calibration & Validation

### Programming Accuracy Test
- Target: 10 conductance values
- Measurement: Actual vs. target
- Tolerance: ±5%

### Noise Characterization
- Measure 1000 reads per conductance state
- Validate noise std deviation
- Confirm distribution type

### Drift Validation
- Program to fixed conductance
- Measure over 24+ hours
- Validate temporal response

### Temperature Testing
- Test -40°C to +125°C range
- Measure conductance vs. temperature
- Verify leakage scaling

## Integration Parameters

In `device_layer/device_config.py`:

```python
@dataclass
class DeviceConfig:
    device_type: str              # "reram", "pcm", "sram"
    max_conductance: float = 1e-4
    min_conductance: float = 1e-6
    noise_level: float = 0.02
    drift_enabled: bool = True
    temperature_celsius: float = 25.0
    enable_stuck_at_faults: bool = False
    fault_rate: float = 0.001
```

## Future Extensions

- Additional device types (memristor, OxRAM)
- Advanced noise models (flicker, burst)
- Cycle counting and degradation
- On-chip learning models
