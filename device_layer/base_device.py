"""
Base device model abstraction for NeuraEdge IP.
All physical devices (ReRAM, PCM, SRAM) inherit from DeviceModel.
"""

from abc import ABC, abstractmethod
import numpy as np


class DeviceModel(ABC):
    """Abstract base class for physical device models."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def program(self, conductance: float) -> float:
        """
        Program device to target conductance.
        Args:
            conductance: Target conductance value
        Returns:
            Actual programmed conductance (may differ due to noise/drift)
        """
        pass

    @abstractmethod
    def read(self, voltage: float) -> float:
        """
        Read current from device at given voltage.
        Args:
            voltage: Applied voltage
        Returns:
            Read current
        """
        pass

    @abstractmethod
    def update_drift(self, time_elapsed: float):
        """Update device state due to temporal drift."""
        pass

    @abstractmethod
    def inject_noise(self) -> float:
        """Return noise contribution to current."""
        pass
