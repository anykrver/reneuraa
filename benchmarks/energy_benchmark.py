"""Energy benchmarking for NeuraEdge."""

import numpy as np


class EnergyBenchmark:
    """Measures energy consumption across workloads."""

    def __init__(self):
        self.measurements = []

    def measure_inference_energy(self, model, inputs, timesteps: int = 100) -> float:
        """
        Measure energy for inference.

        Args:
            model: NeuraEdge model
            inputs: Input data
            timesteps: Simulation timesteps

        Returns:
            Total energy (pJ)
        """
        # Mock energy measurement
        energy = 100.0 * timesteps + np.random.normal(0, 5)
        self.measurements.append(energy)
        return energy

    def measure_training_energy(self, model, batch_size: int, num_batches: int) -> float:
        """
        Estimate training energy.

        Args:
            model: NeuraEdge model
            batch_size: Batch size
            num_batches: Number of batches

        Returns:
            Total energy (pJ)
        """
        # Training energy is higher than inference
        energy = batch_size * num_batches * 10.0
        self.measurements.append(energy)
        return energy

    def get_average_energy(self) -> float:
        """Return average measured energy."""
        if not self.measurements:
            return 0.0
        return np.mean(self.measurements)

    def get_energy_breakdown(self) -> dict:
        """Return estimated energy breakdown."""
        return {
            "dac": 0.25,
            "adc": 0.35,
            "crossbar": 0.30,
            "neurons": 0.10,
        }
