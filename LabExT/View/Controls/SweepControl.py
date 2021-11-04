#!/usr/bin/env python3
"""
IEF, ETH Zürich
Author(s): Boris Vukovic

"""

import logging
from tkinter import Tk, Frame
import json
import os
from copy import deepcopy
from tkinter import Label, OptionMenu, StringVar, font, NORMAL, END, _setit

from LabExT.Utils import find_dict_with_ignore, get_configuration_file_path
from LabExT.View.Controls.CustomFrame import CustomFrame


# TODO: Write code
class SweepParameterMenu(Frame):
    """
    Frame which contains the menu to add and remove parameter sweeps
    """

    def __init__(self, parent, experiment_manager):
        """
        # Constructor
        :param parent: Parent frame
        :param experiment_manager: Experiment manager
        """
        super(SweepParameterMenu, self).__init__(parent)

        self.logger = logging.getLogger()
        self._experiment_manager = experiment_manager
        self.__setup__()

    def __setup__(self):
        """
        Setup the CustomTable containing all devices
        """
        pass
