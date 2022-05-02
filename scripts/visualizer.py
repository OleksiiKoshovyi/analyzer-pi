#!/usr/bin/env python
#  -*- coding: utf-8 -*-


from datetime import datetime
import glob
import pandas as pd
import matplotlib.pyplot as plt


def process_csv(name):
    samples_df = pd.read_csv(name)
    start_timestamp = samples_df['date'][0]
    samples_df['date'] = samples_df['date'] - start_timestamp
    samples_df.set_index('date', inplace=True)
    samples_df.groupby('channel')['sample'].plot(legend=True, ylabel='sample')

    start_date = datetime.fromtimestamp(start_timestamp)
    plt.title(f'Start time: {start_date}')
    plt.show()

def main():
    # list of csv in the folder ./samples
    SAMPLES_FOLDER_PATH = './samples/'
    SEARCH_PATTERN = "*.csv"
    samples = glob.glob(SAMPLES_FOLDER_PATH + SEARCH_PATTERN)
    
    # user choose one file
    print(f'{len(samples)} csv files:')
    for i, sample in enumerate(samples):
        print(f'{i:3}. {sample}')
    FILE_INDEX = int(input('Choose csv file for visualization: '))
    if 0 <= FILE_INDEX < len(samples):
        sample = samples[FILE_INDEX]
        process_csv(sample)
    else:
        raise ValueError('index out of bounds')

if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()