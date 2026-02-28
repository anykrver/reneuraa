"""NeuraEdge public API."""

from typing import Dict
import numpy as np
from architecture.tile_manager import TileManager
from architecture.execution_engine import ExecutionEngine
from device_layer.device_config import DeviceConfig, DeviceFactory


class NeuraEdge:
    """Main NeuraEdge API for users."""

    def __init__(self, config: Dict = None):
        """
        Initialize NeuraEdge platform.

        Args:
            config: Configuration dictionary
        """
        if config is None:
            config = {}

        self.config = {
            "num_tiles": config.get("num_tiles", 4),
            "tile_size": config.get("tile_size", 64),
            "device_type": config.get("device_type", "reram"),
            "mode": config.get("mode", "snn"),
        }

        # Initialize device
        device_config = DeviceConfig(device_type=self.config["device_type"])
        device = DeviceFactory.create(device_config)

        # Initialize hardware
        self.tile_manager = TileManager(
            num_tiles=self.config["num_tiles"],
            tile_size=self.config["tile_size"],
            device_model=device
        )

        self.execution_engine = ExecutionEngine(
            self.tile_manager,
            num_tiles=self.config["num_tiles"]
        )

    def program_weights(self, tile_id: int, weights: np.ndarray) -> bool:
        """
        Program weights to tile.

        Args:
            tile_id: Target tile
            weights: Weight matrix

        Returns:
            Success status
        """
        try:
            self.tile_manager.program_tile(tile_id, weights)
            return True
        except Exception as e:
            print(f"Programming error: {e}")
            return False

    def run_inference(self, tile_id: int, inputs: np.ndarray, timesteps: int = 100) -> np.ndarray:
        """
        Run inference on tile.

        Args:
            tile_id: Target tile
            inputs: Input data
            timesteps: Simulation timesteps

        Returns:
            Output spikes
        """
        result = self.execution_engine.execute_layer(
            tile_id=tile_id,
            inputs=inputs,
            timesteps=timesteps
        )
        return np.array(result["outputs"])

    def get_power_report(self) -> dict:
        """Get power report."""
        return self.execution_engine.get_power_report()

    def reset(self):
        """Reset system."""
        self.execution_engine.reset()

