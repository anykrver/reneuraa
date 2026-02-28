"""SDK interface for NeuraEdge."""

from api.neuraedge_api import NeuraEdge
from typing import Optional
import numpy as np


class NeuraEdgeSDK:
    """High-level SDK interface."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SDK.

        Args:
            config_path: Path to configuration YAML
        """
        from api.config_parser import ConfigParser

        if config_path:
            config = ConfigParser.load(config_path)
        else:
            config = {}

        self.platform = NeuraEdge(config)
        self.models = {}

    def create_model(self, model_name: str, num_layers: int, layer_sizes: list):
        """
        Create a model.

        Args:
            model_name: Model identifier
            num_layers: Number of layers
            layer_sizes: Layer dimensions
        """
        self.models[model_name] = {
            "num_layers": num_layers,
            "layer_sizes": layer_sizes,
            "weights": {},
        }

    def load_weights(self, model_name: str, layer_idx: int, weights: np.ndarray):
        """
        Load weights for model layer.

        Args:
            model_name: Model identifier
            layer_idx: Layer index
            weights: Weight matrix
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        self.models[model_name]["weights"][layer_idx] = weights

    def infer(self, model_name: str, inputs: np.ndarray, tile_id: int = 0) -> np.ndarray:
        """
        Run inference.

        Args:
            model_name: Model identifier
            inputs: Input data
            tile_id: Target tile

        Returns:
            Inference outputs
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        return self.platform.run_inference(tile_id, inputs)

    def get_statistics(self) -> dict:
        """Get platform statistics."""
        return {
            "config": self.platform.config,
            "models": list(self.models.keys()),
            "power_report": self.platform.get_power_report(),
        }
