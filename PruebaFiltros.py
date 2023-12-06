#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Prueba Filtros
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import numpy as np
import sip



class PruebaFiltros(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Prueba Filtros", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Prueba Filtros")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "PruebaFiltros")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 400e3
        self.periodos_tiempo = periodos_tiempo = 10
        self.min_res_rat = min_res_rat = 8/60
        self.max_res_rat = max_res_rat = 20/60
        self.max_hea_rat = max_hea_rat = 100/60
        self.freq_tone = freq_tone = samp_rate/100
        self.tx_gain = tx_gain = 43
        self.t = t = 1/min_res_rat
        self.rx_gain = rx_gain = 42
        self.n_periodos_tiempo = n_periodos_tiempo = int( np.ceil(  periodos_tiempo*samp_rate/freq_tone ) )
        self.min_hea_rat = min_hea_rat = 60/60
        self.max_fre_vital_signals = max_fre_vital_signals = max( max_hea_rat, max_res_rat)
        self.freq = freq = 5.63e9
        self.fft_size = fft_size = 1024
        self.amplitude = amplitude = 900e-3
        self.M = M = 100

        ##################################################
        # Blocks
        ##################################################

        self._tx_gain_range = Range(0, 50, 1, 43, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, "'tx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_gain_win)
        self._rx_gain_range = Range(0, 50, 1, 42, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=M,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_c(
            n_periodos_tiempo, #size
            samp_rate, #samp_rate
            "Time s_in and s_out", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_freq_sink_x_0_1_0_0_0 = qtgui.freq_sink_c(
            fft_size, #size
            window.WIN_HANN, #wintype
            0, #fc
            samp_rate, #bw
            "FFT s_in and s_out", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_0_0_0_win)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_min_output_buffer((int( fft_size/4 )))
        self.qtgui_freq_sink_x_0_1_0_0_0.set_max_output_buffer((int( fft_size*3/4 )))
        self.qtgui_freq_sink_x_0_1_0_0 = qtgui.freq_sink_f(
            fft_size, #size
            window.WIN_HANN, #wintype
            0, #fc
            samp_rate, #bw
            "Phase Frequency Sign Vitals", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_1_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_0_0_win)
        self.qtgui_freq_sink_x_0_1_0_0.set_min_output_buffer((int( fft_size/4 )))
        self.qtgui_freq_sink_x_0_1_0_0.set_max_output_buffer((int( fft_size*3/4 )))
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_f(
            fft_size, #size
            window.WIN_HANN, #wintype
            0, #fc
            (samp_rate/M), #bw
            "Phase Frequency Respiration and Heart", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                100,
                samp_rate,
                (max_fre_vital_signals+freq_tone),
                ((max_fre_vital_signals+freq_tone)/8),
                window.WIN_HANN,
                6.76))
        self.blocks_multiply_conjugate_cc_1 = blocks.multiply_conjugate_cc(1)
        self.blocks_complex_to_arg_1 = blocks.complex_to_arg(1)
        self.band_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                (samp_rate/M),
                min_hea_rat,
                max_hea_rat,
                (min(min_hea_rat, max_hea_rat)/8),
                window.WIN_HANN,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                (samp_rate/M),
                min_res_rat,
                max_res_rat,
                (min(min_res_rat, max_res_rat)/8),
                window.WIN_HANN,
                6.76))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_tone, (900e-3), 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_conjugate_cc_1, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_freq_sink_x_0_1_0_0_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0_1, 1))
        self.connect((self.blocks_complex_to_arg_1, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_complex_to_arg_1, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_complex_to_arg_1, 0), (self.qtgui_freq_sink_x_0_1_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_conjugate_cc_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_1_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_arg_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "PruebaFiltros")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_freq_tone(self.samp_rate/100)
        self.set_n_periodos_tiempo(int( np.ceil(  self.periodos_tiempo*self.samp_rate/self.freq_tone ) ))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_res_rat, self.max_res_rat, (min(self.min_res_rat, self.max_res_rat)/8), window.WIN_HANN, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_hea_rat, self.max_hea_rat, (min(self.min_hea_rat, self.max_hea_rat)/8), window.WIN_HANN, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(100, self.samp_rate, (self.max_fre_vital_signals+self.freq_tone), ((self.max_fre_vital_signals+self.freq_tone)/8), window.WIN_HANN, 6.76))
        self.qtgui_freq_sink_x_0_1.set_frequency_range(0, (self.samp_rate/self.M))
        self.qtgui_freq_sink_x_0_1_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_bandwidth(self.samp_rate, 0)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_periodos_tiempo(self):
        return self.periodos_tiempo

    def set_periodos_tiempo(self, periodos_tiempo):
        self.periodos_tiempo = periodos_tiempo
        self.set_n_periodos_tiempo(int( np.ceil(  self.periodos_tiempo*self.samp_rate/self.freq_tone ) ))

    def get_min_res_rat(self):
        return self.min_res_rat

    def set_min_res_rat(self, min_res_rat):
        self.min_res_rat = min_res_rat
        self.set_t(1/self.min_res_rat)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_res_rat, self.max_res_rat, (min(self.min_res_rat, self.max_res_rat)/8), window.WIN_HANN, 6.76))

    def get_max_res_rat(self):
        return self.max_res_rat

    def set_max_res_rat(self, max_res_rat):
        self.max_res_rat = max_res_rat
        self.set_max_fre_vital_signals(max( self.max_hea_rat, self.max_res_rat))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_res_rat, self.max_res_rat, (min(self.min_res_rat, self.max_res_rat)/8), window.WIN_HANN, 6.76))

    def get_max_hea_rat(self):
        return self.max_hea_rat

    def set_max_hea_rat(self, max_hea_rat):
        self.max_hea_rat = max_hea_rat
        self.set_max_fre_vital_signals(max( self.max_hea_rat, self.max_res_rat))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_hea_rat, self.max_hea_rat, (min(self.min_hea_rat, self.max_hea_rat)/8), window.WIN_HANN, 6.76))

    def get_freq_tone(self):
        return self.freq_tone

    def set_freq_tone(self, freq_tone):
        self.freq_tone = freq_tone
        self.set_n_periodos_tiempo(int( np.ceil(  self.periodos_tiempo*self.samp_rate/self.freq_tone ) ))
        self.analog_sig_source_x_0.set_frequency(self.freq_tone)
        self.low_pass_filter_0.set_taps(firdes.low_pass(100, self.samp_rate, (self.max_fre_vital_signals+self.freq_tone), ((self.max_fre_vital_signals+self.freq_tone)/8), window.WIN_HANN, 6.76))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_t(self):
        return self.t

    def set_t(self, t):
        self.t = t

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_n_periodos_tiempo(self):
        return self.n_periodos_tiempo

    def set_n_periodos_tiempo(self, n_periodos_tiempo):
        self.n_periodos_tiempo = n_periodos_tiempo

    def get_min_hea_rat(self):
        return self.min_hea_rat

    def set_min_hea_rat(self, min_hea_rat):
        self.min_hea_rat = min_hea_rat
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_hea_rat, self.max_hea_rat, (min(self.min_hea_rat, self.max_hea_rat)/8), window.WIN_HANN, 6.76))

    def get_max_fre_vital_signals(self):
        return self.max_fre_vital_signals

    def set_max_fre_vital_signals(self, max_fre_vital_signals):
        self.max_fre_vital_signals = max_fre_vital_signals
        self.low_pass_filter_0.set_taps(firdes.low_pass(100, self.samp_rate, (self.max_fre_vital_signals+self.freq_tone), ((self.max_fre_vital_signals+self.freq_tone)/8), window.WIN_HANN, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_amplitude(self):
        return self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_res_rat, self.max_res_rat, (min(self.min_res_rat, self.max_res_rat)/8), window.WIN_HANN, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate/self.M), self.min_hea_rat, self.max_hea_rat, (min(self.min_hea_rat, self.max_hea_rat)/8), window.WIN_HANN, 6.76))
        self.qtgui_freq_sink_x_0_1.set_frequency_range(0, (self.samp_rate/self.M))




def main(top_block_cls=PruebaFiltros, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
