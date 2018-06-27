"""lvp - A loose implementation of Lempel-Ziv compression, for use in determining song complexity/repetition.
VERSION 0.1.0

This program is based off of a blog post by Colin Morris titled "Are Pop Lyrics Getting More Repetitive?" <https://pudding.cool/2017/05/song-repetition/>. In the blog post Mr. Morris used his own version of the LZ algorithm to determine how repetitive a song is. I have taken my own interpretation of this idea and implemented it in this program.

This program was requested by, and created for, Cliff Stumme aka "The Pop Song Professor". 

Copyright (C) 2018, Ian S. Pringle
License GNULv3+: GNU GPL Version 3 or later <https://github.com/pard68/lzp/blob/master/LICENSE>
This is free software: you are free to change and redistribute it.
There is NO warranty."""

'''
--------------------------
New Code
--------------------------
'''
import re
import string

original_file_name = ""

def read_from_file(file_name):
	global original_file_name
	original_file_name = file_name
	with open(file_name, 'r') as string:
		string = string.read()
		return string

def write_to_file(string):
	global original_file_name
	with open("comp_%s" % original_file_name, 'w') as output_file:
		output_file.write("%s" % string)

def compare(a, b):
	return a == b

def parse_(string):			#Creates an array of locations in string. Line starts and ends, and verses
	lyrics = []
	line = []
	lineStart = 0
	loc = 0
	
	for char in string:
		prevChar = string[loc-1]
		if char is "\n" and prevChar is "\n":
			pass
		else:
			nextChar = string[loc+1]
			if char is "\n" and nextChar is not "\n":
				lineEnd = loc
				line.append([lineStart, lineEnd])
				lineStart = lineEnd + 1
			elif char is "\n" and nextChar is "\n":
				lineEnd = loc
				line.append([lineStart, lineEnd])
				lineStart = lineEnd + 2
				lyrics.append(line)
				line =[]
		loc += 1
	return lyrics

def compare_verses(string, array, numberOfVerses):
	start = 0
	end = array[numberOfVerses][-1][-1]
	target = string[start:end]

	print(string.find(target, end))

def compare_half(string, array):
	middleVerse = int(len(array) / 2 - len(array) / 2 % 2) - 1
	compare_verses(string, array, middleVerse)

string = read_from_file('lyrics_full.txt')
#compare_verses(string)
arrayLyrics = parse_(string)
compare_half(string, arrayLyrics)

'''
--------------------------
Old Code
--------------------------

import re

og_file_name = ""

def get_text(file_name):
	global og_file_name
	og_file_name = file_name
	with open(file_name, 'r') as lyrics:
		lyrics = lyrics.read()
		return lyrics

def write_text(string):
	global og_file_name
	with open("comp_%s" % og_file_name, 'w') as output_file:
		output_file.write("%s" % string)
	
	
def get_line(string, line_start, line_end): #passing 1 for count_yes will return the x instead of location + 1. Passing 0 for line_end will return the location which is 50% of the lines		
	location = 0

	while line_start < line_end:
		location = string.find('\n', location + 1)
		line_start += 1
	return location

def line_total(string, verse_num):
	if verse_num == 0:
		return verse_num
	elif verse_num == 1:
		verse_start = 0
	else:
		verse_start = get_verse(string, verse_num, 0) - len(string[get_verse(string, verse_num - 1, 0):get_verse(string, verse_num, 0)])
	verse_end = get_verse(string, verse_num, 0)
	x = 0	

	while verse_start < verse_end:
		verse_start = string.find('\n', verse_start + 1)
		x += 1
	return x

def get_verse(string, verse_num, count_yes):
	if verse_num == 0:
		verse_num = string.count('\n\n') + 1
		if count_yes == 1:
			return int(verse_num)
	loc = 0
	while verse_num > 0:
		loc = string.find('\n\n', loc + 1)
		verse_num -= 1
	return int(loc)

def get_next(string, param, loc): #returns start index of match
	next_loc = string.find(param, loc)
	return next_loc

def replace(string, new, loc_start, loc_end):
	string = string[:loc_start] + new + string[loc_end:]
	return string

def compress(start, end):
	compression = '%s:%s' % (start, end)
	return compression

def get_mid(total):
	if total % 2 == 0:
		total /= 2
	elif total % 2 != 0:
		total = (total - 1) / 2
	return int(total)

def verse(lyrics):
	verse_start = 0
	verse_end = get_mid(get_verse(lyrics, 0, 1))
	
	loc_start = 0
	loc_end = get_verse(lyrics, verse_end, 0)
	
	p = re.compile('[0-9]+\++[0-9]*')

	"""Searches lyrics for duplicates of 50% of the verses."""
	#total = get_verse(lyrics, 0, 1)
	j = verse_end
	while j > 0:
		loc_start = 0
		loc_end = get_verse(lyrics, verse_end, 0)
		#print(verse_start, verse_end, j, loc_start, loc_end)
		total = get_verse(lyrics, 0, 1)
		while verse_end != total:
			#print(verse_start, verse_end, loc_start, loc_end)
			verses = lyrics[loc_start:loc_end]
			match = get_next(lyrics, verses, loc_end)
			if verses == '\n':
				match = -1
			if verses == '\n\n':
				match = -1
			if verses == '':
				match = -1
			if match != -1:# and re.search('[0-9+\++[0-9]', verses) is None and '\n\n' not in verses:
				lyrics  = replace(lyrics, compress(loc_start, loc_end), match, match + len(verses))
				#print(match)
				#print(repr(verses))
			#i += 1
			verse_start += 1
			verse_end += 1

			loc_start = get_verse(lyrics, verse_start, 0) + 2
			loc_end = get_verse(lyrics, verse_end, 0)
                        
		j -= 1
		verse_end = j
		verse_start = 0
		#print("\n") 
	return lyrics

def line(lyrics):
	verse_start = 0
	verse_end = 1
	
	verse_total = get_verse(lyrics, 0, 1)

	"""Move verse to verse"""
	while verse_total > 0:
		line_start = line_total(lyrics, verse_start)
		line_end = line_total(lyrics, verse_end)
		if line_start == 0:
			loc_start = 0
		else:
			loc_start = 1 
		loc_end = get_line(lyrics, line_start, line_end)
		total = line_total(lyrics, verse_end)
	
		while verse_end > 0: 
			while line_end <= total: 
				print(ltotal, line_end)
				lines = lyrics[loc_start:loc_end]
				match = get_next(lyrics, lines, loc_end)
				if lines == '\n':
					match = -1
				if lines == '\n\n':
					match = -1
				if lines == '':
					match = -1
				if match != -1:
					lyrics = replace(lyrics, compress(loc_start, loc_end), match, match + len(lines))
				
				line_start += 1
				line_end += 1
				
			ltotal -= 1
			line_start = 0
			line_end -= 1		
						

		verse_total -= 1
		verse_start += 1
		verse_end += 1

	return lyrics
	
def lzp(file_name):
	lyrics = get_text(file_name)

	#lyrics = verse(lyrics)
	lyrics = line(lyrics)
	write_text(lyrics)

def dev():
	lzp('lyrics_full.txt')

dev()

'''
