# Analyzer-pi

Final project for international semester in University Valladolid.
The main goal of this project is aqusition and analysis of the voltage of an aqusition board.

## Scripts

### Config
In the file `scripts/config.sampling.json` we may manage sampling rules:
- channels
- duration
- interval
- output sources: console, csv

### Sampling
You should upload current version of the `scripts/values_reader.py` to your raspberry-pi via `tools/upload.py` there you may run sampling script.
In order to print a result of sampling in console or save in a csv file you should set console or csv parametrs in `scripts/config.sampling.json` to `true` respectively.

### Visualization
You may visualize collected data via `scrupts/visualizer.py`. Previously you should download collected data from raspberry-pi. In order to do it you should run `tools/download.py` script. It will download not only csv files, but also last uploaded scripts.

## Config
You should rename `config.example.json` to `config.json`
and set specific user and host for your future connections.

## Tools
Tools folder is dedicated to manage little tasks in few clicks:
For now you may
- `upload.py`: upload new versions of your scripts to raspberry-pi
- `download.py`: download last updated script to your own pc.