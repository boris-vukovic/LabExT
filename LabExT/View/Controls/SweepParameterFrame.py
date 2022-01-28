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
from LabExT.View.TooltipMenu import CreateToolTip


class SweepParameterMenu(CustomFrame):
    """
    Frame which contains the menu to add and remove parameter sweeps
    """

    @property
    def parameter_source(self):
        """Gets the currently set parameter list."""
        return self._sweepable_parameter_source

    @parameter_source.setter
    def parameter_source(self, source):
        """Sets the parameter list."""
        self._sweepable_parameter_source = source

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
        self.clear()  # remove all existing ui controls from the table

        if self.parameter_source is None:
            return

        self.selected_parameter = StringVar(value='')
        self.add_widget(OptionMenu(self,
                                   self.selected_parameter,
                                   [p.name for p in self.parameter_source]),
                        row=0,
                        column=1,
                        sticky='we')

        # TODO: Remove copy pasta
        # add the fields for all the parameters
        self.add_widget(OptionMenu())
        r = 0
        for parameter_name in self.parameter_source:
            parameter = self.parameter_source[parameter_name]  # get the next parameter
            self.add_widget(Label(self, text='{}:'.format(parameter_name)),
                            row=r,
                            column=0,
                            padx=5,
                            sticky='w')  # add parameter name
            self.rowconfigure(r, weight=1)
            self.columnconfigure(0, weight=1)

            if parameter.parameter_type == 'bool':
                self.add_widget(Checkbutton(self,
                                            variable=parameter.variable,
                                            state='normal' if parameter.allow_user_changes else 'disabled'),
                                row=r,
                                column=1,
                                padx=5,
                                sticky='we')
            elif parameter.parameter_type == 'dropdown':
                if not isinstance(parameter.options, list) and not isinstance(parameter.options, tuple):
                    raise ValueError(
                        "Dropdown options has to be a list or tuple, got {} instead.".format(type(parameter.options)))
                self.add_widget(OptionMenu(self,
                                           parameter.variable,
                                           *parameter.options),
                                row=r,
                                column=1,
                                sticky='we')
            else:
                self.add_widget(Entry(self,
                                      textvariable=parameter.variable,
                                      width=self._customwidth,
                                      state='normal' if parameter.allow_user_changes else 'disabled'),
                                row=r,
                                column=1,
                                padx=5,
                                sticky='we')
                self.columnconfigure(1, weight=2)

            if parameter.unit is not None:
                self.add_widget(Label(self, text='[{}]'.format(parameter.unit)),
                                row=r,
                                column=2,
                                padx=5,
                                sticky='we')  # add unit description

            # add browse button for files and folders
            if parameter.parameter_type == 'folder':
                self.add_widget(Button(self, text='browse...', command=parameter.browse_folders),
                                row=r,
                                column=2,
                                padx=5,
                                sticky='we')
            if parameter.parameter_type == 'file':
                self.add_widget(Button(self, text='browse...', command=parameter.browse_files),
                                row=r,
                                column=2,
                                padx=5,
                                sticky='we')
            if parameter.parameter_type == 'openfile':
                self.add_widget(Button(self, text='browse...', command=parameter.browse_files_open),
                                row=r,
                                column=2,
                                padx=5,
                                sticky='we')
            r += 1
