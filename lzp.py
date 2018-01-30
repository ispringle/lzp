"""lvp - A loose implementation of Lempel-Ziv compression, for use in determining song complexity/repetition.

This program is based off of a blog post by Colin Morris titled "Are Pop Lyrics Getting More Repetitive?" <https://pudding.cool/2017/05/song-repetition/>. In the blog post Mr. Morris used his own version of the LZ algorithm to determine how repetitive a song is. I have taken my own interpretation of this idea and implemented it in this program.

This program was requested by, and created for, Cliff Stumme aka "The Pop Song Professor". 

Copyright (C) 2018, Ian S. Pringle
License GNULv3+: GNU GPL Version 3 or later <https://github.com/pard68/lzp/blob/master/LICENSE>
This is free software: you are free to change and redistribute it.
There is NO warranty."""

def get_text(file_name):
	with open(file_name, 'r') as lyrics:
		lyrics = lyrics.read()
		return lyrics

def start_loc(string):
	x = string.count('\n')
	if x % 2 == 0:
		x = int(x / 2)
	elif x % 2 != 0:
		x = int((x - 1) / 2)
	location = 0
	while x > 0:
		location = string.find('\n', location + 1)
		x -= 1
	return location + 1

def get_next(string, param, loc):
	next_loc = string.find(param, loc+1)
	return next_loc

def replace(string, new, loc_start, loc_end):
	string = string[:loc_start] + new + string[loc_end:]
	return string

def compress(start, end):
	compression = '%s+%s' % (start, end)
	return compression

def lzp(file_name):
	lyrics = get_text(file_name)

	loc_start = 0
	loc_end = start_loc(lyrics)
	line = lyrics[loc_start:loc_end]

	match = get_next(lyrics, line, loc_end)
	
	if match != -1:
		lyrics = replace(lyrics, compress(loc_start, loc_end), match, match + len(line))
		print(lyrics)
	elif match == -1:
		print("No match!")


















def dev():
	lzp('lyrics.txt')

dev()
