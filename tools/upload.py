import json
import subprocess
import click


print('You are going to upload scripts to raspberry-pi.')
if not click.confirm('It may replace old files. Continue?', default=True):
    exit

with open('../config.json', encoding='utf-8', mode='r') as config_file:
    config = json.load(config_file)
    user = config['user']
    host = config['host']
    connection = f'{user}@{host}:'
    subprocess.run( ["scp", "-P", "22",
        "../scripts/*.py",
        connection + "daqhats/examples/python/mcc128/"],
        check=True)
