# NeuraEdge Architecture Specification

## Overview

NeuraEdge is a modular neuromorphic computing platform designed for event-driven inference at the edge. This document defines the architecture, dataflow, and interface specifications.

## System Architecture

```
┌─────────────────────────────────────────┐
│       Application Layer (API/SDK)       │
├─────────────────────────────────────────┤
│    Execution Engine & Scheduler         │
├─────────────────────────────────────────┤
│  Hybrid Compute    │  Routing  │ Memory │
├─────────────────────────────────────────┤
│ NeuraTile Array (Tile0...TileN)         │
│ ┌──────────────┐ ┌──────────────┐      │
│ │ Crossbar 64x │ │ Neuron Clust │      │
│ │ ReRAM/PCM    │ │ LIF Neurons  │      │
│ └──────────────┘ └──────────────┘      │
├─────────────────────────────────────────┤
│    Device Layer (ReRAM/PCM Models)      │
├─────────────────────────────────────────┤
│  Power Engine   │  Power Supply         │
└─────────────────────────────────────────┘
```

## Tile Architecture

Each NeuraTile contains:

1. **Crossbar Array** (64×64)
   - Memristive weights
   - ADC/DAC for I/O
   - IR drop modeling

2. **Neuron Cluster** (64 neurons)
   - LIF neuron model
   - Threshold detection
   - Refractory period tracking

3. **Local Buffers**
   - Input buffer (16KB)
   - Output buffer (16KB)
   - Weight cache

4. **Power Monitor**
   - Per-component energy tracking
   - Real-time power estimation

## Execution Modes

- **SNN Mode**: Event-driven spike processing
- **Dense Mode**: Standard MAC operations
- **Hybrid Mode**: Automatic mode switching based on sparsity

## Device Layer

Supports multiple memory technologies:

- **ReRAM**: High conductance variation, temporal drift
- **PCM**: Stronger drift, asymmetric read/write
- **SRAM**: Reference comparison (ideal device)

Each device includes:
- Conductance programming model
- Noise injection (Gaussian, RTN)
- Temporal drift modeling
- Temperature effects

## Power Model

Total energy per cycle:

```
E_total = E_DAC + E_ADC + E_Crossbar + E_Neuron + E_Router
```

Where:
- E_DAC: Digital-to-analog conversion
- E_ADC: Analog-to-digital conversion
- E_Crossbar: Memristive read operations
- E_Neuron: Spike generation and integration
- E_Router: Inter-tile spike routing

## Routing Architecture

### Mesh Topology
- 2D mesh network with dimension-order routing
- Spike packet format: [Source | Dest | Neuron_ID | Timestamp | Payload]
- Arbitration policies: Round-robin, priority-based, FIFO

## Memory Hierarchy

1. **On-Tile Buffers** (16KB each)
   - Low latency, high power
   - Single-tile scope

2. **Global SRAM** (256KB)
   - Medium latency
   - Shared across tiles
   - Weight storage and inter-tile buffers

3. **Quantization**
   - 4-bit, 8-bit, 16-bit weight formats
   - Dynamic range compression

## API Interface

See `api/` for public interfaces:
- `NeuraEdge`: Main platform API
- `NeuraEdgeSDK`: High-level SDK wrapper
- `ConfigParser`: Configuration management

## Performance Targets

- Latency: 1-10ms per inference
- Power: 50-200 mW (full system)
- Efficiency: 1000+ ops/mJ
- Scalability: 1-16 tiles

## Future Extensions

- RTL synthesis (SystemVerilog)
- FPGA prototyping
- ASIC tape-out ready
- On-chip learning support
