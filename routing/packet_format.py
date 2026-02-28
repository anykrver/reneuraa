"""
Spike packet format definition.
"""

from dataclasses import dataclass
import struct
from typing import Tuple


@dataclass
class PacketFormat:
    """Standard spike packet format for NeuraEdge."""

    SOURCE_BITS = 8  # Max 256 tiles
    DEST_BITS = 8
    NEURON_BITS = 16  # Max 65536 neurons per tile
    TIMESTAMP_BITS = 16
    PAYLOAD_BITS = 8

    @staticmethod
    def encode_packet(source: int, dest: int, neuron_id: int, timestamp: int, payload: int = 1) -> int:
        """
        Encode packet into 64-bit integer.

        Format: [source(8) | dest(8) | neuron(16) | timestamp(16) | payload(8)]

        Args:
            source: Source tile ID
            dest: Destination tile ID
            neuron_id: Neuron index
            timestamp: Event timestamp
            payload: Payload data

        Returns:
            64-bit encoded packet
        """
        packet = 0
        packet |= (source & 0xFF) << 56
        packet |= (dest & 0xFF) << 48
        packet |= (neuron_id & 0xFFFF) << 32
        packet |= (timestamp & 0xFFFF) << 16
        packet |= (payload & 0xFF) << 0
        return packet

    @staticmethod
    def decode_packet(packet: int) -> Tuple[int, int, int, int, int]:
        """
        Decode packet from 64-bit integer.

        Returns:
            (source, dest, neuron_id, timestamp, payload)
        """
        source = (packet >> 56) & 0xFF
        dest = (packet >> 48) & 0xFF
        neuron_id = (packet >> 32) & 0xFFFF
        timestamp = (packet >> 16) & 0xFFFF
        payload = packet & 0xFF
        return (source, dest, neuron_id, timestamp, payload)

    @staticmethod
    def get_packet_size_bits() -> int:
        """Return packet size in bits."""
        return (
            PacketFormat.SOURCE_BITS
            + PacketFormat.DEST_BITS
            + PacketFormat.NEURON_BITS
            + PacketFormat.TIMESTAMP_BITS
            + PacketFormat.PAYLOAD_BITS
        )
