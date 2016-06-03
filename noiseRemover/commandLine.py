

import argparse
import os
import fnmatch

def recursive_search(directory, ext='words'):
	matches = []
	for root, dirnames, filenames in os.walk(directory):
		for filename in fnmatch.filter(filenames, '*.'+ext):
			matches.append(os.path.join(root, filename))
	return matches

def check_directories(directories):
	for key, value in args.iteritems():
		if not os.path.isdir(value):
			print 'ERROR: Directory, ', value, ' was not found'
			#exit(1)


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('word_test_dir', metavar='wrdTest', type=str,
					help='directory for the test images (words)')

parser.add_argument('word_trainnig_dir', metavar='wrdTrain', type=str,
					help='directory for the trainning images (words)')

parser.add_argument('xml_test_dir', metavar='xmlTest', type=str,
					help='directory for the labeled xml (words)')

parser.add_argument('xml_trainning_dir', metavar='xmlTrain', type=str,
					help='directory for the labeled xml (characters)')

args = vars(parser.parse_args())

xml_test_files = recursive_search(args['xml_test_dir'])
xml_trainning_files = recursive_search(args['xml_trainning_dir'])









