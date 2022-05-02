import json
import subprocess
import click


print('You are going to download scripts from raspberry-pi.')
if not click.confirm('It may replace old files. Continue?', default=True):
    exit

with open('../config.json', encoding='utf-8', mode='r') as config_file:
    config = json.load(config_file)
    user = config['user']
    host = config['host']
    connection = '{}@{}:'.format(user, host)
    subprocess.run( ["scp", "-r", "-P", "22",
        "../scripts/*",
        connection + "daqhats/examples/python/mcc128/"] )
