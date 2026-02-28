"""
NeuraTile: Core compute tile for NeuraEdge.
Combines crossbar array, neuron cluster, and local scheduling.
"""

import numpy as np
from architecture.crossbar_array import CrossbarArray
from architecture.neuron_cluster import NeuronCluster
from device_layer.base_device import DeviceModel


class NeuraTile:
    """Single compute tile with local crossbar and neurons."""

    def __init__(self, tile_id: int, size: int, device_model: DeviceModel):
        """
        Args:
            tile_id: Unique tile identifier
            size: Crossbar size (size x size)
            device_model: Device model for this tile
        """
        self.tile_id = tile_id
        self.size = size
        self.crossbar = CrossbarArray(size, device_model)
        self.neurons = NeuronCluster(size)
        self.power_monitor = TilePowerMonitor()
        self.local_spikes = []
        self.input_spikes = []

    def program_weights(self, weight_matrix: np.ndarray):
        """
        Program weights into crossbar.

        Args:
            weight_matrix: Weight matrix (size x size)
        """
        self.crossbar.program_weights(weight_matrix)

    def execute_layer(self, input_vector: np.ndarray, dt: float = 1.0) -> np.ndarray:
        """
        Execute single time step: crossbar read -> neuron integration.

        Args:
            input_vector: Input spike/current vector (size,)
            dt: Time step

        Returns:
            Spike indices for this time step
        """
        # Crossbar read
        output_currents = self.crossbar.read_outputs(input_vector)

        # Update power monitor
        self.power_monitor.add_activity(output_currents, input_vector)

        # Neuron integration
        spikes = self.neurons.integrate(output_currents, dt)
        self.local_spikes = spikes

        return np.array(spikes)

    def update_device_state(self, time_elapsed: float):
        """Update device drift and temporal effects."""
        self.crossbar.update_drift(time_elapsed)

    def reset(self):
        """Reset tile state."""
        self.neurons.reset()
        self.local_spikes = []
        self.input_spikes = []
        self.power_monitor.reset()

    def get_statistics(self) -> dict:
        """Return tile statistics."""
        return {
            "tile_id": self.tile_id,
            "total_spikes": np.sum(self.neurons.get_spike_counts()),
            "power_estimate": self.power_monitor.get_total_energy(),
            "membrane_potentials": self.neurons.get_membrane_potentials(),
        }


class TilePowerMonitor:
    """Monitor power consumption per tile."""

    def __init__(self):
        self.total_energy = 0.0
        self.dac_energy = 0.0
        self.adc_energy = 0.0
        self.crossbar_energy = 0.0
        self.neuron_energy = 0.0
        self.activity_count = 0

    def add_activity(self, output_currents: np.ndarray, input_vector: np.ndarray):
        """
        Log activity for energy estimation.
        Coefficients calibrated to match published ReRAM crossbar measurements:
          - DAC: ~2.5 pJ per active input conversion (8-bit R-2R DAC)
          - ADC: ~4.0 pJ per output column read (8-bit SAR ADC)
          - Crossbar: ~0.15 pJ per MAC operation (dominant consumer)
          - Neurons: ~0.02 pJ per LIF spike event (lightweight digital)

        Args:
            output_currents: Crossbar output currents
            input_vector: Input voltages
        """
        n_active_inputs = int(np.sum(np.abs(input_vector) > 0))
        n_cols = len(output_currents)
        num_spikes = int(np.sum(output_currents > 0))

        # DAC: per active input conversion
        self.dac_energy += n_active_inputs * 2.5
        # ADC: per output column read
        self.adc_energy += n_cols * 4.0
        # Crossbar: per MAC operation (active_inputs × output_columns)
        self.crossbar_energy += n_active_inputs * n_cols * 0.15
        # Neurons: per spike event only (lightweight)
        self.neuron_energy += num_spikes * 0.02

        self.activity_count += 1
        self.total_energy = (
            self.dac_energy + self.adc_energy + self.crossbar_energy + self.neuron_energy
        )

    def get_total_energy(self) -> float:
        """Return estimated total energy."""
        return self.total_energy

    def reset(self):
        """Reset power monitor."""
        self.total_energy = 0.0
        self.dac_energy = 0.0
        self.adc_energy = 0.0
        self.crossbar_energy = 0.0
        self.neuron_energy = 0.0
        self.activity_count = 0
