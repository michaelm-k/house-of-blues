# Dependencies: mutagen (pip install mutagen # http://mutagen.readthedocs.io/en/latest/api/mp3.html#mutagen.mp3.MPEGInfo)
# Example usage: python update.py -c update.json -d

import os
import json
import sys
import argparse
from mutagen.mp3 import EasyMP3 as MP3

DATA = {}
DRYRUN = True

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--config', type=str, required=True)
	parser.add_argument('-d', '--dryrun', action='store_true')
	return parser.parse_args()

def populate_vars(args):
	global DATA
	global DRYRUN
	
	DRYRUN = args.dryrun
	config = args.config
	with open(config) as f:    
		DATA = json.load(f)

def rename_file(filename, new_filename):
	os.rename(filename, new_filename)
		
def update_file_metadata(path, data, title, artist):
	audio = MP3(path)
	audio.tags['date'] = data['year']
	audio.tags['title'] = title
	audio.tags['albumartist'] = data['album_artist']
	audio.tags['artist'] = artist
	audio.tags['album'] = data['album']
	audio.save()
		
def update_files(data):
	dir = data["directory"]
	os.chdir(dir)
	for i, filename in enumerate(os.listdir()):
		ext = os.path.splitext(filename)[1]
		artist = data["songs"][i]["artist"]
		title = data["songs"][i]["title"]
		new_filename = artist + " - " + title + ext
		if DRYRUN:
			print(filename + " -> " + new_filename)
		else:
			update_file_metadata(os.path.join(dir, filename), data, title, artist)
			rename_file(filename, new_filename)

if __name__ == "__main__":
	populate_vars(parse_args())
	update_files(DATA)
