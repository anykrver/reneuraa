"""
Simple HTTP server for NeuraEdge Platform Dashboard
Serves at http://localhost:8080
"""

import json
import sys
sys.path.insert(0, '.')

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import numpy as np
from api.neuraedge_api import NeuraEdge
from ui.dashboard import Dashboard

# Global platform instance
ne = None
dashboard = None

class NeuraEdgeHandler(BaseHTTPRequestHandler):
    """HTTP request handler for NeuraEdge dashboard."""

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/':
            self.serve_html()
        elif path == '/api/metrics':
            self.serve_metrics()
        elif path == '/api/run_inference':
            self.run_inference()
        elif path == '/api/system_info':
            self.serve_system_info()
        else:
            self.send_404()

    def serve_html(self):
        """Serve main dashboard HTML."""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeuraEdge IP Platform Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1e3c72;
            margin-bottom: 5px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .card h2 {
            color: #1e3c72;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 15px;
            border-bottom: 2px solid #2a5298;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child {
            border-bottom: none;
        }
        .metric-label {
            color: #666;
            font-weight: 500;
        }
        .metric-value {
            color: #2a5298;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }
        .button {
            background: #2a5298;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .button:hover {
            background: #1e3c72;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #eee;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #2a5298, #1e3c72);
            width: 0%;
            transition: width 0.3s;
        }
        .status {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.active {
            background: #d4edda;
            color: #155724;
        }
        .status.idle {
            background: #f8f9fa;
            color: #6c757d;
        }
        footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 NeuraEdge IP Platform</h1>
            <p class="subtitle">Professional Neuromorphic Computing Platform | Real-Time Dashboard</p>
        </header>

        <div class="grid">
            <!-- System Info Card -->
            <div class="card">
                <h2>System Configuration</h2>
                <div id="system-info">Loading...</div>
            </div>

            <!-- Performance Metrics Card -->
            <div class="card">
                <h2>Performance Metrics</h2>
                <div id="performance-metrics">Loading...</div>
            </div>

            <!-- Power Breakdown Card -->
            <div class="card">
                <h2>Power Consumption</h2>
                <div id="power-metrics">Loading...</div>
            </div>

            <!-- Per-Tile Status Card -->
            <div class="card">
                <h2>Tile Status</h2>
                <div id="tile-status">Loading...</div>
            </div>

            <!-- Control Panel Card -->
            <div class="card">
                <h2>Control Panel</h2>
                <button class="button" onclick="runInference()">Run Inference</button>
                <button class="button" onclick="refreshMetrics()">Refresh Metrics</button>
                <button class="button" onclick="resetSystem()">Reset System</button>
            </div>

            <!-- Device Info Card -->
            <div class="card">
                <h2>Device Information</h2>
                <div id="device-info">Loading...</div>
            </div>
        </div>

        <footer>
            <p>NeuraEdge IP Platform v0.1.0 | Real-Time Monitoring Dashboard</p>
            <p>© 2024 NeuraEdge Contributors | <a href="#" style="color: white;">Documentation</a></p>
        </footer>
    </div>

    <script>
        function updateMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('performance-metrics').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Total Energy:</span>
                            <span class="metric-value">${data.total_energy.toFixed(2)} mJ</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Efficiency:</span>
                            <span class="metric-value">${data.efficiency.toFixed(0)} ops/mJ</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Spike Count:</span>
                            <span class="metric-value">${data.spike_count}</span>
                        </div>
                    `;

                    document.getElementById('power-metrics').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">DAC Energy:</span>
                            <span class="metric-value">${data.dac_energy.toFixed(1)} pJ</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">ADC Energy:</span>
                            <span class="metric-value">${data.adc_energy.toFixed(1)} pJ</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Crossbar Energy:</span>
                            <span class="metric-value">${data.crossbar_energy.toFixed(1)} pJ</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Neuron Energy:</span>
                            <span class="metric-value">${data.neuron_energy.toFixed(1)} pJ</span>
                        </div>
                    `;

                    document.getElementById('tile-status').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Tile 0:</span>
                            <span class="status active">ACTIVE</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Tile 1:</span>
                            <span class="status idle">IDLE</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Tile 2:</span>
                            <span class="status idle">IDLE</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Tile 3:</span>
                            <span class="status idle">IDLE</span>
                        </div>
                    `;
                });

            fetch('/api/system_info')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('system-info').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Tiles:</span>
                            <span class="metric-value">${data.num_tiles}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Tile Size:</span>
                            <span class="metric-value">${data.tile_size}×${data.tile_size}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Device:</span>
                            <span class="metric-value">${data.device_type.toUpperCase()}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Mode:</span>
                            <span class="metric-value">${data.mode.toUpperCase()}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Total Neurons:</span>
                            <span class="metric-value">${data.total_neurons}</span>
                        </div>
                    `;

                    document.getElementById('device-info').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Max Conductance:</span>
                            <span class="metric-value">1e-4 S</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Min Conductance:</span>
                            <span class="metric-value">1e-6 S</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Noise Level:</span>
                            <span class="metric-value">2%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Drift Enabled:</span>
                            <span class="metric-value">TRUE</span>
                        </div>
                    `;
                });
        }

        function runInference() {
            fetch('/api/run_inference')
                .then(r => r.json())
                .then(data => {
                    alert('Inference executed!\\nSpikes: ' + data.spikes);
                    updateMetrics();
                });
        }

        function refreshMetrics() {
            updateMetrics();
            alert('Metrics refreshed');
        }

        function resetSystem() {
            if (confirm('Reset system state?')) {
                alert('System reset');
                updateMetrics();
            }
        }

        // Auto-update every 2 seconds
        updateMetrics();
        setInterval(updateMetrics, 2000);
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_metrics(self):
        """Serve JSON metrics."""
        tile_0 = ne.tile_manager.get_tile(0)
        spike_counts = tile_0.neurons.get_spike_counts()
        power = ne.get_power_report()
        pm = tile_0.power_monitor

        metrics = {
            "total_energy": power['total_energy_mj'],
            "efficiency": power['efficiency_ops_per_mj'],
            "spike_count": int(np.sum(spike_counts)),
            "dac_energy": pm.dac_energy,
            "adc_energy": pm.adc_energy,
            "crossbar_energy": pm.crossbar_energy,
            "neuron_energy": pm.neuron_energy,
        }

        self.send_json(metrics)

    def serve_system_info(self):
        """Serve system configuration."""
        info = {
            "num_tiles": ne.config['num_tiles'],
            "tile_size": ne.config['tile_size'],
            "device_type": ne.config['device_type'],
            "mode": ne.config['mode'],
            "total_neurons": ne.config['num_tiles'] * ne.config['tile_size'],
        }
        self.send_json(info)

    def run_inference(self):
        """Execute inference and return results."""
        np.random.seed(int(np.random.rand() * 1000))
        weights = np.random.randn(64, 64) * 0.3
        weights = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)
        inputs = np.random.rand(64) * 1.5
        inputs = (inputs > 0.5).astype(float)

        ne.program_weights(0, weights)
        outputs = ne.run_inference(0, inputs, timesteps=50)

        total_spikes = sum(len(s) if isinstance(s, (list, np.ndarray)) else 0 for s in outputs)
        dashboard.update()

        result = {
            "spikes": total_spikes,
            "energy": ne.get_power_report()['total_energy_mj'],
        }
        self.send_json(result)

    def send_json(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_404(self):
        """Send 404 response."""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 Not Found</h1>')

    def log_message(self, format, *args):
        """Suppress HTTP logs."""
        return


if __name__ == '__main__':
    # Initialize platform
    print("\n" + "=" * 70)
    print("Starting NeuraEdge Platform Dashboard Server")
    print("=" * 70)

    ne = NeuraEdge(config={
        "num_tiles": 4,
        "tile_size": 64,
        "device_type": "reram",
        "mode": "snn"
    })
    dashboard = Dashboard(ne)

    # Start server
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, NeuraEdgeHandler)

    print("\n[OK] Platform initialized")
    print(f"[OK] Server running at http://localhost:8080")
    print(f"[OK] {ne.config['num_tiles']} tiles x "
          f"{ne.config['tile_size']}x{ne.config['tile_size']} crossbars")
    print(f"[OK] Device: {ne.config['device_type'].upper()}")
    print("\n" + "=" * 70)
    print("Open http://localhost:8080 in your browser")
    print("Press Ctrl+C to stop server")
    print("=" * 70 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("[OK] Server stopped")
