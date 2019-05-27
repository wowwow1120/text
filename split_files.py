#!/usr/bin/python

import os
import sys


if __name__ == '__main__':
	target_file = sys.argv[1]

	open_file = open(target_file, 'r')
	lines = open_file.readlines()
	for line in lines:
		title = line.split('\t')[0]
		open_output_file = open(title+'.txt' , 'w')
		contents = line.split('\t')[1]
		open_output_file.write(contents)
	open_output_file.close()
