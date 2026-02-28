"""
Activity tracking for power analysis.
"""

import numpy as np
from typing import Dict, List


class ActivityTracker:
    """Tracks switching activity for power analysis."""

    def __init__(self, num_tiles: int):
        self.num_tiles = num_tiles
        self.dac_switches = np.zeros(num_tiles)
        self.adc_switches = np.zeros(num_tiles)
        self.crossbar_accesses = np.zeros(num_tiles)
        self.spike_events = np.zeros(num_tiles)
        self.router_accesses = np.zeros(num_tiles)
        self.cycle_count = 0

    def log_dac_activity(self, tile_id: int, activity: int = 1):
        """Log DAC switching activity."""
        self.dac_switches[tile_id] += activity

    def log_adc_activity(self, tile_id: int, activity: int = 1):
        """Log ADC switching activity."""
        self.adc_switches[tile_id] += activity

    def log_crossbar_activity(self, tile_id: int, num_reads: int = 1):
        """Log crossbar read operations."""
        self.crossbar_accesses[tile_id] += num_reads

    def log_spike_event(self, tile_id: int, num_spikes: int = 1):
        """Log spike generation."""
        self.spike_events[tile_id] += num_spikes

    def log_router_activity(self, tile_id: int, num_packets: int = 1):
        """Log spike router activity."""
        self.router_accesses[tile_id] += num_packets

    def get_activity_report(self, tile_id: int) -> Dict:
        """Get activity report for tile."""
        return {
            "tile_id": tile_id,
            "dac_switches": int(self.dac_switches[tile_id]),
            "adc_switches": int(self.adc_switches[tile_id]),
            "crossbar_reads": int(self.crossbar_accesses[tile_id]),
            "spike_events": int(self.spike_events[tile_id]),
            "router_packets": int(self.router_accesses[tile_id]),
        }

    def get_global_activity(self) -> Dict:
        """Get global activity summary."""
        return {
            "total_dac_switches": int(np.sum(self.dac_switches)),
            "total_adc_switches": int(np.sum(self.adc_switches)),
            "total_crossbar_reads": int(np.sum(self.crossbar_accesses)),
            "total_spikes": int(np.sum(self.spike_events)),
            "total_router_packets": int(np.sum(self.router_accesses)),
            "cycle_count": self.cycle_count,
        }

    def advance_cycle(self):
        """Advance simulation cycle."""
        self.cycle_count += 1

    def reset(self):
        """Reset all counters."""
        self.dac_switches = np.zeros(self.num_tiles)
        self.adc_switches = np.zeros(self.num_tiles)
        self.crossbar_accesses = np.zeros(self.num_tiles)
        self.spike_events = np.zeros(self.num_tiles)
        self.router_accesses = np.zeros(self.num_tiles)
        self.cycle_count = 0
