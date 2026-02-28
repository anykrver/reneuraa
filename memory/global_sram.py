"""
Global SRAM for NeuraEdge platform.
"""

import numpy as np
from typing import Optional


class GlobalSRAM:
    """Global memory for inter-tile communication and buffering."""

    def __init__(self, size_kB: int = 256):
        """
        Args:
            size_kB: Memory size in kilobytes
        """
        self.size_bytes = size_kB * 1024
        self.memory = bytearray(self.size_bytes)
        self.read_counter = 0
        self.write_counter = 0
        self.allocation_table = {}

    def allocate(self, name: str, size_bytes: int) -> int:
        """
        Allocate memory region.

        Args:
            name: Region name
            size_bytes: Size in bytes

        Returns:
            Starting address
        """
        if not self.allocation_table:
            start_addr = 0
        else:
            last_region = max(self.allocation_table.values(), key=lambda x: x["addr"] + x["size"])
            start_addr = last_region["addr"] + last_region["size"]

        if start_addr + size_bytes > self.size_bytes:
            raise MemoryError(f"Not enough SRAM for {name}")

        self.allocation_table[name] = {"addr": start_addr, "size": size_bytes}
        return start_addr

    def write(self, address: int, data: np.ndarray):
        """Write data to memory."""
        data_bytes = data.astype(np.float32).tobytes()
        self.memory[address : address + len(data_bytes)] = data_bytes
        self.write_counter += 1

    def read(self, address: int, size_bytes: int) -> np.ndarray:
        """Read data from memory."""
        data_bytes = bytes(self.memory[address : address + size_bytes])
        self.read_counter += 1
        return np.frombuffer(data_bytes, dtype=np.float32)

    def get_utilization(self) -> float:
        """Return memory utilization (0-1)."""
        total_allocated = sum(r["size"] for r in self.allocation_table.values())
        return total_allocated / self.size_bytes
