"""Configuration parser for NeuraEdge."""

import yaml
from typing import Dict, Optional


class ConfigParser:
    """Parses YAML configuration files."""

    @staticmethod
    def load(config_path: str) -> Dict:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            return config if config else {}
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return {}

    @staticmethod
    def save(config: Dict, output_path: str):
        """
        Save configuration to YAML file.

        Args:
            config: Configuration dictionary
            output_path: Output file path
        """
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    @staticmethod
    def validate(config: Dict) -> bool:
        """
        Validate configuration.

        Args:
            config: Configuration dictionary

        Returns:
            True if valid
        """
        required_keys = ["num_tiles", "tile_size", "device_type"]
        return all(key in config for key in required_keys)

    @staticmethod
    def get_defaults() -> Dict:
        """Get default configuration."""
        return {
            "num_tiles": 4,
            "tile_size": 64,
            "device_type": "reram",
            "mode": "snn",
            "timesteps": 100,
            "quantization_bits": 8,
        }
