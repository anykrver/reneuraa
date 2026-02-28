"""
Execution engine for NeuraEdge platform.
Coordinates multi-tile execution and mode switching.
"""

import numpy as np
from typing import List, Dict
from architecture.tile_manager import TileManager
from architecture.scheduler import TileScheduler


class ExecutionEngine:
    """Orchestrates full system execution."""

    def __init__(self, tile_manager: TileManager, num_tiles: int):
        """
        Args:
            tile_manager: TileManager instance
            num_tiles: Number of tiles
        """
        self.tile_manager = tile_manager
        self.scheduler = TileScheduler(num_tiles)
        self.current_cycle = 0
        self.global_spikes = {}
        self.execution_mode = "snn"  # snn or dense

    def set_mode(self, mode: str):
        """
        Switch execution mode.

        Args:
            mode: 'snn' or 'dense'
        """
        if mode not in ["snn", "dense"]:
            raise ValueError(f"Invalid mode: {mode}")
        self.execution_mode = mode

    def execute_layer(
        self,
        tile_id: int,
        inputs: np.ndarray,
        weights: np.ndarray = None,
        timesteps: int = 1
    ) -> Dict:
        """
        Execute a single layer on specified tile.

        Args:
            tile_id: Target tile
            inputs: Input spike train (timesteps, size)
            weights: Optional weight matrix
            timesteps: Number of time steps

        Returns:
            Dictionary with spike outputs and statistics
        """
        tile = self.tile_manager.get_tile(tile_id)

        if weights is not None:
            tile.program_weights(weights)

        outputs = []
        stats = {
            "total_spikes": 0,
            "energy_consumed": 0,
            "spike_rate": 0,
        }

        for t in range(timesteps):
            if inputs.ndim == 1:
                input_vec = inputs
            else:
                input_vec = inputs[t] if t < inputs.shape[0] else np.zeros(inputs.shape[1])

            spike_out = tile.execute_layer(input_vec, dt=1.0)
            outputs.append(spike_out)

        # Aggregate statistics
        stats["total_spikes"] = sum(len(out) for out in outputs)
        stats["energy_consumed"] = tile.power_monitor.get_total_energy()
        stats["spike_rate"] = stats["total_spikes"] / (timesteps * tile.size)

        return {
            "outputs": outputs,
            "statistics": stats,
        }

    def execute_network(self, layer_configs: List[Dict]) -> Dict:
        """
        Execute multi-layer network.

        Args:
            layer_configs: List of layer configurations
                {
                    'tile_id': int,
                    'weights': np.ndarray,
                    'inputs': np.ndarray,
                    'timesteps': int
                }

        Returns:
            Execution results
        """
        results = []
        for config in layer_configs:
            result = self.execute_layer(
                tile_id=config["tile_id"],
                inputs=config["inputs"],
                weights=config.get("weights"),
                timesteps=config.get("timesteps", 1),
            )
            results.append(result)

        self.current_cycle += 1
        return {"layers": results, "total_cycles": self.current_cycle}

    def get_power_report(self) -> Dict:
        """Get power report for entire system."""
        power_data = self.tile_manager.get_power_summary()
        return {
            "total_energy_mj": power_data["total_energy"],
            "per_tile": power_data["per_tile"],
            "efficiency_ops_per_mj": self._estimate_efficiency(),
        }

    def _estimate_efficiency(self) -> float:
        """Estimate computational efficiency."""
        power = self.tile_manager.get_power_summary()["total_energy"]
        if power == 0:
            return 0.0
        return 1.0 / power

    def reset(self):
        """Reset execution state."""
        self.tile_manager.reset_all()
        self.current_cycle = 0
        self.global_spikes = {}
