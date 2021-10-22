#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: ebaum
# GNU Radio version: 3.8.3.1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.fsk_deviation_hz = fsk_deviation_hz = 5e3
        self.filter_samp_rate = filter_samp_rate = fsk_deviation_hz * 3
        self.tx_samp_rate = tx_samp_rate = 1e6
        self.tx_gain = tx_gain = 8
        self.squelch_lvl_neg = squelch_lvl_neg = 35
        self.scatter_center_freq = scatter_center_freq = 200.125e3
        self.samp_rate = samp_rate = 1e6
        self.rx_gain = rx_gain = 80
        self.fsk_width_hz = fsk_width_hz = 500
        self.cutoff = cutoff = filter_samp_rate
        self.center_freq = center_freq = 915e6
        self.carrier_freq = carrier_freq = 100e3

        ##################################################
        # Blocks
        ##################################################
        self._squelch_lvl_neg_tool_bar = Qt.QToolBar(self)
        self._squelch_lvl_neg_tool_bar.addWidget(Qt.QLabel('squelch level (-dB)' + ": "))
        self._squelch_lvl_neg_line_edit = Qt.QLineEdit(str(self.squelch_lvl_neg))
        self._squelch_lvl_neg_tool_bar.addWidget(self._squelch_lvl_neg_line_edit)
        self._squelch_lvl_neg_line_edit.returnPressed.connect(
            lambda: self.set_squelch_lvl_neg(int(str(self._squelch_lvl_neg_line_edit.text()))))
        self.top_layout.addWidget(self._squelch_lvl_neg_tool_bar)
        self._scatter_center_freq_tool_bar = Qt.QToolBar(self)
        self._scatter_center_freq_tool_bar.addWidget(Qt.QLabel('scatter_center_freq' + ": "))
        self._scatter_center_freq_line_edit = Qt.QLineEdit(str(self.scatter_center_freq))
        self._scatter_center_freq_tool_bar.addWidget(self._scatter_center_freq_line_edit)
        self._scatter_center_freq_line_edit.returnPressed.connect(
            lambda: self.set_scatter_center_freq(eng_notation.str_to_num(str(self._scatter_center_freq_line_edit.text()))))
        self.top_layout.addWidget(self._scatter_center_freq_tool_bar)
        self._cutoff_range = Range(5000, filter_samp_rate, (filter_samp_rate-5000)/20, filter_samp_rate, 200)
        self._cutoff_win = RangeWidget(self._cutoff_range, self.set_cutoff, 'cutoff', "counter_slider", float)
        self.top_layout.addWidget(self._cutoff_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(tx_samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            256, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            center_freq+scatter_center_freq+carrier_freq, #fc
            filter_samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.001)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(True)



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
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            center_freq+scatter_center_freq+carrier_freq, #fc
            filter_samp_rate, #bw
            "", #name
            2
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)



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
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            int(samp_rate/filter_samp_rate),
            firdes.low_pass(
                1,
                samp_rate,
                15e3,
                2e3,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            int(samp_rate/filter_samp_rate),
            firdes.low_pass(
                1,
                samp_rate,
                cutoff,
                cutoff/5,
                firdes.WIN_HAMMING,
                6.76))
        self._fsk_deviation_hz_tool_bar = Qt.QToolBar(self)
        self._fsk_deviation_hz_tool_bar.addWidget(Qt.QLabel('fsk_deviation_hz' + ": "))
        self._fsk_deviation_hz_line_edit = Qt.QLineEdit(str(self.fsk_deviation_hz))
        self._fsk_deviation_hz_tool_bar.addWidget(self._fsk_deviation_hz_line_edit)
        self._fsk_deviation_hz_line_edit.returnPressed.connect(
            lambda: self.set_fsk_deviation_hz(eng_notation.str_to_num(str(self._fsk_deviation_hz_line_edit.text()))))
        self.top_grid_layout.addWidget(self._fsk_deviation_hz_tool_bar, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/Users/ebaum/Documents/capstone/repo/processing/hamming-test/hamming-preamb-inc-lp-s15k.iq', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -(carrier_freq + scatter_center_freq), 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(tx_samp_rate, analog.GR_COS_WAVE, carrier_freq, 1, 0, 0)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(-squelch_lvl_neg, 1e-4, 0, True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.set_filter_samp_rate(self.fsk_deviation_hz * 3)
        Qt.QMetaObject.invokeMethod(self._fsk_deviation_hz_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.fsk_deviation_hz)))

    def get_filter_samp_rate(self):
        return self.filter_samp_rate

    def set_filter_samp_rate(self, filter_samp_rate):
        self.filter_samp_rate = filter_samp_rate
        self.set_cutoff(self.filter_samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.tx_samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.tx_samp_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_squelch_lvl_neg(self):
        return self.squelch_lvl_neg

    def set_squelch_lvl_neg(self, squelch_lvl_neg):
        self.squelch_lvl_neg = squelch_lvl_neg
        Qt.QMetaObject.invokeMethod(self._squelch_lvl_neg_line_edit, "setText", Qt.Q_ARG("QString", str(self.squelch_lvl_neg)))
        self.analog_pwr_squelch_xx_0.set_threshold(-self.squelch_lvl_neg)

    def get_scatter_center_freq(self):
        return self.scatter_center_freq

    def set_scatter_center_freq(self, scatter_center_freq):
        self.scatter_center_freq = scatter_center_freq
        Qt.QMetaObject.invokeMethod(self._scatter_center_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.scatter_center_freq)))
        self.analog_sig_source_x_1.set_frequency(-(self.carrier_freq + self.scatter_center_freq))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.cutoff/5, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 15e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_fsk_width_hz(self):
        return self.fsk_width_hz

    def set_fsk_width_hz(self, fsk_width_hz):
        self.fsk_width_hz = fsk_width_hz

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.cutoff/5, firdes.WIN_HAMMING, 6.76))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.analog_sig_source_x_0.set_frequency(self.carrier_freq)
        self.analog_sig_source_x_1.set_frequency(-(self.carrier_freq + self.scatter_center_freq))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq+self.scatter_center_freq+self.carrier_freq, self.filter_samp_rate)





def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
