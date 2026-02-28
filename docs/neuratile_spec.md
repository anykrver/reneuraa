# NeuraTile Internal Specification

## Tile Block Diagram

```
                     Input Vector (64)
                            │
                            ▼
                    ┌──────────────────┐
                    │ Input Registers  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Crossbar Array  │
                    │    (64x64)       │
                    │   ReRAM/PCM      │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
        ┌──────┐      ┌──────────┐     ┌──────────┐
        │ ADC  │      │ ADC BUF  │     │ Control  │
        │8-bit │      │          │     │ Logic    │
        └──┬───┘      └──────────┘     └──────────┘
           │                │
           │      ┌─────────▼────────┐
           │      │  Neuron Cluster  │
           │      │  (64 LIF Neurons)│
           │      └────────┬─────────┘
           │               │
           │        ┌──────▼──────┐
           │        │  Threshold  │
           │        │  Logic      │
           │        └──────┬──────┘
           │               │
           └───────────────┼─────────────────┐
                          │                 │
                    Output Spikes     Status/Control

```

## Crossbar Parameters

| Parameter | Value |
|-----------|-------|
| Size | 64×64 |
| Device | ReRAM/PCM/SRAM |
| Max Conductance | 1e-4 S |
| Min Conductance | 1e-6 S |
| ADC Resolution | 8 bit |
| DAC Resolution | 8 bit |
| IR Drop Model | 5% reduction |

## LIF Neuron Model

```
dV/dt = -(V - V_rest) / τ_m + I_in / C_m

Threshold: V_threshold = 1.0V
Refractory: 2.0 ms
Reset: V → 0
```

## Dataflow Example

### Single Timestep Execution

1. **Input Stage** (t=0)
   - Input vector [64 neurons] arrives
   - Store in input register

2. **Crossbar Read** (t=1)
   - Apply input voltages to rows
   - Read output currents from columns
   - Apply ADC quantization

3. **Neuron Integration** (t=2-3)
   - Integrate input currents
   - Check threshold
   - Generate spikes
   - Update refractory state

4. **Output** (t=4)
   - Spike indices available
   - Route to other tiles or next layer
   - Energy logged

## Performance Characteristics

- Throughput: 64 neurons/cycle at 100MHz = 6.4G ops/s
- Latency per spike: 1-4 cycles depending on model
- Memory bandwidth: 8.2 GB/s (nominal)

## Power Breakdown per Cycle

| Component | Power |
|-----------|-------|
| Crossbar Read | 12.8 mW (64×64 @ 100 pJ) |
| ADC | 9.6 mW (64 accesses @ 150 pJ) |
| DAC | 6.4 mW (64 accesses @ 100 pJ) |
| Neurons | 2.0 mW (estimated 50% spike rate) |
| Other | 5.2 mW (routing, control) |
| **Total** | **36 mW** (full utilization) |

## Verification Checklist

- [ ] Crossbar I-V linearity test
- [ ] ADC quantization verification
- [ ] LIF neuron integration accuracy
- [ ] Power measurement calibration
- [ ] Noise injection validation
- [ ] Drift modeling verification
