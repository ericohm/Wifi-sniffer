#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Wed Aug  5 10:51:17 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx
import sys
import time

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.4e6

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(891e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(1, 0)
        self.rtlsdr_source_0.set_gain_mode(0, 0)
        self.rtlsdr_source_0.set_gain(50, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        try:
            self.rtlsdr_source_0.get_sample_rates().start()
        except RuntimeError:
            print "Source has no sample rates (wrong device arguments?)."
            sys.exit(1)
          
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=1024,
        	ref_scale=2,
        	frame_rate=60,
        	avg_alpha=1.0,
        	average=True,
        )
        self.blocks_float_to_char_0 = blocks.float_to_char(1024, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1024, "gsm_power.txt", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.rtlsdr_source_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_file_sink_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)


def freq_hop(freq):
    print "before freq",freq
    if freq < 915000000:
        freq = freq+2400000
    else:
        freq = 891000000
    print "after freq",freq
    return freq



if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)


    for i in range(0,60):
        freq = tb.rtlsdr_source_0.get_center_freq()
        freq = freq_hop(freq)
        while (tb.rtlsdr_source_0.set_center_freq(freq, 0) == 0):
            tb.rtlsdr_source_0.set_center_freq(900000000, 0)
            print "tryin"
            time.sleep(2)
        time.sleep(0.3)

            




    tb.Start(False)

0

