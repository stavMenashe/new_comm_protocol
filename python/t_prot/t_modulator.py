#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 GaliandStav.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
import queue 
from gnuradio import gr

class t_modulator(gr.sync_block):
    """
    docstring for block t_modulator
    """
    def __init__(self, t = 1, Fs = 1000, text = "Hello World From Gali and Stav!"):
        gr.sync_block.__init__(self,
            name="t_modulator",
            in_sig=None,
            out_sig=[numpy.float32, ])
        self.t = t
        self.Fs = Fs
        self.text = text
        self.mod_str = queue.Queue()
        
        self.set_q()
    
    def set_q(self):
        # take the bits out of the given string.
        bits = ''.join(format(ord(i), '08b') for i in self.text)
        
        #for i in range(self.t * self.Fs):
            #self.mod_str.put(-1) # preamble

        for bit in bits:
            if bit == '0':
                for i in range(int(self.t * self.Fs)):
                    self.mod_str.put(1)
                for i in range(int(self.t * self.Fs)):
                    self.mod_str.put(-1)
                    self.mod_str.put(-1)
            else:
                for i in range(int(self.t * self.Fs)):
                    self.mod_str.put(1)
                    self.mod_str.put(1)
                for i in range(int(self.t * self.Fs)):
                    self.mod_str.put(-1)
        
    
    def work(self, input_items, output_items):
        out = output_items[0]
        
        out[:] = numpy.zeros(len(out));
        
        for i in range(min(self.mod_str.qsize(), len(out))):
            out[i] = self.mod_str.get()
        
        return len(output_items[0])
        
    def size_of_block(self):
        size = int((8192 - self.Fs * self.t) / (8 * 3 * self.Fs * self.t))
        size = size * 8 * 3 * self.Fs * self.t
        return size
    
    def decode_message(self, message):
        index = 0
        jumps = self.Fs * self.t
        curr_ch = ""
        size = 0
        count_fails = 0
        while index + jumps + jumps < len(message):
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
                if count_fails >= 8:
                    break
            
            size += 1
            if size == 8:
                dec_val = int(curr_ch, 2)
                print("-", chr(dec_val), "-", end = "")
                curr_ch = ""
                size = 0
                
            index += jumps
    
    
