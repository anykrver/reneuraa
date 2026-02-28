"""Router latency testing for multi-tile NeuraEdge."""

import numpy as np


class RouterLatencyTest:
    """Tests spike routing latency and throughput."""

    @staticmethod
    def measure_hop_latency(router, num_hops: int, num_packets: int = 1000) -> dict:
        """
        Measure latency vs number of hops.

        Args:
            router: SpikeRouter instance
            num_hops: Number of routing hops
            num_packets: Number of test packets

        Returns:
            Latency measurements
        """
        results = {"hops": num_hops, "avg_latency_cycles": 0, "packets_tested": num_packets}

        # Mock latency: ~1 cycle per hop
        latency = 1.0 * num_hops
        results["avg_latency_cycles"] = latency

        return results

    @staticmethod
    def measure_throughput(router, num_tiles: int, spike_rate: float) -> dict:
        """
        Measure router throughput.

        Args:
            router: SpikeRouter instance
            num_tiles: Number of tiles
            spike_rate: Spike rate per neuron (0-1)

        Returns:
            Throughput measurements
        """
        results = {
            "num_tiles": num_tiles,
            "spike_rate": spike_rate,
            "max_throughput_spikes_per_cycle": 0,
            "utilization": 0,
        }

        # Mock throughput
        max_throughput = num_tiles * 64  # 64 neurons per tile
        utilization = spike_rate * 0.8
        results["max_throughput_spikes_per_cycle"] = int(max_throughput * utilization)
        results["utilization"] = utilization

        return results

    @staticmethod
    def measure_contention(router, traffic_matrix: np.ndarray) -> dict:
        """
        Measure router contention for traffic pattern.

        Args:
            router: SpikeRouter instance
            traffic_matrix: (num_tiles, num_tiles) traffic matrix

        Returns:
            Contention measurements
        """
        results = {
            "max_contention": np.max(np.sum(traffic_matrix, axis=0)),
            "avg_contention": np.mean(np.sum(traffic_matrix, axis=0)),
            "bottleneck_tile": np.argmax(np.sum(traffic_matrix, axis=0)),
        }

        return results
