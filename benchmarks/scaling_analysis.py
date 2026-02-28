"""Scaling analysis for NeuraEdge tiles."""

import numpy as np


class ScalingAnalysis:
    """Analyzes power and performance scaling."""

    @staticmethod
    def power_vs_tile_size(tile_sizes: list, model_instance) -> dict:
        """
        Analyze power scaling with tile size.

        Args:
            tile_sizes: List of tile sizes to test
            model_instance: NeuraEdge model

        Returns:
            Scaling results
        """
        results = {"tile_sizes": tile_sizes, "power_mw": []}

        for size in tile_sizes:
            # Mock power measurement
            power = 0.1 * (size ** 1.5)
            results["power_mw"].append(power)

        return results

    @staticmethod
    def latency_vs_num_tiles(num_tiles_list: list, model_instance) -> dict:
        """
        Analyze latency scaling with number of tiles.

        Args:
            num_tiles_list: List of tile counts to test
            model_instance: NeuraEdge model

        Returns:
            Scaling results
        """
        results = {"num_tiles": num_tiles_list, "latency_ms": []}

        for num_tiles in num_tiles_list:
            # Mock latency scaling (sublinear)
            latency = 100.0 / np.sqrt(num_tiles)
            results["latency_ms"].append(latency)

        return results

    @staticmethod
    def efficiency_analysis(activity_rates: list, model_instance) -> dict:
        """
        Analyze efficiency at different activity levels.

        Args:
            activity_rates: List of activity rates (0-1)
            model_instance: NeuraEdge model

        Returns:
            Efficiency results
        """
        results = {"activity_rates": activity_rates, "ops_per_mj": []}

        for rate in activity_rates:
            # Mock efficiency (better at high activity)
            ops_per_mj = 1000 * rate
            results["ops_per_mj"].append(ops_per_mj)

        return results
