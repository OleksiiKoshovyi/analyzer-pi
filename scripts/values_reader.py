#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 128 Functions Demonstrated:
        mcc128.a_in_read
        mcc128.a_in_mode_write
        mcc128.a_in_range_write

    Purpose:
        Read a single data value for each channel in a loop.

    Description:
        This example demonstrates acquiring data using a software timed loop
        to read a single value from each selected channel on each iteration
        of the loop.
"""
from __future__ import print_function
from time import sleep
from sys import stdout

from pandas import Interval
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string
from datetime import datetime
import csv
import json
from types import SimpleNamespace


# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def get_config():
    with open('./config.sampling.json', encoding='utf-8', mode='r') as config_file:
        config = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))
        return config

def sample_voltage(hat, options, config):
    duration = config.duration
    sample_interval = config.interval
    channels = config.channels
    if len(channels) == 0:
        print('You didn\'t select any channel in config')
        return []
    start_time = datetime.now().timestamp()
    end_time = start_time + duration
    samples = []
    while datetime.now().timestamp() < end_time:
        # Read a single value from each selected channel.
        for chan in channels:
            value = hat.a_in_read(chan, options)
            time = str(datetime.now().timestamp())
            samples.append({'date': time, 'channel': chan, 'sample': value})
        # Wait the specified interval between reads.
        sleep(sample_interval)
    samples_count = len(samples)
    channels_count = len(channels)
    samples_per_channel = int(samples_count / channels_count)
    print('samples per channel: ', samples_per_channel)
    return samples

def save_result_to_csv(samples, start_time):
    file_name = 'samples/voltage-{}.csv'.format(str(start_time))
    fieldnames = ['date', 'channel', 'sample']
    with open(file_name, 'w', newline='') as csv_file:
        print('new file created: {}'.format(file_name))
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(samples)

def print_result_to_console(samples):
    for sample in samples:
        print('{:>}. Ch: {}. {:12.7} V'.format(sample['date'], sample['channel'], sample['sample']))

def print_result(config, samples, start_time):
    output_sources = config.output_sources
    if output_sources.console:
        print_result_to_console(samples)
    if output_sources.csv:
        save_result_to_csv(samples, start_time)

def main():
    """
    This function is executed automatically when the module is run directly.
    """
    config = get_config()
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 3
    input_mode = AnalogInputMode.SE
    input_range = AnalogInputRange.BIP_10V

    mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]

    try:
        # Ensure low_chan and high_chan are valid.
        if low_chan < 0 or low_chan >= mcc_128_num_channels:
            error_message = ('Error: Invalid low_chan selection - must be '
                             '0 - {0:d}'.format(mcc_128_num_channels - 1))
            raise Exception(error_message)
        if high_chan < 0 or high_chan >= mcc_128_num_channels:
            error_message = ('Error: Invalid high_chan selection - must be '
                             '0 - {0:d}'.format(mcc_128_num_channels - 1))
            raise Exception(error_message)
        if low_chan > high_chan:
            error_message = ('Error: Invalid channels - high_chan must be '
                             'greater than or equal to low_chan')
            raise Exception(error_message)

        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        hat = mcc128(address)

        hat.a_in_mode_write(input_mode)
        hat.a_in_range_write(input_range)

        print('\nMCC 128 single data value read example')
        print('    Functions demonstrated:')
        print('         mcc128.a_in_read')
        print('         mcc128.a_in_mode_write')
        print('         mcc128.a_in_range_write')
        print('    Input mode: ', input_mode_to_string(input_mode))
        print('    Input range: ', input_range_to_string(input_range))
        print('    Channels: {0:d} - {1:d}'.format(low_chan, high_chan))
        print('    Selected channels: {}'.format(config.channels))
        print('    Sampling interval: {}'.format(config.interval))
        print('    Sampling duration: {}'.format(config.duration))
        print('    Options:', enum_mask_to_string(OptionFlags, options))
        try:
            input("\nPress 'Enter' to continue")
        except (NameError, SyntaxError):
            pass

        print('\nAcquiring data ... Press Ctrl-C to abort')

        try:
            start_time = datetime.now().timestamp()
            samples = sample_voltage(hat, options, config)
            print_result(config, samples, start_time)
            print('Done')

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
