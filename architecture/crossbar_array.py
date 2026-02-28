"""
Memristive crossbar array for NeuraEdge.
Implements weight programming, ADC/DAC conversion, and read current integration.
"""

import numpy as np
from device_layer.base_device import DeviceModel
from typing import List


class CrossbarArray:
    """Memristive crossbar array (e.g., 64x64)."""

    def __init__(self, size: int, device_model: DeviceModel):
        """
        Args:
            size: Crossbar dimensions (size x size)
            device_model: Device model instance (ReRAM/PCM/SRAM)
        """
        self.size = size
        self.device_model = device_model
        self.weights = np.zeros((size, size))
        self.devices = [[device_model.__class__() for _ in range(size)] for _ in range(size)]
        self.ir_drop_enabled = True
        self.adc_bits = 8
        self.dac_bits = 8

    def program_weights(self, weight_matrix: np.ndarray):
        """
        Program conductance values to crossbar.
        Weights are normalized to [0, 1] and mapped to conductance.

        Args:
            weight_matrix: Input weights (size x size)
        """
        assert weight_matrix.shape == (self.size, self.size)
        self.weights = weight_matrix.copy()

        # Normalize to [0, 1]
        if weight_matrix.max() > 0:
            normalized = weight_matrix / weight_matrix.max()
        else:
            normalized = weight_matrix

        # Program each device
        for i in range(self.size):
            for j in range(self.size):
                target_conductance = normalized[i, j] * self.device_model.max_conductance
                self.devices[i][j].program(target_conductance)

    def read_outputs(self, input_vector: np.ndarray) -> np.ndarray:
        """
        Apply input voltages and read crossbar output currents.

        Args:
            input_vector: Input voltages (size,)

        Returns:
            Output currents (size,)
        """
        assert input_vector.shape == (self.size,)
        outputs = np.zeros(self.size)

        for j in range(self.size):  # Output lines
            for i in range(self.size):  # Input lines
                current = self.devices[i][j].read(input_vector[i])
                noise = self.devices[i][j].inject_noise()
                outputs[j] += current + noise

        # IR drop effect (simplified)
        if self.ir_drop_enabled:
            outputs *= 0.95

        # ADC quantization
        outputs = self._quantize_adc(outputs)

        return outputs

    def update_drift(self, time_elapsed: float):
        """Update all devices for temporal drift."""
        for i in range(self.size):
            for j in range(self.size):
                self.devices[i][j].update_drift(time_elapsed)

    def _quantize_adc(self, values: np.ndarray) -> np.ndarray:
        """Quantize to ADC resolution."""
        max_val = values.max() if values.max() > 0 else 1.0
        levels = (1 << self.adc_bits) - 1
        return np.round(values / max_val * levels) / levels * max_val
