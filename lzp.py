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

def get_line(string, line_num, count_yes): #passing 1 for Loc_yes will return the x instead of location + 1. Passing 0 for line_num will return the location which is 50% of the lines
	if line_num == 0:
		x = string.count('\n')
		if x % 2 == 0:
			x = int(x / 2)
		elif x % 2 != 0:
			x = int((x - 1) / 2)
		if count_yes == 1:
			return x
	else: 
		x = line_num

	location = 0
	while x > 0:
		location = string.find('\n', location + 1)
		x -= 1
	return location + 1

def get_verse(string, verse_num, count_yes):
	loc = string.find('\n\n', verse_num)
	return loc

def get_next(string, param, loc): #returns start index of match
	next_loc = string.find(param, loc)
	return next_loc

def replace(string, new, loc_start, loc_end):
	string = string[:loc_start] + new + "\n" + string[loc_end:]
	return string

def compress(start, end):
	compression = '%s+%s' % (start, end)
	return compression

def verse(lyrics):
	loc_start = 0
	loc_end = get_verse(lyrics, 0, 0)
	
	#verse = lyrics[loc_start:loc_end]
	#get_next(lyrics, verse, loc_end)

	i = 1
	k = get_verse(lyrics, 0, 1)
	while i < k:
		verse = lyrics[loc_start:loc_end]
		

def lzp(file_name):
	lyrics = get_text(file_name)

	loc_start = 0
	loc_end = get_line(lyrics, 0, 0)
	line = lyrics[loc_start:loc_end]

	match = get_next(lyrics, line, loc_end)
	
	#Compare Lines
	i = get_line(lyrics, 0, 1)
	while i > 0:
		line = lyrics[loc_start:loc_end]
		j = True
		while j == True:
			match = get_next(lyrics, line, loc_end)
			if match != -1:
				lyrics = replace(lyrics, compress(loc_start, loc_end), match, match + len(line))
				print(lyrics)
				print("\n")
				loc_end = match + len(line)
			elif match == -1:
				print("No match!")
				print(line)
				print("\n")
				j = False
		i -= 1
		loc_end = get_line(lyrics, i, 0)

















def dev():
	lzp('lyrics_full.txt')

dev()
