# Spike Router Specification

## Overview

The spike router enables inter-tile spike communication in multi-tile NeuraEdge systems. It implements a 2D mesh topology with dimension-order routing.

## Network Topology

### 2D Mesh Layout

```
┌─────────┬─────────┬─────────┬─────────┐
│ Tile(0) │ Tile(1) │ Tile(2) │ Tile(3) │
├─────────┼─────────┼─────────┼─────────┤
│ Tile(4) │ Tile(5) │ Tile(6) │ Tile(7) │
├─────────┼─────────┼─────────┼─────────┤
│ Tile(8) │ Tile(9) │Tile(10) │Tile(11) │
├─────────┼─────────┼─────────┼─────────┤
│Tile(12) │Tile(13) │Tile(14) │Tile(15) │
└─────────┴─────────┴─────────┴─────────┘
```

For 4-tile system:
```
┌─────────┬─────────┐
│ Tile(0) │ Tile(1) │
├─────────┼─────────┤
│ Tile(2) │ Tile(3) │
└─────────┴─────────┘
```

## Spike Packet Format

### Packet Structure

```
┌───────┬────────┬──────────┬───────────┬─────────┐
│Source │  Dest  │ Neuron   │ Timestamp │ Payload │
│ ID(8) │  ID(8) │ ID(16)   │ (16)      │ (8)     │
└───────┴────────┴──────────┴───────────┴─────────┘
           64-bit packet
```

### Field Descriptions

| Field | Bits | Description |
|-------|------|-------------|
| Source ID | 8 | Source tile (0-255) |
| Dest ID | 8 | Destination tile (0-255) |
| Neuron ID | 16 | Neuron index within tile (0-65535) |
| Timestamp | 16 | Event timestamp (cycles) |
| Payload | 8 | Optional data (typically 1 for spike) |

### Example Packet

```
Spike from Tile 0, Neuron 42 → Tile 1, timestamp 150:
Encoded: 0x00_01_002A_0096_01
         0x[SRC][DST][NEUID][TIME][PL]
```

## Routing Algorithm

### Dimension-Order Routing (XY Routing)

1. Route in X (column) direction first
2. Then route in Y (row) direction
3. No deadlock possible (acyclic routing)

### Example Path

Source (0,0) → Destination (2,1):

```
Step 0: Tile (0,0)  → Emit packet
Step 1: Tile (1,0)  → X-direction (moving right)
Step 2: Tile (2,0)  → X-direction (at destination X)
Step 3: Tile (2,1)  → Y-direction (at destination)
Step 4: Destination receives packet (4 hops total)
```

### Manhattan Distance

Distance = |X_src - X_dest| + |Y_src - Y_dest|

For (0,0) to (2,1): |0-2| + |0-1| = 3 hops

## Arbitration Policies

### Round-Robin
- Fair allocation
- Prevents starvation
- Suitable for general workloads

### Priority-based
- Higher priority ID gets precedence
- Useful for latency-critical control signals
- May cause priority inversion

### FIFO
- First come, first served
- Simple to implement
- Can cause head-of-line blocking

## Latency Characteristics

### Single Packet
- Per-hop latency: 1 cycle (ideal)
- Routing decision: < 1 cycle
- Total latency for 3-hop path: 3-4 cycles

### With Contention
- Average contention delay: 0-5 cycles
- Maximum: can lead to deadlock without flow control

## Throughput

### Peak Throughput
- Per tile: 64 neurons × spike rate
- Max spike rate: 1 spike/cycle per neuron
- 4-tile system theoretical max: 256 spikes/cycle

### Practical Throughput
- With 30% spike rate: ~77 spikes/cycle
- Limited by arbitration and physical links

## Flow Control

### Buffer Management
- Per-tile input buffer: 256 packets
- Packet drop on overflow (configurable)
- Backpressure signaling (future)

### Congestion Detection
- Monitor buffer occupancy
- Measure packet drop rate
- Adaptive throttling (future enhancement)

## Power Consumption

| Component | Per Packet |
|-----------|-----------|
| Router logic | 0.02 pJ |
| Link transmission | 0.01 pJ |
| Buffer access | 0.005 pJ |
| **Total** | **0.035 pJ** |

Energy per spike hop: 0.035 pJ

## Verification Testcases

### Functional Tests
- [ ] Single packet routing
- [ ] Multi-packet routing with contention
- [ ] All-to-all communication pattern
- [ ] Dimension-order correctness
- [ ] Arbitration fairness

### Performance Tests
- [ ] Latency measurement (latency vs. distance)
- [ ] Throughput measurement (throughput vs. traffic)
- [ ] Congestion handling
- [ ] Buffer overflow behavior

### Stress Tests
- [ ] Sustained 100% traffic
- [ ] Adversarial patterns (hotspot communication)
- [ ] Random traffic
- [ ] Burst traffic

## Future Extensions

1. **Adaptive Routing**: Avoid congested paths
2. **Virtual Channels**: Deadlock prevention
3. **Quality of Service (QoS)**: Prioritize critical paths
4. **Rate Control**: Congestion-aware throttling
5. **Multi-cast Spikes**: Broadcast to multiple destinations
