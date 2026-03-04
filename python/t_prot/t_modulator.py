#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 GaliandStav.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class t_modulator(gr.sync_block):
    """
    docstring for block t_modulator
    """
    def __init__(self, t = 1, Fs = 1000, text = "Hello World From Gali and Stav!"):
        gr.sync_block.__init__(self,
            name="t_modulator",
            in_sig=None,
            out_sig=[<+numpy.float32+>, ])
        self.t = t
        self.Fs = Fs
        self.text = text


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] = whatever
        return len(output_items[0])
