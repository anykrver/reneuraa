"""MNIST benchmark for NeuraEdge."""

import numpy as np


class MNISTBenchmark:
    """MNIST inference benchmark."""

    def __init__(self, num_samples: int = 100):
        self.num_samples = num_samples
        self.results = {
            "accuracy": 0.0,
            "latency_ms": 0.0,
            "energy_mj": 0.0,
            "throughput_samples_per_sec": 0.0,
        }

    def run(self, model, test_data, test_labels) -> dict:
        """
        Run MNIST benchmark.

        Args:
            model: NeuraEdge model
            test_data: Test images
            test_labels: Test labels

        Returns:
            Benchmark results
        """
        if test_data.shape[0] < self.num_samples:
            test_data = test_data[:self.num_samples]
            test_labels = test_labels[:self.num_samples]

        correct = 0
        total_time = 0.0
        total_energy = 0.0

        for i in range(self.num_samples):
            # Mock inference timing
            start_time = 0
            output = model.forward(test_data[i])
            end_time = 1.0
            total_time += end_time - start_time

            # Prediction
            if isinstance(output, np.ndarray):
                pred = np.argmax(output)
            else:
                pred = 0

            if pred == test_labels[i]:
                correct += 1

            total_energy += 0.1  # Mock energy

        self.results["accuracy"] = correct / self.num_samples
        self.results["latency_ms"] = total_time / self.num_samples
        self.results["energy_mj"] = total_energy
        self.results["throughput_samples_per_sec"] = self.num_samples / max(total_time, 0.001)

        return self.results
