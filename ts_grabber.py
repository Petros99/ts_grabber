#!/usr/bin/env python3
import requests
import argparse
import wget
from subprocess import run

parser = argparse.ArgumentParser()
#parser.add_argument('vid_name', type=str)
parser.add_argument('m3u8_url', type=str)
parser.add_argument('name', type=str)
args = parser.parse_args()

run('rm -rfv *.ts', shell=True, check=True)
i = 0
m3u8_folder = args.m3u8_url
while True:
    i -= 1
    if m3u8_folder[i] == '/':
        break

m3u8_folder = m3u8_folder[:i] + '/'


m3u8_file = requests.get(args.m3u8_url)

ts_name = ''
for letter in m3u8_file.text:
    if letter == '\n':
        if ts_name[0] != '#':
            fname = wget.download(m3u8_folder + ts_name)
            run('cat ' + fname + ' >> ' + 'all.ts', shell=True, check=True)
        ts_name = ''

    else:
        ts_name += letter
run(['ffmpeg', '-i', 'all.ts', str(args.name) + '.mp4'])
run('rm -rfv *.ts', shell=True, check=True)
