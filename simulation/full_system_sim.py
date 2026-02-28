"""Full system simulator for NeuraEdge."""

import numpy as np
from architecture.execution_engine import ExecutionEngine
from power_engine.activity_tracker import ActivityTracker


class FullSystemSimulator:
    """Complete NeuraEdge system simulator."""

    def __init__(self, execution_engine: ExecutionEngine, num_tiles: int):
        """
        Args:
            execution_engine: ExecutionEngine instance
            num_tiles: Number of tiles
        """
        self.execution_engine = execution_engine
        self.num_tiles = num_tiles
        self.activity_tracker = ActivityTracker(num_tiles)
        self.cycle_count = 0
        self.simulation_log = []

    def run_inference(self, layer_configs: list, max_cycles: int = 1000) -> dict:
        """
        Run full inference simulation.

        Args:
            layer_configs: Layer configurations
            max_cycles: Maximum simulation cycles

        Returns:
            Simulation results
        """
        results = {
            "total_cycles": 0,
            "total_energy": 0.0,
            "layer_results": [],
        }

        for layer_idx, config in enumerate(layer_configs):
            layer_result = self.execution_engine.execute_layer(
                tile_id=config.get("tile_id", 0),
                inputs=config["inputs"],
                weights=config.get("weights"),
                timesteps=config.get("timesteps", 10),
            )

            results["layer_results"].append(layer_result)
            self.activity_tracker.advance_cycle()
            self.cycle_count += 1

        results["total_cycles"] = self.cycle_count
        results["total_energy"] = self.execution_engine.tile_manager.get_power_summary()["total_energy"]

        return results

    def reset(self):
        """Reset simulator."""
        self.execution_engine.reset()
        self.activity_tracker.reset()
        self.cycle_count = 0
        self.simulation_log = []

    def get_statistics(self) -> dict:
        """Get simulation statistics."""
        return {
            "total_cycles": self.cycle_count,
            "activity": self.activity_tracker.get_global_activity(),
        }
