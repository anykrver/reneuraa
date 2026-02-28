"""
Device configuration and factory for NeuraEdge IP.
"""

from dataclasses import dataclass
from typing import Literal
from device_layer.base_device import DeviceModel
from device_layer.reram_model import ReRAMModel
from device_layer.pcm_model import PCMModel
from device_layer.sram_fallback import SRAMFallbackModel


@dataclass
class DeviceConfig:
    """Device configuration parameters."""

    device_type: Literal["reram", "pcm", "sram"] = "reram"
    max_conductance: float = 1e-4
    min_conductance: float = 1e-6
    noise_level: float = 0.02
    drift_enabled: bool = True
    temperature_celsius: float = 25.0
    enable_stuck_at_faults: bool = False
    fault_rate: float = 0.001


class DeviceFactory:
    """Factory for creating device models."""

    @staticmethod
    def create(config: DeviceConfig) -> DeviceModel:
        """Create device model based on config."""
        if config.device_type == "reram":
            return ReRAMModel(
                max_conductance=config.max_conductance,
                min_conductance=config.min_conductance
            )
        elif config.device_type == "pcm":
            return PCMModel(
                max_conductance=config.max_conductance,
                min_conductance=config.min_conductance
            )
        elif config.device_type == "sram":
            return SRAMFallbackModel(
                max_conductance=config.max_conductance,
                min_conductance=config.min_conductance
            )
        else:
            raise ValueError(f"Unknown device type: {config.device_type}")
