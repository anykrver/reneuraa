# NeuraEdge Web Dashboard Guide

## Quick Start

### Option 1: Double-Click (Easiest)
- Open `g:\neuraedge ip\` folder
- Double-click **`START_DASHBOARD.bat`**
- Opens automatically at http://localhost:8080

### Option 2: Command Line
```bash
cd "g:\neuraedge ip"
python ui/server.py
```

Then open browser: **http://localhost:8080**

---

## Web Dashboard Overview

### Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│  NeuraEdge IP Platform | Professional Neuromorphic │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [ System Config ]  [ Performance ]  [ Power ]     │
│  ├─ Tiles: 4        ├─ Energy      ├─ DAC         │
│  ├─ Size: 64x64     ├─ Efficiency  ├─ ADC         │
│  ├─ Device: ReRAM   ├─ Spikes      ├─ Crossbar    │
│  ├─ Mode: SNN       |              ├─ Neurons     │
│  └─ Neurons: 256    |              |              │
│                                                     │
│  [ Tile Status ]    [ Controls ]   [ Device Info ] │
│  ├─ Tile 0: ACTIVE  ├─ Run         ├─ MaxG: 1e-4 │
│  ├─ Tile 1: IDLE    ├─ Refresh     ├─ MinG: 1e-6 │
│  ├─ Tile 2: IDLE    ├─ Reset       ├─ Noise: 2%  │
│  └─ Tile 3: IDLE    |              └─ Drift: ON  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Key Features

#### 1. System Configuration Panel
- **Tiles**: Number of compute tiles (4)
- **Tile Size**: Crossbar dimensions (64×64)
- **Device**: Type (ReRAM/PCM/SRAM)
- **Mode**: Execution mode (SNN/Dense/Hybrid)
- **Total Neurons**: Aggregate count

#### 2. Performance Metrics
- **Total Energy**: Cumulative energy consumption (mJ)
- **Efficiency**: Computation efficiency (ops/mJ)
- **Spike Count**: Total output spikes generated
- **Auto-refreshes every 2 seconds**

#### 3. Power Consumption Breakdown
- **DAC Energy**: Digital-to-analog conversion (pJ)
- **ADC Energy**: Analog-to-digital conversion (pJ)
- **Crossbar Energy**: Memristive read operations (pJ)
- **Neuron Energy**: Spike integration and generation (pJ)

#### 4. Per-Tile Status
- Real-time status for each tile
- Active/Idle indicators
- Visual status badges

#### 5. Control Panel
- **Run Inference**: Execute single inference iteration
- **Refresh Metrics**: Manual metrics update
- **Reset System**: Clear energy counters

#### 6. Device Information
- **Max Conductance**: Maximum device conductance
- **Min Conductance**: Minimum device conductance
- **Noise Level**: Device noise variation
- **Drift Enabled**: Temporal degradation enabled

---

## API Endpoints

### 1. Get System Configuration
```bash
curl http://localhost:8080/api/system_info
```

**Response:**
```json
{
  "num_tiles": 4,
  "tile_size": 64,
  "device_type": "reram",
  "mode": "snn",
  "total_neurons": 256
}
```

### 2. Get Real-Time Metrics
```bash
curl http://localhost:8080/api/metrics
```

**Response:**
```json
{
  "total_energy": 1984.85,
  "efficiency": 0.0,
  "spike_count": 0,
  "dac_energy": 1100.0,
  "adc_energy": 5.39,
  "crossbar_energy": 79.46,
  "neuron_energy": 800.0
}
```

### 3. Run Inference
```bash
curl http://localhost:8080/api/run_inference
```

**Response:**
```json
{
  "spikes": 42,
  "energy": 2150.5
}
```

### 4. HTML Dashboard
```bash
curl http://localhost:8080/
```

Returns complete HTML dashboard page.

---

## Performance Monitoring

### Energy Tracking

The dashboard monitors energy consumption across:

| Component | Typical Value | Notes |
|-----------|--------------|-------|
| DAC | 1100 pJ | Voltage conversion per timestep |
| ADC | 5-10 pJ | Quantization per timestep |
| Crossbar | 50-100 pJ | Memristor read operations |
| Neurons | 800-1000 pJ | LIF integration |
| **Total** | **~2000 pJ** | Per 100-timestep inference |

### Efficiency Metrics

- **ops/mJ**: Operations per millijoule
- **Scales with spike rate**: Higher sparsity = better efficiency
- **Power breakdown**: See which component dominates

---

## Troubleshooting

### Port Already in Use
If port 8080 is occupied:

1. Find process using port 8080
2. Modify `ui/server.py` line 441: `server_address = ('', 8080)` → change `8080`
3. Restart server

### Browser Won't Connect
- Check: Is Python running?
- Check: Terminal shows "Server running at http://localhost:8080"?
- Try: http://127.0.0.1:8080 instead of localhost

### Metrics Not Updating
- Click "Refresh Metrics" button
- Check browser console (F12) for errors
- Verify API endpoints: curl http://localhost:8080/api/metrics

### Special Characters Display Issue
- Some systems may not render Unicode properly
- Edit `ui/server.py` to use ASCII-only characters
- Dashboard works regardless of display issues

---

## Integration Examples

### Python Integration
```python
import requests

# Get system info
response = requests.get('http://localhost:8080/api/system_info')
config = response.json()
print(f"Tiles: {config['num_tiles']}")

# Run inference
response = requests.get('http://localhost:8080/api/run_inference')
result = response.json()
print(f"Spikes: {result['spikes']}, Energy: {result['energy']} mJ")
```

### JavaScript Integration
```javascript
// Fetch metrics
fetch('http://localhost:8080/api/metrics')
  .then(r => r.json())
  .then(data => {
    console.log(`Energy: ${data.total_energy} mJ`);
    console.log(`Efficiency: ${data.efficiency} ops/mJ`);
  });

// Run inference
fetch('http://localhost:8080/api/run_inference')
  .then(r => r.json())
  .then(data => console.log(data));
```

### cURL Examples
```bash
# One-liner to get all metrics
curl http://localhost:8080/api/system_info && \
curl http://localhost:8080/api/metrics && \
curl http://localhost:8080/api/run_inference
```

---

## Advanced Configuration

### Change Server Port
Edit `ui/server.py` line 441:
```python
server_address = ('', 9000)  # Change from 8080 to 9000
```

### Customize Workload
Edit inference generation in `ui/server.py` `run_inference()` method:
```python
# Increase noise/complexity
weights = np.random.randn(64, 64) * 0.5  # Higher variation
inputs = np.random.rand(64) * 2.0  # Stronger input
```

### Enable HTTPS
(For production use)
```python
# Use ssl module to wrap socket
import ssl
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert.pem')
```

---

## Server Management

### Graceful Shutdown
- **Keyboard interrupt**: Press Ctrl+C
- **Clean termination**: Server closes all connections
- **State preserved**: Metrics retained until next run

### Background Execution
On Windows:
```batch
start python ui/server.py
```

On Linux/Mac:
```bash
python ui/server.py &
```

### Monitor Server Health
```bash
# Check if running
curl -s http://localhost:8080/ | head -1

# Watch metrics in real-time (Linux/Mac)
watch -n 1 'curl -s http://localhost:8080/api/metrics | jq .'
```

---

## Performance Tips

### Reduce Dashboard Refresh Rate
In HTML, change line with `setInterval`:
```javascript
// Change from 2000ms to 5000ms (5 seconds)
setInterval(updateMetrics, 5000);
```

### Profile API Response Time
```bash
time curl http://localhost:8080/api/metrics
```

Typical response: <10ms

### Monitor Server Resource Usage
```bash
# Windows
tasklist | findstr python

# Linux
ps aux | grep server.py
```

---

## Support & Issues

- **Documentation**: See `docs/` folder
- **Source Code**: `ui/server.py` and `ui/dashboard.py`
- **Contributing**: Open issues on GitHub

---

**Last Updated**: 2024
**Version**: 0.1.0
**Status**: Production Ready
