# Dependencies: pydub (pip install pydub # https://github.com/jiaaro/pydub)
# Example usage: python manipulate.py

import os
from sys import stdin
from pydub import AudioSegment

def get_input():
	return stdin.readline().rstrip("\n")

def boost(audio_segment, amount):
	audio_segment = audio_segment + amount
	return audio_segment

def slice(audio_segment, start, stop):
	audio_segment = audio_segment[start:(stop + 1000)]
	return audio_segment

def reverse(audio_segment):
	audio_segment = audio_segment.reverse()
	return audio_segment

def fade(audio_segment, fade_in, fade_out):
	if fade_in != 0:
		audio_segment = audio_segment.fade_in(fade_in)
	if fade_out != 0:
		audio_segment = audio_segment.fade_out(fade_out)
	return audio_segment

def print_properties(audio_segment):
	print("Duration (s): " + "{:.2f}".format(audio_segment.duration_seconds))
	print("dBFS: " + "{:.2f}".format(audio_segment.dBFS))
	print("Max dBFS: " + "{:.2f}".format(audio_segment.max_dBFS))
	print("# channels: " + str(audio_segment.channels))
	print("Sample width (bytes): " + str(audio_segment.sample_width))
	print("Frame rate (Hz): " + str(audio_segment.frame_rate))

def normalize(audio_segment):
	audio_segment = audio_segment.apply_gain(-audio_segment.max_dBFS)
	return audio_segment
	
def timestamp_to_seconds(timestamp):
	nums = timestamp.split(':')
	return int(nums[0]) * 60 + int(nums[1])

if __name__ == "__main__":
	print("Enter path to directory:")
	path_to_dir = get_input()
	os.chdir(path_to_dir)
	
	while True:
		files = []
		i = 0
		for file in os.listdir():
			if os.path.isdir(file) or not file.endswith(".wav"):
				continue
			files.append(file)
			print(file + " (" + str(i) + ")")
			i += 1
		
		print("Select file:")
		i = int(get_input())	
		
		path_to_file = os.path.join(path_to_dir, files[i])
		format = "wav"
		audio_segment = AudioSegment.from_file(path_to_file, format)
		while True:			
			print("Select operation: boost (1), slice (2), reverse (3), fade (4), view properties (5), normalize (6)")
			op = get_input()
			if op == '1':
				print("Boost amount (dB):")
				amount = int(get_input())
				audio_segment = boost(audio_segment, amount)
			elif op == '2':
				print("Start (x:xx):")
				timestamp = get_input()			
				start = timestamp_to_seconds(timestamp)
				print("Stop (y:yy):")
				timestamp = get_input()
				stop = timestamp_to_seconds(timestamp)
				audio_segment = slice(audio_segment, start * 1000, stop * 1000)
			elif op == '3':
				audio_segment = reverse(audio_segment)
			elif op == '4':
				print("Fade in (s):")
				fade_in = int(get_input())
				print("Fade out (s):")
				fade_out = int(get_input())
				audio_segment = fade(audio_segment, fade_in * 1000, fade_out * 1000)
			elif op == '5':
				print_properties(audio_segment)
				break
			elif op == '6':
				audio_segment = normalize(audio_segment)
			else:
				continue
			audio_segment.export(path_to_file, format=format)
			break
