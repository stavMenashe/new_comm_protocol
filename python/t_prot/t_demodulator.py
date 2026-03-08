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
        self.in_msg = False
        self.last_samples = []
        self.start_vec = []
        self.end_vec = []

    def decode_message(self, samps):
        message = numpy.concatenate((self.last_samples, samps), axis=0)
        ch_len = int(self.Fs * self.t) * 8 * 3
        
        while len(message) >= ch_len:
            self.decode_packet(message[:ch_len])
            message = message[ch_len - 1:]
            
        self.last_samples = message
                
    def decode_packet(self, message):
        index = 0
        jumps = int(self.Fs * self.t)
        curr_ch = ""
        size = 0
        count_fails = 0

        while index + jumps + jumps < len(message):
            symb0 = message[index]
            index += jumps
            symb1 = message[index]
            index += jumps
            symb2 = message[index]
            
            if symb0 > 1 and symb1 < 1 and symb2 < 1:
                curr_ch += "0"
                count_fails = 0
            elif symb0 > 1 and symb1 > 1 and symb2 < 1:
                curr_ch += "1"
                count_fails = 0
            else:
                print("failed")
                count_fails += 1
                curr_ch += "0"
                if count_fails >= self.timeout:
                    self.in_msg = False
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
        index = 0
    
        if self.in_msg == False:
            index = self.find_msg(in0)
        if self.in_msg == True:
            if not (index == -1):
                self.decode_message(in0[index:])
            
        return len(input_items[0])
    
    def find_msg(self, samples):
        ch_len = int((int(self.Fs * self.t) * 8 * 3) / 500)
        
        prev = samples[0]
        index = 0
        
        while index < len(samples):
            if len(self.start_vec) == ch_len and len(self.end_vec) == ch_len:
                if abs(numpy.mean(self.start_vec) - numpy.mean(self.end_vec)) > self.epsilon:
                    self.in_msg = True
                    return index
                else:
                    self.start_vec = numpy.delete(self.start_vec, 0)
                    self.end_vec = numpy.append(self.end_vec, samples[index])
                    self.start_vec = numpy.append(self.start_vec, self.end_vec[0])
                    self.end_vec = numpy.delete(self.end_vec, 0)
                    
            elif len(self.start_vec) < ch_len:
                self.start_vec = numpy.append(self.start_vec, samples[index])
            elif len(self.end_vec) < ch_len:
                self.end_vec = numpy.append(self.end_vec, samples[index])
            index += 1
        return -1
