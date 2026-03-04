#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 GaliandStav.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class t_demodulator(gr.sync_block):
    """
    docstring for block t_demodulator
    """
    def __init__(self, t = 1, Fs= 1000, epsilon = 0.5, timeout = 2001):
        gr.sync_block.__init__(self,
            name="t_demodulator",
            in_sig=[numpy.float32, ],
            out_sig=None)
        self.t = t
        self.Fs = Fs
        self.epsilon = epsilon
        self.timeout = timeout

    def detect_message(self, message):
        index = 0
        jumps = self.Fs * self.t
        curr_ch = ""
        size = 0
        count_fails = 0
        while index < len(message):
            symb0 = message[index]
            index += jumps
            symb1 = message[index]
            index += jumps
            symb2 = message[index]
            
            if symb0 == 1 and symb1 == -1 and symb2 == -1:
                curr_ch += "0"
                count_fails = 0
            elif symb0 == 1 and symb1 == 1 and symb2 == -1:
                curr_ch += "1"
                count_fails = 0
            else:
                count_fails += 1
                curr_ch += "0"
                if count_fails >= self.timeout:
                    break
            
            size += 1
            if size == 8:
                dec_val = int(curr_ch, 2)
                print(chr(dec_val), end = "")
                curr_ch = ""
                size = 0
                
            index += jumps
            

    def work(self, input_items, output_items):
        in0 = input_items[0]
        prev = in0[0]
        index = 1
        while index < len(in0):
            curr = in0[index]
            if abs(curr - prev) > self.epsilon:
                self.detect_message(in0[index:])
                break
            index += 1
            prev = curr
            
        return len(input_items[0])
