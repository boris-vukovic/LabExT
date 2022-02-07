import numpy as np
from LabExT.Measurements.MeasAPI.Measparam import MeasParamInt, MeasParamFloat, MeasParam


from LabExT.Utils import get_configuration_file_path
import json
import os


class MeasParamSweep:
    def __init__(self, measurement):
        self.settings_path = 'sweep_settings_file.json'

        self.measurement = measurement
        self._sweep_parameter_name = None
        self._start = None
        self._stop = None
        self._number_of_values = None

    def set_sweep_parameters(self, sweep_parameter_name: str, start: str, stop: str, number_of_values: str):
        """

        :param sweep_parameter_name:
        :param start:
        :param stop:
        :param number_of_values:
        :return:
        """
        try:
            start = float(start)
            stop = float(stop)
            number_of_values = int(number_of_values)
        except ValueError as e:
            raise ValueError('Could not convert sweep parameters into numbers: {}'.format(e))

        if sweep_parameter_name not in self.measurement.parameters:
            raise ValueError('Invalid sweep parameter given ')

    def set_sweep_boundaries(self, start, stop, number_of_values: int):
        """
        :param start: Start value of the parameter sweep
        :param stop: Stop value of the parameter sweep
        :param number_of_values: Number of points between start and stop (includes endpoint)
        :return: None
        """
        number_of_values = int(np.floor(number_of_values))
        if number_of_values > 0:
            self._number_of_values = number_of_values
        else:
            raise ValueError('Number of sweep values must be greater than 0.')

        if type(self.measurement.parameters[self.sweep_parameter_name]) is MeasParamFloat:
            # Swept parameter is of type float
            if start == stop:
                raise ValueError('Start and stop values for parameter sweep cannot be the same.')
            self._start = float(start)
            self._stop = float(stop)
        else:
            raise ValueError('Sweeps only support measurement parameters of type MeasParamFloat.')

        self._start = start
        self._stop = stop
        self._number_of_values = number_of_values

    def get_parameter_sweep_values(self):
        """
        Generates a list of values for the swept parameter
        :return:
        """
        return np.linspace(self._start, self._stop, num=self._number_of_values)


