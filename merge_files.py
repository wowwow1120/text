#!/usr/bin/python

import os
import sys

if __name__ == '__main__':
	target_dir = sys.argv[1]

	list_dir = os.listdir(target_dir)
	open_output_file = open(os.path.join(target_dir, 'output.txt'), 'w')
	for files in list_dir :
		fir_col = files
		open_files = open(target_dir+'/'+files, 'r')
		lines = open_files.readlines()
		long_line = ''
		for line in lines:
			long_line += line.strip()

		open_output_file.write(fir_col +'\t' + long_line + '\n')
	open_output_file.close()

