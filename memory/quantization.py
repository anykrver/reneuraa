"""
Quantization schemes for NeuraEdge weights.
"""

import numpy as np
from enum import Enum


class QuantizationBits(Enum):
    """Quantization options."""

    B_4 = 4
    B_8 = 8
    B_16 = 16


class Quantizer:
    """Quantizes weights for efficient storage."""

    def __init__(self, bits: QuantizationBits = QuantizationBits.B_8):
        self.bits = bits.value
        self.levels = (1 << self.bits) - 1
        self.scale = None
        self.zero_point = None

    def quantize(self, weights: np.ndarray) -> np.ndarray:
        """
        Quantize weights to fixed-point.

        Args:
            weights: Full-precision weights

        Returns:
            Quantized weights
        """
        w_min = weights.min()
        w_max = weights.max()

        self.scale = (w_max - w_min) / self.levels
        self.zero_point = -w_min / self.scale

        quantized = np.round((weights - w_min) / self.scale)
        quantized = np.clip(quantized, 0, self.levels)

        return quantized.astype(np.uint32 if self.bits > 16 else np.uint16)

    def dequantize(self, quantized: np.ndarray) -> np.ndarray:
        """
        Dequantize back to full precision.

        Args:
            quantized: Quantized weights

        Returns:
            Full-precision weights
        """
        if self.scale is None or self.zero_point is None:
            raise ValueError("Must quantize before dequantize")

        dequantized = quantized * self.scale + (self.zero_point * self.scale)
        return dequantized

    def get_compression_ratio(self) -> float:
        """Return compression ratio vs 32-bit float."""
        return 32 / self.bits
