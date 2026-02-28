"""Multi-tile simulation for distributed workloads."""

import numpy as np
from architecture.tile_manager import TileManager
from routing.spike_router import SpikeRouter


class MultiTileSimulator:
    """Simulates multi-tile execution with routing."""

    def __init__(self, tile_manager: TileManager, num_tiles: int):
        """
        Args:
            tile_manager: TileManager instance
            num_tiles: Number of tiles
        """
        self.tile_manager = tile_manager
        self.num_tiles = num_tiles
        self.router = SpikeRouter(num_tiles)
        self.cycle_count = 0

    def execute_timestep(self, tile_inputs: dict) -> dict:
        """
        Execute single timestep across all tiles with inter-tile communication.

        Args:
            tile_inputs: {tile_id: input_vector}

        Returns:
            Spike outputs per tile
        """
        outputs = {}

        # Execute all tiles
        for tile_id, inputs in tile_inputs.items():
            spikes = self.tile_manager.execute(tile_id, inputs, dt=1.0)
            outputs[tile_id] = spikes

            # Route spikes to other tiles
            for spike_idx in spikes:
                for dest_tile in range(self.num_tiles):
                    if dest_tile != tile_id:
                        packet = self.router.create_packet(
                            source_tile=tile_id,
                            dest_tile=dest_tile,
                            neuron_id=spike_idx,
                            timestamp=self.cycle_count
                        )
                        self.router.route_spike(packet)

        self.cycle_count += 1
        return outputs

    def get_routing_statistics(self) -> dict:
        """Get routing statistics."""
        return self.router.get_statistics()

    def reset(self):
        """Reset simulator."""
        self.tile_manager.reset_all()
        self.cycle_count = 0
