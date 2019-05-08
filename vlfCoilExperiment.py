#! /usr/bin/env python2

# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Vlfcoilexperiment
# Generated: Tue May  7 23:07:43 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class vlfCoilExperiment(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Vlfcoilexperiment")

        ##################################################
        # Variables
        ##################################################
        self.tuneMultiplier = tuneMultiplier = 0
        self.samp_rate = samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        _tuneMultiplier_sizer = wx.BoxSizer(wx.VERTICAL)
        self._tuneMultiplier_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_tuneMultiplier_sizer,
        	value=self.tuneMultiplier,
        	callback=self.set_tuneMultiplier,
        	label='tuneMultiplier',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._tuneMultiplier_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_tuneMultiplier_sizer,
        	value=self.tuneMultiplier,
        	callback=self.set_tuneMultiplier,
        	minimum=0,
        	maximum=48000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_tuneMultiplier_sizer)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 5000, 1000, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/tmp/magnetic-loop-rawaudio-mono-normalized.wav', True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, tuneMultiplier, 1, 0)
        self.analog_agc2_xx_0 = analog.agc2_ff(1e-1, 0.1, 0.1, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))

    def get_tuneMultiplier(self):
        return self.tuneMultiplier

    def set_tuneMultiplier(self, tuneMultiplier):
        self.tuneMultiplier = tuneMultiplier
        self._tuneMultiplier_slider.set_value(self.tuneMultiplier)
        self._tuneMultiplier_text_box.set_value(self.tuneMultiplier)
        self.analog_sig_source_x_0.set_frequency(self.tuneMultiplier)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 1000, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)


def main(top_block_cls=vlfCoilExperiment, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
