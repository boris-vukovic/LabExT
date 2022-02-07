#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LabExT  Copyright (C) 2021  ETH Zurich and Polariton Technologies AG
This program is free software and comes with ABSOLUTELY NO WARRANTY; for details see LICENSE file.
"""

import json
import logging
import os
from tkinter import DoubleVar, StringVar, BooleanVar, IntVar, Label, Entry, Checkbutton, filedialog, Button, \
    OptionMenu, TclError, NORMAL, DISABLED

from LabExT.Measurements.MeasAPI import *
from LabExT.Utils import get_configuration_file_path
from LabExT.View.Controls.CustomFrame import CustomFrame


class SingleSweepParameterFrame(CustomFrame):
    """A ui control that creates a table from a given set of
    parameters so they can easily be set from the ui."""

    def __init__(self, parent, customwidth=20, store_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._selected_parameter = StringVar()
        self._selected_parameter.set('-')
        self._selected_parameter.trace('w', self.on_selected_parameter_changed)
        self._sweep_parameter_options_list = ['-']

        # StringVars for Entries
        self._start = StringVar()
        self._stop = StringVar()
        self._number_of_values = StringVar()

        self._start.set('')
        self._stop.set('')
        self._number_of_values.set('')

        self._root = parent  # keep reference to the ui parent
        self._customwidth = customwidth
        self.store_callback = store_callback
        self.__setup__()  # draw the table

    def __setup__(self):
        self.clear()  # remove all existing ui controls from the table

        """
        if self.sweep_parameter is None:
            return
        """
        if self.get_selected_parameter() == '-':
            entry_state = DISABLED
        else:
            entry_state = NORMAL

        # Select Measurement Parameter
        self.menu = self.add_widget(
            OptionMenu(self, self._selected_parameter, *self._sweep_parameter_options_list),
            row=1, column=0, padx=2, pady=2, sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Start Parameter
        self.add_widget(Label(self, text='Start'),
                        row=0,
                        column=1,
                        padx=5,
                        sticky='w')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.add_widget(Entry(self,
                              textvariable=self._start,
                              width=self._customwidth,
                              state=entry_state),
                        row=0,
                        column=2,
                        padx=5,
                        sticky='we')
        self.columnconfigure(2, weight=2)

        # Stop Parameter
        self.add_widget(Label(self, text='Stop'),
                        row=1,
                        column=1,
                        padx=5,
                        sticky='w')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.add_widget(Entry(self,
                              textvariable=self._stop,
                              width=self._customwidth,
                              state=entry_state),
                        row=1,
                        column=2,
                        padx=5,
                        sticky='we')
        self.columnconfigure(2, weight=2)

        # Number of Points
        self.add_widget(Label(self, text='Number of Points'),
                        row=2,
                        column=1,
                        padx=5,
                        sticky='w')
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.add_widget(Entry(self,
                              textvariable=self._number_of_values,
                              width=self._customwidth,
                              state=entry_state),
                        row=2,
                        column=2,
                        padx=5,
                        sticky='we')
        self.columnconfigure(2, weight=2)

    @property
    def sweep_parameter_options(self):
        """Gets the measurement parameter which can be swept."""
        return self._sweep_parameter_options_list

    @sweep_parameter_options.setter
    def sweep_parameter_options(self, parameter_list):
        """Sets the parameter."""
        self._sweep_parameter_options_list = ['-'] + parameter_list
        self.__setup__()

    def set_standard_empty_sweep_parameters(self):
        """Sets standard parameters when a new sweep is created"""
        self._selected_parameter.set('-')
        self._start.set('0.0')
        self._stop.set('1.0')
        self._number_of_values.set('10')

    def get_selected_parameter(self):
        return self._selected_parameter.get()

    def on_selected_parameter_changed(self, *args):
        """Called when the value of the selected parameter in the options menu is selected"""
        if self._selected_parameter.get() == '-':
            self.toggle_entries(False)
        else:
            self.toggle_entries(True)

    def toggle_entries(self, state: bool):
        """
        Enables or disables the start, stop, number of values entries
        :param state: True for enable, False for disable
        :return: None
        """
        for k, widget in self.children.items():
            if widget.winfo_class() == 'Entry':
                if state:
                    widget.configure(state=NORMAL)
                else:
                    widget.configure(state=DISABLED)

    def write_back_sweep_values(self):
        self.store_callback(self._selected_parameter.get(),
                            self._start.get(),
                            self._stop.get(),
                            self._number_of_values.get())

    def destroy(self):
        try:
            self.write_back_sweep_values()
        except ValueError as e:
            logging.getLogger().warning(
                "Encountered invalid parameter values! Did not save changed parameters! Full Errors:\n" + str(e))
        CustomFrame.destroy(self)

    def make_json_able(self):
        data = {'sweep_parameter_name': self._selected_parameter.get(),
                'sweep_start': self._start.get(),
                'sweep_stop': self._stop.get(),
                'sweep_number_of_values': self._number_of_values.get()}
        return data

    def serialize(self, file_name):
        data = self.make_json_able()
        file_path = get_configuration_file_path(file_name)
        with open(file_path, 'w') as json_file:
            json_file.write(json.dumps(data))
        return True

    def deserialize(self, file_name):
        file_path = get_configuration_file_path(file_name)
        if not os.path.isfile(file_path):
            return False
        with open(file_path, 'r') as json_file:
            data = json.loads(json_file.read())

            try:
                self._selected_parameter.set(data['sweep_parameter_name'])
                self._start.set(data['sweep_start'])
                self._stop.set(data['sweep_stop'])
                self._number_of_values.set(data['sweep_number_of_values'])
            except KeyError as e:
                logging.getLogger().warning(
                    "Could not deserialize sweep parameters because keywords not found in settings file:\n" + str(e))
                self.set_standard_empty_sweep_parameters()

        self.__setup__()
        return True
