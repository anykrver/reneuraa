# Hybrid Compute Specification

## Overview

NeuraEdge supports multiple compute modes optimized for different workload characteristics:
- **SNN Mode**: Event-driven spike processing
- **Dense Mode**: Standard neural network inference
- **Hybrid Mode**: Automatic mode selection

## SNN (Spiking Neural Network) Mode

### Characteristics
- Event-driven computation
- Sparsity-based power efficiency
- Temporal dynamics
- Lower average power, higher latency variance

### Execution Model

```
Input Spikes (Spiking Train)
    ↓
    ├─ Timestep 0: Integrate input → spike?
    ├─ Timestep 1: Integrate input → spike?
    ├─ ...
    └─ Timestep N: Final output count
    ↓
Output Spike Count
```

### Energy Efficiency

- Power scales with spike rate
- 10% spike rate: ~12 mW
- 50% spike rate: ~60 mW
- 100% spike rate (dense): ~120 mW

### Implementation

- Uses LIF neuron model
- Configurable timesteps (default: 100)
- Accumulates spikes over time

## Dense Mode

### Characteristics
- Standard matrix-multiply accumulate (MAC)
- Single-cycle throughput
- Deterministic latency
- Higher minimum power

### Execution Model

```
Input Vector (continuous)
    ↓
Analog Current Output
    ↓
ADC Quantization
    ↓
Digital Output
```

### Performance
- Latency: 1 cycle per layer
- Throughput: 64×64 MACs/cycle
- Deterministic behavior

### Implementation
- Direct matrix multiplication
- ReLU activation between layers
- Layer-by-layer processing

## Hybrid Mode

### Mode Selection Strategy

```python
def select_mode(sparsity):
    if sparsity < 0.1:  # Very sparse
        return "SNN"
    elif sparsity > 0.8:  # Very dense
        return "Dense"
    else:
        return "SNN"  # Default to SNN for power
```

### Sparsity Definition

Sparsity = (Number of zeros) / (Total elements)

- Low sparsity (0-0.3): Use Dense mode
- High sparsity (0.7-1.0): Use SNN mode
- Medium sparsity (0.3-0.7): Use SNN mode (safer for power)

### Mode Switching Overhead

- Context save/restore: ~10 cycles
- Minimal performance impact for per-layer switching
- Can reduce switching frequency to bundle layers

## Detailed Mode Comparison

| Attribute | SNN | Dense | Notes |
|-----------|-----|-------|-------|
| Power Scaling | O(spike_rate) | Constant | SNN more efficient for sparse |
| Latency | 100-500 cycles | ~1 cycle | Dense much faster |
| Area (typical) | 64×64 crossbar | 64×64 crossbar | Same hardware |
| Precision | Spike count | 8-16 bit | Dense higher precision |
| Throughput | 6.4 ops/ns (50% sparse) | 41 ops/ns | Dense ~6.4× faster |

## Configuration

### SNN Mode Parameters

```yaml
mode: snn
timesteps: 100              # Simulation timesteps
spike_threshold: 1.0        # LIF threshold
tau_membrane: 20.0          # Time constant (ms)
refractory_period: 2.0      # Refractory (ms)
```

### Dense Mode Parameters

```yaml
mode: dense
quantization_bits: 8        # Output quantization
activation: relu            # Activation function
```

### Hybrid Mode Parameters

```yaml
mode: hybrid
sparsity_threshold: 0.3     # Switch threshold
auto_tune: true             # Learn optimal threshold
```

## Performance Characteristics

### SNN Mode Power Efficiency

```
Spike Rate vs Power (100 timesteps):

100% ├─────════════════════ 120 mW
 75% ├──────═════════════ 90 mW
 50% ├────────═════════ 60 mW
 25% ├──────────═════ 30 mW
 10% ├───────────═ 12 mW
  0% ├───────────────── 5 mW
     └──────────────────────
      0    25    50    75    100
           Spike Rate (%)
```

### Dense Mode Latency

```
Input → MAC → ADC → Output
  1c      1c    1c     Total: 3 cycles per layer
```

## Verification

### SNN Verification
- [ ] Spike count accuracy
- [ ] Voltage integration correctness
- [ ] Refractory period enforcement
- [ ] Temporal dynamics validation

### Dense Verification
- [ ] MAC output correctness
- [ ] ADC quantization accuracy
- [ ] Activation function correctness
- [ ] Deterministic behavior

### Hybrid Verification
- [ ] Mode switching correctness
- [ ] Output consistency across modes
- [ ] Sparsity detection accuracy
- [ ] Performance overhead measurement

## Future Extensions

1. **Batch Dense Processing**: Process multiple inputs in parallel
2. **Recurrent Connections**: SNN with feedback loops
3. **Online Learning**: Spike-Timing-Dependent Plasticity (STDP)
4. **Mixed-Precision**: Different precisions per layer
5. **Temporal Batching**: Process multiple timesteps in parallel
