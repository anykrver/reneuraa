"""
Spike router for NeuraEdge multi-tile communication.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SpikePacket:
    """Spike event packet."""

    source_tile_id: int
    dest_tile_id: int
    neuron_id: int
    timestamp: int
    payload: float = 1.0


class SpikeRouter:
    """Routes spike packets between tiles."""

    def __init__(self, num_tiles: int):
        self.num_tiles = num_tiles
        self.packet_buffer = [[] for _ in range(num_tiles)]
        self.routing_table = self._init_routing_table()
        self.total_packets_routed = 0

    def create_packet(
        self,
        source_tile: int,
        dest_tile: int,
        neuron_id: int,
        timestamp: int
    ) -> SpikePacket:
        """Create spike packet."""
        return SpikePacket(
            source_tile_id=source_tile,
            dest_tile_id=dest_tile,
            neuron_id=neuron_id,
            timestamp=timestamp
        )

    def route_spike(self, packet: SpikePacket) -> bool:
        """
        Route spike packet to destination tile.

        Args:
            packet: SpikePacket

        Returns:
            True if successfully routed
        """
        if packet.dest_tile_id >= self.num_tiles:
            return False

        self.packet_buffer[packet.dest_tile_id].append(packet)
        self.total_packets_routed += 1
        return True

    def get_packets(self, tile_id: int) -> List[SpikePacket]:
        """
        Get all packets destined for tile.

        Args:
            tile_id: Destination tile

        Returns:
            List of spike packets
        """
        packets = self.packet_buffer[tile_id]
        self.packet_buffer[tile_id] = []
        return packets

    def _init_routing_table(self) -> np.ndarray:
        """Initialize routing table (identity for now)."""
        return np.eye(self.num_tiles, dtype=int)

    def get_statistics(self) -> dict:
        """Get routing statistics."""
        total_buffered = sum(len(buf) for buf in self.packet_buffer)
        return {
            "total_packets_routed": self.total_packets_routed,
            "buffered_packets": total_buffered,
        }
