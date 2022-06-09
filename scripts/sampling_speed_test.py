#!/usr/bin/env python

import math
from time import time
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string


CHANNEL_MAXIMAL_NUMBER = 4
SAMPLING_START_NUMBER = 100
SAMPLING_STEP_MULTIPLIER = 10
SAMPLING_STEPS_NUMBER = 3

# Get an instance of the selected hat device object.
address = select_hat_device(HatIDs.MCC_128)
hat = mcc128(address)
options = OptionFlags.DEFAULT
input_mode = AnalogInputMode.SE
input_range = AnalogInputRange.BIP_10V
hat.a_in_mode_write(input_mode)
hat.a_in_range_write(input_range)


def test_sampling_speed(config):
    start_time = time()
    channels = [i for i in range(config['channel_number'])]
    for i in range(config['sampling_number']):
        for channel in channels:
            sampling_result = hat.a_in_read(channel, options)
    end_time = time()
    difference = end_time - start_time
    return difference

def test_sampling():
    sampling_numbers = [SAMPLING_START_NUMBER * int(math.pow(SAMPLING_STEP_MULTIPLIER, i)) for i in range(SAMPLING_STEPS_NUMBER)]
    print('Sampling speed test')
    for channel_number in range(1, CHANNEL_MAXIMAL_NUMBER + 1):
        print('Channel number:', channel_number)
        print('Sampling number  |  Time  |  per channel |  per sampling  |  per ch and sampling')
        for sampling_number in sampling_numbers:
            config = {'channel_number': channel_number, 'sampling_number': sampling_number}
            sampling_time = test_sampling_speed(config)
            time_per_channel = sampling_time / channel_number
            time_per_sampling = sampling_time / sampling_number
            time_per_channel_and_sampling = time_per_channel / sampling_number
            print(sampling_number, sampling_time, time_per_channel, time_per_sampling, time_per_channel_and_sampling)

def main():
    test_sampling()

if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
