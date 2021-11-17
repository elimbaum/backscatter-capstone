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
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
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
        self.tone_freq_khz = tone_freq_khz = 100
        self.symbol_rate = symbol_rate = 1e3
        self.filter_samp_rate = filter_samp_rate = 30e3
        self.tx_samp_rate = tx_samp_rate = 1e6
        self.tx_gain = tx_gain = 60
        self.tone_freq = tone_freq = tone_freq_khz * 1e3
        self.ted_gain = ted_gain = 1
        self.sps = sps = int(filter_samp_rate/symbol_rate)
        self.scatter_center_freq = scatter_center_freq = 150942.76
        self.samp_rate = samp_rate = 1e6
        self.rx_gain = rx_gain = 45
        self.pulse_width_hz = pulse_width_hz = 4000
        self.nfilts = nfilts = 32
        self.moving_avg_len = moving_avg_len = filter_samp_rate/10
        self.loop_bw = loop_bw = 0.045
        self.freq_offset = freq_offset = -200
        self.enable_rx = enable_rx = 1
        self.damp = damp = 1
        self.center_freq = center_freq = 915e6

        ##################################################
        # Blocks
        ##################################################
        self._ted_gain_range = Range(0.1, 4, 0.1, 1, 200)
        self._ted_gain_win = RangeWidget(self._ted_gain_range, self.set_ted_gain, 'ted_gain', "counter_slider", float)
        self.top_layout.addWidget(self._ted_gain_win)
        self._loop_bw_range = Range(0, 0.1, 0.005, 0.045, 200)
        self._loop_bw_win = RangeWidget(self._loop_bw_range, self.set_loop_bw, 'loop_bw', "counter_slider", float)
        self.top_layout.addWidget(self._loop_bw_win)
        self._damp_range = Range(0.1, 5, 0.2, 1, 200)
        self._damp_win = RangeWidget(self._damp_range, self.set_damp, 'damp', "counter_slider", float)
        self.top_layout.addWidget(self._damp_win)
        self._tx_gain_range = Range(0, 89, 1, 60, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX gain (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self._rx_gain_range = Range(0, 76, 1, 45, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX gain (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_3 = qtgui.time_sink_f(
            256, #size
            filter_samp_rate, #samp_rate
            "", #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_3.enable_tags(True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.0, 0, 1, "")
        self.qtgui_time_sink_x_3.enable_autoscale(False)
        self.qtgui_time_sink_x_3.enable_grid(False)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(True)
        self.qtgui_time_sink_x_3.enable_stem_plot(False)


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


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_3_win)
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
        self.low_pass_filter_1 = filter.interp_fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                filter_samp_rate,
                1200,
                500,
                firdes.WIN_HAMMING,
                6.76))
        self._freq_offset_tool_bar = Qt.QToolBar(self)
        self._freq_offset_tool_bar.addWidget(Qt.QLabel('Freq Offset (Hz)' + ": "))
        self._freq_offset_line_edit = Qt.QLineEdit(str(self.freq_offset))
        self._freq_offset_tool_bar.addWidget(self._freq_offset_line_edit)
        self._freq_offset_line_edit.returnPressed.connect(
            lambda: self.set_freq_offset(eng_notation.str_to_num(str(self._freq_offset_line_edit.text()))))
        self.top_layout.addWidget(self._freq_offset_tool_bar)
        _enable_rx_check_box = Qt.QCheckBox('enable_rx')
        self._enable_rx_choices = {True: 1, False: 0}
        self._enable_rx_choices_inv = dict((v,k) for k,v in self._enable_rx_choices.items())
        self._enable_rx_callback = lambda i: Qt.QMetaObject.invokeMethod(_enable_rx_check_box, "setChecked", Qt.Q_ARG("bool", self._enable_rx_choices_inv[i]))
        self._enable_rx_callback(self.enable_rx)
        _enable_rx_check_box.stateChanged.connect(lambda i: self.set_enable_rx(self._enable_rx_choices[bool(i)]))
        self.top_grid_layout.addWidget(_enable_rx_check_box, 1, 4, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            loop_bw,
            damp,
            ted_gain,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_binary_slicer_fb_2 = digital.binary_slicer_fb()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, filter_samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repeat_1 = blocks.repeat(gr.sizeof_float*1, sps)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, 1/1000, 4000, 1)
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_gr_complex*1, '/Users/ebaum/Documents/capstone/iq/ask-tuned-30k.iq', True, 0, 0)
        self.blocks_file_source_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_3 = blocks.add_const_ff(-1)
        self.blocks_add_const_vxx_2 = blocks.add_const_ff(-0.5)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_2, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_add_const_vxx_3, 0), (self.qtgui_time_sink_x_3, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_2, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_add_const_vxx_3, 0))
        self.connect((self.blocks_file_source_1, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_repeat_1, 0), (self.qtgui_time_sink_x_3, 2))
        self.connect((self.blocks_sub_xx_0, 0), (self.digital_binary_slicer_fb_2, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.digital_binary_slicer_fb_2, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_repeat_1, 0))
        self.connect((self.low_pass_filter_1, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.qtgui_time_sink_x_3, 1))


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
        self.set_sps(int(self.filter_samp_rate/self.symbol_rate))

    def get_filter_samp_rate(self):
        return self.filter_samp_rate

    def set_filter_samp_rate(self, filter_samp_rate):
        self.filter_samp_rate = filter_samp_rate
        self.set_moving_avg_len(self.filter_samp_rate/10)
        self.set_sps(int(self.filter_samp_rate/self.symbol_rate))
        self.blocks_throttle_0.set_sample_rate(self.filter_samp_rate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.filter_samp_rate, 1200, 500, firdes.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_3.set_samp_rate(self.filter_samp_rate)

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_tone_freq(self):
        return self.tone_freq

    def set_tone_freq(self, tone_freq):
        self.tone_freq = tone_freq

    def get_ted_gain(self):
        return self.ted_gain

    def set_ted_gain(self, ted_gain):
        self.ted_gain = ted_gain
        self.digital_symbol_sync_xx_0.set_ted_gain(self.ted_gain)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_repeat_1.set_interpolation(self.sps)

    def get_scatter_center_freq(self):
        return self.scatter_center_freq

    def set_scatter_center_freq(self, scatter_center_freq):
        self.scatter_center_freq = scatter_center_freq
        Qt.QMetaObject.invokeMethod(self._scatter_center_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.scatter_center_freq)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_pulse_width_hz(self):
        return self.pulse_width_hz

    def set_pulse_width_hz(self, pulse_width_hz):
        self.pulse_width_hz = pulse_width_hz
        Qt.QMetaObject.invokeMethod(self._pulse_width_hz_line_edit, "setText", Qt.Q_ARG("QString", str(self.pulse_width_hz)))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_moving_avg_len(self):
        return self.moving_avg_len

    def set_moving_avg_len(self, moving_avg_len):
        self.moving_avg_len = moving_avg_len

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.loop_bw)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        Qt.QMetaObject.invokeMethod(self._freq_offset_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq_offset)))

    def get_enable_rx(self):
        return self.enable_rx

    def set_enable_rx(self, enable_rx):
        self.enable_rx = enable_rx
        self._enable_rx_callback(self.enable_rx)

    def get_damp(self):
        return self.damp

    def set_damp(self, damp):
        self.damp = damp
        self.digital_symbol_sync_xx_0.set_damping_factor(self.damp)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq





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
