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
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string
from datetime import datetime
import csv
import json

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def configure_script():
    with open('./config.sampling.json', encoding='utf-8', mode='r') as config_file:
        config = json.load(config_file)
        channels = config['channels']
        duration = config['duration']
        interval = config['interval']
        output_config = config['output_config']
        return channels, duration, interval, output_config

def main():
    """
    This function is executed automatically when the module is run directly.
    """
    channels, duration, interval, output_config = configure_script()
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 3
    channel_count = len(channels)
    input_mode = AnalogInputMode.SE
    input_range = AnalogInputRange.BIP_10V

    mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]
    sample_interval = interval  # Seconds

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
        print('    Selected channels: {}'.format(channels))
        print('    Options:', enum_mask_to_string(OptionFlags, options))
        try:
            input("\nPress 'Enter' to continue")
        except (NameError, SyntaxError):
            pass

        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\nSample')

        try:
            samples_per_channel = 0
            time = str(datetime.now().timestamp())
            file_name = 'samples/voltage-{}.csv'.format(time)
            fieldnames = ['date', 'channel', 'sample']
            with open(file_name, 'w', newline='') as csv_file:
                print('new file created: {}'.format(file_name))
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                samples = [{}] * channel_count
                start_time = datetime.now().timestamp()
                end_time = start_time + duration
                while datetime.now().timestamp() < end_time:
                    # Display the updated samples per channel count
                    samples_per_channel += 1
                    print('{:17}'.format(samples_per_channel))

                    # Read a single value from each selected channel.
                    for id, chan in enumerate(channels):
                        value = hat.a_in_read(chan, options)
                        time = str(datetime.now().timestamp())
                        samples[id] = {'date': time, 'channel': chan, 'sample': value}

                    stdout.flush()
                    # Save in csv
                    if output_config['save_result_in_csv']:
                        writer.writerows(samples)
                    # Print in console
                    if output_config['print_result']:
                        for sample in samples:
                            print('{:>}. Ch: {}. {:12.7} V'.format(sample['date'], sample['channel'], sample['sample']))

                    # Wait the specified interval between reads.
                    sleep(sample_interval)

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
