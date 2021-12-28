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
        self.tone_freq_khz = tone_freq_khz = 300
        self.symbol_rate = symbol_rate = 1e3
        self.filter_samp_rate = filter_samp_rate = 30e3
        self.tx_samp_rate = tx_samp_rate = 1e6
        self.tx_gain = tx_gain = 89
        self.tone_freq = tone_freq = tone_freq_khz * 1e3
        self.sps = sps = int(filter_samp_rate/symbol_rate)
        self.scatter_center_freq = scatter_center_freq = 149545.76
        self.samp_rate = samp_rate = 200e3
        self.rx_gain = rx_gain = 38
        self.pulse_width_hz = pulse_width_hz = 2000
        self.oversample = oversample = 4
        self.moving_avg_len = moving_avg_len = int(filter_samp_rate/symbol_rate * 10)
        self.freq_offset = freq_offset = -1400
        self.center_freq = center_freq = 915e6

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 89, 1, 89, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX gain (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._scatter_center_freq_tool_bar = Qt.QToolBar(self)
        self._scatter_center_freq_tool_bar.addWidget(Qt.QLabel('Scatter Freq (Hz)' + ": "))
        self._scatter_center_freq_line_edit = Qt.QLineEdit(str(self.scatter_center_freq))
        self._scatter_center_freq_tool_bar.addWidget(self._scatter_center_freq_line_edit)
        self._scatter_center_freq_line_edit.returnPressed.connect(
            lambda: self.set_scatter_center_freq(eng_notation.str_to_num(str(self._scatter_center_freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._scatter_center_freq_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = Range(0, 76, 1, 38, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX gain (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._pulse_width_hz_tool_bar = Qt.QToolBar(self)
        self._pulse_width_hz_tool_bar.addWidget(Qt.QLabel('pulse width (hz)' + ": "))
        self._pulse_width_hz_line_edit = Qt.QLineEdit(str(self.pulse_width_hz))
        self._pulse_width_hz_tool_bar.addWidget(self._pulse_width_hz_line_edit)
        self._pulse_width_hz_line_edit.returnPressed.connect(
            lambda: self.set_pulse_width_hz(int(str(self._pulse_width_hz_line_edit.text()))))
        self.top_grid_layout.addWidget(self._pulse_width_hz_tool_bar, 2, 3, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_offset_tool_bar = Qt.QToolBar(self)
        self._freq_offset_tool_bar.addWidget(Qt.QLabel('Freq Offset (Hz)' + ": "))
        self._freq_offset_line_edit = Qt.QLineEdit(str(self.freq_offset))
        self._freq_offset_tool_bar.addWidget(self._freq_offset_line_edit)
        self._freq_offset_line_edit.returnPressed.connect(
            lambda: self.set_freq_offset(eng_notation.str_to_num(str(self._freq_offset_line_edit.text()))))
        self.top_layout.addWidget(self._freq_offset_tool_bar)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(center_freq + tone_freq + scatter_center_freq, 0)
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
        self._tone_freq_khz_tool_bar = Qt.QToolBar(self)
        self._tone_freq_khz_tool_bar.addWidget(Qt.QLabel('Tone Freq (kHz)' + ": "))
        self._tone_freq_khz_line_edit = Qt.QLineEdit(str(self.tone_freq_khz))
        self._tone_freq_khz_tool_bar.addWidget(self._tone_freq_khz_line_edit)
        self._tone_freq_khz_line_edit.returnPressed.connect(
            lambda: self.set_tone_freq_khz(eng_notation.str_to_num(str(self._tone_freq_khz_line_edit.text()))))
        self.top_grid_layout.addWidget(self._tone_freq_khz_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
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
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            filter_samp_rate, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            int(samp_rate/filter_samp_rate),
            firdes.low_pass(
                0.1,
                samp_rate,
                pulse_width_hz,
                pulse_width_hz * 0.5,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_float*1, 'localhost', 5555, 1024, True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(moving_avg_len, 1/moving_avg_len, 5 * moving_avg_len, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, '/Users/ebaum/Documents/capstone/iq/tmp_ask-fulldata-30k.iq', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -freq_offset, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(tx_samp_rate, analog.GR_COS_WAVE, tone_freq, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tone_freq_khz(self):
        return self.tone_freq_khz

    def set_tone_freq_khz(self, tone_freq_khz):
        self.tone_freq_khz = tone_freq_khz
        self.set_tone_freq(self.tone_freq_khz * 1e3)
        Qt.QMetaObject.invokeMethod(self._tone_freq_khz_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.tone_freq_khz)))

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_moving_avg_len(int(self.filter_samp_rate/self.symbol_rate * 10))
        self.set_sps(int(self.filter_samp_rate/self.symbol_rate))

    def get_filter_samp_rate(self):
        return self.filter_samp_rate

    def set_filter_samp_rate(self, filter_samp_rate):
        self.filter_samp_rate = filter_samp_rate
        self.set_moving_avg_len(int(self.filter_samp_rate/self.symbol_rate * 10))
        self.set_sps(int(self.filter_samp_rate/self.symbol_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.filter_samp_rate)

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

    def get_tone_freq(self):
        return self.tone_freq

    def set_tone_freq(self, tone_freq):
        self.tone_freq = tone_freq
        self.analog_sig_source_x_0.set_frequency(self.tone_freq)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq + self.tone_freq + self.scatter_center_freq, 0)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_scatter_center_freq(self):
        return self.scatter_center_freq

    def set_scatter_center_freq(self, scatter_center_freq):
        self.scatter_center_freq = scatter_center_freq
        Qt.QMetaObject.invokeMethod(self._scatter_center_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.scatter_center_freq)))
        self.uhd_usrp_source_0.set_center_freq(self.center_freq + self.tone_freq + self.scatter_center_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(0.1, self.samp_rate, self.pulse_width_hz, self.pulse_width_hz * 0.5, firdes.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_pulse_width_hz(self):
        return self.pulse_width_hz

    def set_pulse_width_hz(self, pulse_width_hz):
        self.pulse_width_hz = pulse_width_hz
        Qt.QMetaObject.invokeMethod(self._pulse_width_hz_line_edit, "setText", Qt.Q_ARG("QString", str(self.pulse_width_hz)))
        self.low_pass_filter_0.set_taps(firdes.low_pass(0.1, self.samp_rate, self.pulse_width_hz, self.pulse_width_hz * 0.5, firdes.WIN_HAMMING, 6.76))

    def get_oversample(self):
        return self.oversample

    def set_oversample(self, oversample):
        self.oversample = oversample

    def get_moving_avg_len(self):
        return self.moving_avg_len

    def set_moving_avg_len(self, moving_avg_len):
        self.moving_avg_len = moving_avg_len
        self.blocks_moving_average_xx_0.set_length_and_scale(self.moving_avg_len, 1/self.moving_avg_len)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        Qt.QMetaObject.invokeMethod(self._freq_offset_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq_offset)))
        self.analog_sig_source_x_1.set_frequency(-self.freq_offset)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq + self.tone_freq + self.scatter_center_freq, 0)





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
