# Dependencies: VLC
# Example usage: python transcode.py -c transcode.json -sf mp4 -df wav

# https://wiki.videolan.org/Documentation:Streaming_HowTo_New/
# https://wiki.videolan.org/VLC_HowTo/Extract_audio/#Extracting_audio_in_original_format
# https://wiki.videolan.org/Transcode/

import os
import json
import sys
import argparse
import subprocess
import re
import time

DATA = {}
TRANSCODER = None
SRC_FORMAT = None
DEST_FORMAT = None

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--config', type=str, required=True)
	parser.add_argument('-t', '--transcoder', type=str, required=True)
	parser.add_argument('-sf', '--srcformat', type=str, required=True)
	parser.add_argument('-df', '--destformat', type=str, required=True)
	return parser.parse_args()

def populate_vars(args):
	global DATA
	global TRANSCODER
	global SRC_FORMAT
	global DEST_FORMAT

	config = args.config
	with open(config) as f:    
		DATA = json.load(f)
	
	TRANSCODER = args.transcoder
	SRC_FORMAT = args.srcformat
	DEST_FORMAT = args.destformat

def build_command(data):
	cmd = data["cmd"]
	args = re.findall(r'\$\w+', cmd)
	for arg in args:
		cmd = cmd.replace(arg, data[arg])
	return cmd

def execute_command(cmd):
	subprocess.call(cmd, shell=True)

def transcode_files(data, transcoder, src_format, dest_format):
	dir = data["directory"]
	os.chdir(dir)
	for file in os.listdir():
		if os.path.isdir(file):
			continue
		
		name = os.path.splitext(file)[0]
		ext = os.path.splitext(file)[1]

		if ext != '.' + src_format:
			continue
		
		data[transcoder][dest_format]["$src"] = os.path.join(dir, file)
		new_file = ''
		if src_format == dest_format:
			new_file = name + " (new)" + '.' + dest_format
		else:
			new_file = name + '.' + dest_format
		data[transcoder][dest_format]["$dest"] = os.path.join(dir, new_file)
		
		cmd = build_command(data[transcoder][dest_format])
		cmd = "\"" + data[transcoder]["exec"] + "\"" + " " + cmd

		print("Transcoding: " + file)
		start = time.time()
		execute_command(cmd)
		end = time.time()
		print("Finished in " + "{:.2f}".format(end-start) + "s")

if __name__ == "__main__":
	populate_vars(parse_args())
	transcode_files(DATA, TRANSCODER, SRC_FORMAT, DEST_FORMAT)
