"""
Energy/power model for NeuraEdge platform.
Calculates DAC, ADC, crossbar, and neuron energy consumption.
"""

import numpy as np


class EnergyModel:
    """Comprehensive energy model."""

    def __init__(self):
        """Initialize energy coefficients (pJ per operation)."""
        self.e_dac_per_access = 0.1  # pJ
        self.e_adc_per_access = 0.15  # pJ
        self.e_crossbar_per_read = 0.05  # pJ per (input * output)
        self.e_neuron_per_spike = 0.05  # pJ
        self.e_router_per_spike = 0.02  # pJ
        self.e_memory_per_read = 0.08  # pJ

    def energy_dac(self, num_inputs: int, num_accesses: int) -> float:
        """
        DAC energy: converting digital weights to analog voltages.

        Args:
            num_inputs: Number of input lines
            num_accesses: Number of DAC accesses

        Returns:
            Total DAC energy (pJ)
        """
        return num_inputs * num_accesses * self.e_dac_per_access

    def energy_adc(self, num_outputs: int, num_reads: int) -> float:
        """
        ADC energy: converting analog currents to digital.

        Args:
            num_outputs: Number of output lines
            num_reads: Number of ADC reads

        Returns:
            Total ADC energy (pJ)
        """
        return num_outputs * num_reads * self.e_adc_per_access

    def energy_crossbar(self, matrix_size: int, num_reads: int) -> float:
        """
        Crossbar read energy (memristor programming assumed separate).

        Args:
            matrix_size: Crossbar dimensions (matrix_size x matrix_size)
            num_reads: Number of read operations

        Returns:
            Total crossbar energy (pJ)
        """
        return matrix_size * matrix_size * num_reads * self.e_crossbar_per_read

    def energy_neurons(self, num_spikes: int) -> float:
        """
        Neuron spike generation energy.

        Args:
            num_spikes: Total number of spikes generated

        Returns:
            Total neuron energy (pJ)
        """
        return num_spikes * self.e_neuron_per_spike

    def energy_routing(self, num_spike_packets: int) -> float:
        """
        Spike routing energy.

        Args:
            num_spike_packets: Number of spike packets routed

        Returns:
            Total routing energy (pJ)
        """
        return num_spike_packets * self.e_router_per_spike

    def energy_memory(self, num_reads: int, num_writes: int) -> float:
        """
        Memory access energy.

        Args:
            num_reads: Number of read operations
            num_writes: Number of write operations

        Returns:
            Total memory energy (pJ)
        """
        return (num_reads + num_writes) * self.e_memory_per_read

    def total_energy(
        self,
        num_inputs: int,
        num_outputs: int,
        matrix_size: int,
        num_reads: int,
        num_spikes: int,
        num_memory_ops: int = 0
    ) -> float:
        """
        Calculate total energy for an operation.

        Args:
            num_inputs: Number of inputs
            num_outputs: Number of outputs
            matrix_size: Crossbar matrix size
            num_reads: Number of crossbar reads
            num_spikes: Number of spikes generated
            num_memory_ops: Memory read + write operations

        Returns:
            Total energy (pJ)
        """
        e_dac = self.energy_dac(num_inputs, num_reads)
        e_adc = self.energy_adc(num_outputs, num_reads)
        e_xbar = self.energy_crossbar(matrix_size, num_reads)
        e_neuron = self.energy_neurons(num_spikes)
        e_memory = self.energy_memory(num_memory_ops // 2, num_memory_ops // 2)

        return e_dac + e_adc + e_xbar + e_neuron + e_memory
