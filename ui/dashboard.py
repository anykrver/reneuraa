"""NeuraEdge dashboard implementation."""

import numpy as np
from typing import Dict


class Dashboard:
    """Real-time monitoring dashboard."""

    def __init__(self, neuraedge_api):
        """
        Initialize dashboard.

        Args:
            neuraedge_api: NeuraEdge API instance
        """
        self.api = neuraedge_api
        self.metrics_history = []

    def update(self):
        """Update dashboard with latest metrics."""
        metrics = {
            "timestamp": len(self.metrics_history),
            "power": self.api.get_power_report(),
            "tile_stats": self._get_tile_stats(),
        }
        self.metrics_history.append(metrics)

    def _get_tile_stats(self) -> list:
        """Get statistics per tile."""
        stats = []
        for tile_id in range(self.api.config["num_tiles"]):
            tile = self.api.tile_manager.get_tile(tile_id)
            stats.append({
                "tile_id": tile_id,
                "energy": tile.power_monitor.get_total_energy(),
                "spike_count": np.sum(tile.neurons.get_spike_counts()),
            })
        return stats

    def get_metrics(self) -> Dict:
        """Get current metrics."""
        if not self.metrics_history:
            return {}
        return self.metrics_history[-1]

    def get_history(self, window: int = 100) -> list:
        """Get metrics history."""
        return self.metrics_history[-window:]
