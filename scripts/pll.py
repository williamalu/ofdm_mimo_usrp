#!/usr/bin/env python


""" Class that reads in data from decoder.py and uses a PLL to correct for
phase offset. """


import numpy as np
import matplotlib.pyplot as plt

import helper
#from decoder import Decoder


j = (0 + 1j)


class PLL(object):

    def __init__(self, data, k_p, k_i, k_d):
        """ Initialize data and PID coefficients. """

        self.data = data
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.data_fixed = None


    def correct_phase_offset(self):
        """ Use PID control to estimate phase offset in self.data, correct for
        it, and save the corrected data as self.data_fixed. """

        phase = 0
        prev_err = 0
        err = 0
        err_sum = 0

        self.data_fixed = np.array([])

        self.abs_val_list = np.array([])
        self.err_list = np.array([])
        self.phase_list = np.array([])

        for x in self.data:

            # Multiply input value by complex exponential of specified phase
            y = x * np.exp(-phase * j)
            self.data_fixed = np.append(self.data_fixed, y)

            # Estimate error in phase for BPSK
            err = -y.real * y.imag #if (np.absolute(x) > .004) else 0.0

            # Estimate error in phase for QPSK
            # A = y.real * np.sign(y.imag)
            # B = y.imag * np.sign(y.real)
            # err = (-1/2) * (A - B)

            # Calculate integral of error
            err_sum += err

            # Calculate derivative of error
            err_diff = err - prev_err

            # Use PID control to find the phase offset for the next step
            phase += self.k_p * err + self.k_i * err_sum + self.k_d * err_diff
            phase = helper.wrap_radian(phase)

            # Define error in previous step
            prev_err = err

            # Track data for plottting
            self.err_list = np.append(self.err_list, err)
            self.abs_val_list = np.append(self.abs_val_list, np.absolute(x))
            self.phase_list = np.append(self.phase_list, phase)


    def correct_frequency_offset(self):
        """ Use P control to estimate frequency offset in self.data, correct for
        it, and save the corrected data as self.data_fixed. """

        freq = 0
        err = 0

        self.data_fixed = np.array([])

        self.abs_val_list = np.array([])
        self.err_list = np.array([])
        self.freq_list = np.array([])

        for i, x in enumerate(self.data):

            # Multiply input value by complex exponential of specified phase
            y = x * np.exp(-freq * i * j)
            self.data_fixed = np.append(self.data_fixed, y)

            # Estimate error in phase for BPSK
            err = y.real * y.imag

            # Use PID control to find the phase offset for the next step
            freq += self.k_p * err

            # Track data for plottting
            self.err_list = np.append(self.err_list, err)
            self.abs_val_list = np.append(self.abs_val_list, np.absolute(x))
            self.freq_list = np.append(self.freq_list, freq)


    def plot_data(self):
        """ Visualize! """

        # Original data and corrected data
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.data.real, linewidth=2.0, label='real')
        plt.plot(self.data.imag, 'r-', linewidth=2.0, label='imag')
        # plt.plot(self.err_list, label='err')
        plt.title('Data')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.data_fixed.real, linewidth=2.0, label='real')
        plt.plot(self.data_fixed.imag, 'r-', linewidth=2.0, label='imag')
        plt.title('Data with phase correction')
        plt.legend()

        # Phase and error
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.phase_list)
        plt.title('Phase Offset Over Time')
        plt.subplot(2, 1, 2)
        plt.plot(self.err_list)
        plt.title('Error Over Time')

        # Absolute value
        plt.figure()
        plt.plot(self.abs_val_list)
        plt.title('Absolute Value Over Time')
        plt.show()


if __name__ == "__main__":

    '''
    data_path = '../data/'
    input_filename = 'received_data_1.bin'
    decoder = Decoder(data_path, input_filename)
    decoder.read_file()
    decoder.find_offsets_bpsk()
    decoder.fix_offsets()
    '''

    k_p = 0.7
    k_i = 0.1
    k_d = 0.0
    pll = PLL(decoder.data_fixed, k_p, k_i, k_d)
    pll.correct_phase_offset()
    pll.plot_data()
