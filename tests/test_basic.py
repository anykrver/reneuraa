"""Unit tests for NeuraEdge platform."""

import pytest
import numpy as np
from device_layer.reram_model import ReRAMModel
from architecture.lif_neuron import LIFNeuron
from architecture.crossbar_array import CrossbarArray


class TestReRAMDevice:
    """Test ReRAM device model."""

    def test_programming(self):
        """Test device programming."""
        device = ReRAMModel()
        target = 5e-5
        actual = device.program(target)
        assert actual > 0
        assert device.current_conductance > 0

    def test_read(self):
        """Test read operation."""
        device = ReRAMModel()
        device.program(1e-5)
        current = device.read(0.5)
        assert current > 0


class TestLIFNeuron:
    """Test LIF neuron model."""

    def test_integration(self):
        """Test voltage integration."""
        neuron = LIFNeuron(threshold=1.0)
        input_current = 0.1
        neuron.integrate(input_current)
        assert neuron.voltage > 0

    def test_spike_generation(self):
        """Test spike generation at threshold."""
        neuron = LIFNeuron()  # default threshold=0.3
        # Integrate sufficient current to trigger spike
        spiked = False
        for _ in range(50):
            if neuron.integrate(0.5):
                spiked = True
                break
        assert spiked


class TestCrossbar:
    """Test crossbar array."""

    def test_programming(self):
        """Test weight programming."""
        device = ReRAMModel()
        crossbar = CrossbarArray(size=64, device_model=device)
        weights = np.random.rand(64, 64)
        crossbar.program_weights(weights)
        # Verify devices were programmed
        assert crossbar.weights.shape == (64, 64)

    def test_read(self):
        """Test crossbar read."""
        device = ReRAMModel()
        crossbar = CrossbarArray(size=64, device_model=device)
        weights = np.ones((64, 64)) * 0.5
        crossbar.program_weights(weights)
        inputs = np.ones(64) * 0.5
        outputs = crossbar.read_outputs(inputs)
        assert outputs.shape == (64,)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
