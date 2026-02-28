# Power Model Specification

## Energy Model Overview

NeuraEdge uses a comprehensive energy model covering all major components.

## Energy Coefficients (per operation)

Coefficients are calibrated against published ReRAM crossbar measurements.

| Component | Energy (pJ) | Scaling | Reference |
|-----------|-------------|---------|-----------|
| DAC | 2.5 | Per active input conversion | 8-bit R-2R DAC |
| ADC | 4.0 | Per output column read | 8-bit SAR ADC |
| Crossbar | 0.15 | Per MAC (input × output) | ReRAM crossbar read |
| Neuron | 0.02 | Per LIF spike event | Digital LIF update |
| Router | 0.02 | Per packet | Mesh hop |
| Memory | 0.08 | Per R/W | SRAM access |

## Energy Formula

```
E_total(pJ) = E_dac + E_adc + E_xbar + E_neuron + E_router + E_mem

where:
  E_dac    = 2.5 × num_active_inputs × num_timesteps
  E_adc    = 4.0 × num_output_columns × num_timesteps
  E_xbar   = 0.15 × num_active_inputs × num_output_columns × num_timesteps
  E_neuron = 0.02 × num_spikes
  E_router = 0.02 × num_spike_packets
  E_mem    = 0.08 × (num_reads + num_writes)
```

## Power Estimation

Real-time power is estimated as:

```
P_mW = E_cycle(pJ) × Frequency(MHz) / 1000
```

## Voltage Scaling

Dynamic power scales as V² for circuits + linear for leakage:

```
P(V) = 0.7 × (V/V_nom)² + 0.3 × (V/V_nom)
```

Nominal voltage: 0.8V

## Frequency Scaling

Frequency scales approximately with voltage in a simplified model:

```
f(V) = max(f_nom × (V/V_nom - 0.2), 0.5 × f_nom)
```

## Temperature Effects

Device conductance has temperature coefficient:

```
G(T) = G_ref × (1 - 0.001 × (T - 25))  // -0.1% per °C
L(T) = L_ref × (1 + 0.05 × (T - 25))   // +5% per °C (leakage)
```

Thermal model:
- Thermal resistance: 10°C/W
- Time constant: 0.1s

## Measurement Methodology

1. **Activity Tracking**: Monitor all DAC/ADC accesses, spike events
2. **Energy Summation**: Accumulate energy per component
3. **Calibration**: Compare simulation vs. silicon measurements
4. **Power Projection**: Scale to real frequency/voltage

## Validation Targets

- Crossbar read energy: ±10% accuracy
- Neuron energy: ±15% accuracy
- Overall system power: ±20% accuracy

## References

- ReRAM power: [Industry paper reference]
- ADC/DAC energy: [Standard cell library data]
- Neuron models: [Neuromorphic literature]
